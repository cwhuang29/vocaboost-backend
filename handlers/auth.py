import logging
from typing import Tuple

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from handlers.auth_helper import formatDetailedUserFromReq, getUserAndDetailedUserByTokenData, createAccessToken, setupNewUser, tryToGetUserOnLogin
from handlers.auth_validator import verifyLoginPayload
from handlers.oauth_validator import getOAuthToken, verifyOAuthToken
from structs.requests.auth import ReqLogin
from structs.schemas.auth import LoginOut, TokenData
from utils.enum import ClientSourceType
from databases.auth import createLoginRecord, createLogoutRecord
from utils.exception import HTTP_CREDENTIALS_EXCEPTION, HTTP_PAYLOAD_MALFORMED_EXCEPTION, HTTP_SERVER_EXCEPTION

logger = logging.getLogger(__name__)


def parseLoginPayload(reqLogin: ReqLogin, accountId: str):
    try:
        user = formatDetailedUserFromReq(reqLogin, accountId)
        return user
    except Exception as err:
        logger.error(str(err))
        raise HTTP_PAYLOAD_MALFORMED_EXCEPTION


def verifyAppLogin(reqLogin: ReqLogin, user, oauthToken):
    try:
        verifyOAuthToken(reqLogin.loginMethod, oauthToken)
        verifyLoginPayload(oauthToken, user)
    except Exception:
        raise HTTP_CREDENTIALS_EXCEPTION


def getAppLoginUser(reqLogin: ReqLogin) -> LoginOut:
    try:
        oauthToken = getOAuthToken(reqLogin.loginMethod, reqLogin.idToken)
        user = parseLoginPayload(reqLogin, oauthToken.sub)
        verifyAppLogin(reqLogin, user, oauthToken)
    except Exception:
        raise HTTP_PAYLOAD_MALFORMED_EXCEPTION
    return user


def getExtLoginUser(reqLogin: ReqLogin) -> LoginOut:
    user = parseLoginPayload(reqLogin, reqLogin.accountId)
    return user


def getLoginUser(reqLogin: ReqLogin, source: ClientSourceType):
    user = None
    if source == ClientSourceType.MOBILE:
        user = getAppLoginUser(reqLogin)
    if source == ClientSourceType.EXTENSION:
        user = getExtLoginUser(reqLogin)
    assert user is not None
    return user


async def createUserIfNotExist(user, db: Session) -> Tuple[TokenData, bool]:
    try:
        dbUser, dbDetailedUser = await tryToGetUserOnLogin(db, user)
        if not dbUser:
            dbUser, dbDetailedUser = await setupNewUser(db, user)
        return dbUser, dbDetailedUser
    except IntegrityError as err:  # e.g., email is not unique
        logger.error(str(err))
        raise HTTP_PAYLOAD_MALFORMED_EXCEPTION
    except Exception as err:
        logger.error(err)
        raise HTTP_SERVER_EXCEPTION


async def loadUserFromDB(user, tokenData: TokenData | None, db: Session):
    isNewUser = tokenData is not None
    if tokenData:
        # This is a valid and signed in user
        dbUser, dbDetailedUser = await getUserAndDetailedUserByTokenData(db, tokenData)
    else:
        # This is a new user or old user whose auth token had expired
        dbUser, dbDetailedUser = await createUserIfNotExist(user, db)
    return dbUser, dbDetailedUser, isNewUser


async def handleLogin(reqLogin: ReqLogin, tokenData: TokenData | None, source: ClientSourceType, db: Session):
    user = getLoginUser(reqLogin, source)
    dbUser, dbDetailedUser, isNewUser = await loadUserFromDB(user, tokenData, db)
    await createLoginRecord(db, dbUser.uuid, source)
    token = createAccessToken(dbUser.uuid, dbUser.method, dbUser.firstName, dbUser.lastName, dbDetailedUser.email)
    return LoginOut(token=token, isNewUser=isNewUser)


async def handleLogout(tokenData: TokenData, source: ClientSourceType, db: Session) -> None:
    await createLogoutRecord(db, tokenData.uuid, source)  # Without await, the db query will not be executed even if server responds success
