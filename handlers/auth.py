from datetime import datetime
import logging

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from handlers.auth_helper import formatDetailedUserFromReq, getUserAndDetailedUserByTokenData, createAccessToken, setupNewUser, tryToGetUserOnLogin
from handlers.auth_validator import verifyLoginMethod, verifyLoginPayload
from handlers.oauth import getOAuthToken, getUserIdentifierFromIDToken
from handlers.oauth_validator import verifyOAuthToken
from structs.models.user import UserORM
from structs.requests.auth import ReqLogin
from structs.schemas.auth import LoginOut, TokenData
from utils.enum import ClientSourceType
from databases.auth import createLoginRecord, createLogoutRecord
from utils.exception import HTTP_CREDENTIALS_EXCEPTION, HTTP_PAYLOAD_MALFORMED_EXCEPTION, HTTP_SERVER_EXCEPTION
from utils.type import DetailedUserORMType, DetailedUserType

logger = logging.getLogger(__name__)


def parseLoginPayload(reqLogin: ReqLogin, accountId: str) -> DetailedUserType:
    try:
        user = formatDetailedUserFromReq(reqLogin, accountId)
        return user
    except Exception as err:
        logger.exception(err)
        raise HTTP_PAYLOAD_MALFORMED_EXCEPTION


def verifyLogin(reqLogin: ReqLogin, user, oauthToken) -> None:
    try:
        verifyLoginMethod(reqLogin.loginMethod)
        verifyOAuthToken(reqLogin.loginMethod, oauthToken)
        verifyLoginPayload(oauthToken, user)
    except Exception as err:
        logger.exception(err)
        raise HTTP_CREDENTIALS_EXCEPTION


def getLoginUser(reqLogin: ReqLogin, source: ClientSourceType) -> DetailedUserType:
    try:
        oauthToken = getOAuthToken(reqLogin.loginMethod, source, reqLogin.idToken)
        assert oauthToken is not None
        accountId = getUserIdentifierFromIDToken(reqLogin.loginMethod, oauthToken)
        user = parseLoginPayload(reqLogin, accountId)
        assert user is not None
        verifyLogin(reqLogin, user, oauthToken)
        return user
    except Exception as err:
        logger.exception(err)
        raise HTTP_PAYLOAD_MALFORMED_EXCEPTION


async def createUserIfNotExist(user: DetailedUserType, db: Session) -> tuple[UserORM, DetailedUserORMType, bool]:
    isNewUser = False
    try:
        dbUser, dbDetailedUser = await tryToGetUserOnLogin(db, user)
        if not dbUser:
            isNewUser = True
            dbUser, dbDetailedUser = await setupNewUser(db, user)
        assert dbUser is not None
        assert dbDetailedUser is not None
        return dbUser, dbDetailedUser, isNewUser
    except IntegrityError as err:  # e.g., email is not unique
        logger.exception(err)
        raise HTTP_PAYLOAD_MALFORMED_EXCEPTION
    except Exception as err:
        logger.exception(err)
        raise HTTP_SERVER_EXCEPTION


async def loadUserFromDB(user: DetailedUserType, tokenData: TokenData | None, db: Session) -> tuple[UserORM, DetailedUserORMType, bool]:
    isNewUser = False
    if tokenData:
        # This is a valid and signed in user
        dbUser, dbDetailedUser = await getUserAndDetailedUserByTokenData(db, tokenData)
    else:
        # This is a new user or old user whose auth token had expired
        dbUser, dbDetailedUser, isNewUser = await createUserIfNotExist(user, db)
    return dbUser, dbDetailedUser, isNewUser


async def handleLogin(reqLogin: ReqLogin, tokenData: TokenData | None, source: ClientSourceType, db: Session):
    reqLogin.timeStamp = datetime.utcnow()
    user = getLoginUser(reqLogin, source)
    dbUser, dbDetailedUser, isNewUser = await loadUserFromDB(user, tokenData, db)
    await createLoginRecord(db, dbUser.uuid, source)
    token = createAccessToken(dbUser.uuid, dbUser.method, dbUser.firstName, dbUser.lastName, dbDetailedUser.email)
    return LoginOut(token=token, isNewUser=isNewUser)


async def handleLogout(tokenData: TokenData, source: ClientSourceType, db: Session) -> None:
    await createLogoutRecord(db, tokenData.uuid, source)  # Without await, the db query will not be executed even if server responds success
