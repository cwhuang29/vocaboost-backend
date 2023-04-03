import logging
from typing import Annotated

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from handlers.auth_helper import authenticateUser, createAccessToken, setupNewUser, decodeAccessToken
from handlers.formatter import formatGoogleUserFromReq
from structs.requests.auth import ReqLogin
from structs.schemas.auth import Token, TokenData
from utils.enum import LoginMethodType
from databases.user import getUserByUUID
from databases.auth import createLoginRecord, createLogoutRecord
from utils.message import HTTP_ERROR_MSG

logger = logging.getLogger(__name__)

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="token")


def getTokenData(token: Annotated[str, Depends(oauth2Scheme)]) -> TokenData:
    return decodeAccessToken(token)


def handleGoogleLogin(reqLogin: ReqLogin, db: Session) -> TokenData:
    try:
        user = formatGoogleUserFromReq(reqLogin)
    except Exception as err:
        logger.error(str(err))
        raise HTTPException(status_code=400, detail=str(err))

    try:
        dbUser, dbDetailedUser = authenticateUser(db, reqLogin)
        if not dbUser:
            dbUser, dbDetailedUser = setupNewUser(db, user)

        createLoginRecord(db, dbUser.id)
        tokenData = TokenData(uuid=dbUser.uuid, method=dbUser.method, email=dbDetailedUser.email)  # pyright: ignore[reportOptionalMemberAccess]
    except IntegrityError as err:  # e.g., email is not unique
        raise HTTPException(status_code=400, detail=err._message())
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=500)
    return tokenData


def handleLogin(reqLogin: ReqLogin, db: Session) -> Token:
    token = None
    if reqLogin.loginMethod == LoginMethodType.GOOGLE:
        tokenData = handleGoogleLogin(reqLogin, db)
    else:
        raise HTTPException(status_code=400, detail=HTTP_ERROR_MSG.LOGIN_NOT_SUPPORT)
    token = createAccessToken(tokenData)
    return token


def handleLogout(tokenData: TokenData, db: Session):
    dbUser = getUserByUUID(db, tokenData.uuid)
    if dbUser:
        createLogoutRecord(db, dbUser.id)