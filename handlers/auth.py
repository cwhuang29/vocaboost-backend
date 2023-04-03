import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from handlers.auth_helper import createTokenData, getUserAndDetailedUserByTokenData, createAccessToken, setupNewUser, decodeAccessToken
from handlers.auth_validator import checkLoginPayload
from handlers.formatter import formatGoogleUserFromReq
from structs.requests.auth import ReqLogin
from structs.schemas.auth import Token, TokenData
from structs.schemas.user import User
from utils.enum import LoginMethodType
from databases.user import getUserByUUID
from databases.auth import createLoginRecord, createLogoutRecord
from utils.message import ERROR_MSG, getErrMsg

logger = logging.getLogger(__name__)

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="token")  # Raise exception if token is not valid


def getTokenData(token: Annotated[str, Depends(oauth2Scheme)]) -> TokenData:
    return decodeAccessToken(token)


async def tryToGetTokenData(req: Request) -> TokenData | None:
    try:
        token = await oauth2Scheme(req)
        tokenData = decodeAccessToken(token)
        return tokenData
    except Exception:
        return None


def parseReqPayload(reqLogin: ReqLogin) -> User:
    try:
        user = None
        if reqLogin.loginMethod == LoginMethodType.GOOGLE:
            user = formatGoogleUserFromReq(reqLogin)
        else:
            raise HTTPException(status_code=400, detail=getErrMsg(ERROR_MSG.LOGIN_NOT_SUPPORT))
        return user
    except Exception as err:
        logger.error(str(err))
        raise HTTPException(status_code=400, detail=getErrMsg(errHead=ERROR_MSG.TRY_AGAIN, errBody=str(err)))


async def authenticateLogin(user: User, tokenData: TokenData | None, db: Session) -> TokenData:
    try:
        dbUser, dbDetailedUser = None, None
        if tokenData:
            # This is a valid and signed in user
            dbUser, dbDetailedUser = await getUserAndDetailedUserByTokenData(db, tokenData)
        else:
            # The token might had expired, or this is a new user first time login
            dbUser, dbDetailedUser = await checkLoginPayload(db, user)
            if not dbUser:
                dbUser, dbDetailedUser = await setupNewUser(db, user)
        tokenData = createTokenData(dbUser.uuid, dbUser.method, dbUser.first_name, dbUser.last_name, dbDetailedUser.email)  # pyright: ignore[reportOptionalMemberAccess]
        return tokenData
    except IntegrityError as err:  # e.g., email is not unique
        raise HTTPException(status_code=400, detail=getErrMsg(errHead=ERROR_MSG.TRY_AGAIN, errBody=err._message()))
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=500)


async def handleLogin(reqLogin: ReqLogin, tokenData: TokenData | None, db: Session) -> Token:
    user = parseReqPayload(reqLogin)
    tokenData = await authenticateLogin(user, tokenData, db)

    await createLoginRecord(db, tokenData.uuid)
    token = createAccessToken(tokenData)
    return token


async def handleLogout(tokenData: TokenData, db: Session) -> None:
    await createLogoutRecord(db, tokenData.uuid)  # Without await, the db query will not be executed even if server responds success
