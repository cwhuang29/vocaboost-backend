from datetime import datetime, timedelta
from typing import Annotated
import uuid

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from config import JWT_SECRET_KEY, JWT_ALGO, JWT_ACCESS_TOKEN_EXPIRE_MINUTES
from databases.setting import createSetting
from databases.user import createUser, getAzureUser, getDetailedUser, getGoogleUser, getUser, getUserByUUID
from formatter.setting import formatDefaultSetting
from formatter.user import formatAzureUserFromReq, formatGoogleUserFromReq
from structs.models.user import UserORM
from structs.requests.auth import ReqLogin
from structs.schemas.auth import Token, TokenData
from structs.schemas.user import User
from utils.enum import LoginMethodType
from utils.exception import HTTP_CREDENTIALS_EXCEPTION
from utils.type import DetailedUserORMTypeAll, DetailedUserTypeAll

oauth2Scheme = OAuth2PasswordBearer(tokenUrl='token')


def createAccessToken(uuid: str, method: int, firstName: str, lastName: str, email: str | None = '', expiresDelta: timedelta | None = None) -> Token:
    payload = {
        'sub': uuid,
        'method': method,
        'firstName': firstName,
        'lastName': lastName,
        'email': email,
    }
    lifespan = expiresDelta if expiresDelta else timedelta(minutes=int(JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    expire = datetime.utcnow() + lifespan

    p = payload.copy()
    p.update({'exp': expire})
    encodedJWT = jwt.encode(p, JWT_SECRET_KEY, algorithm=JWT_ALGO)
    return Token(accessToken=encodedJWT, tokenType='bearer')


def decodeAccessToken(token: Annotated[str, Depends(oauth2Scheme)]) -> TokenData:
    tokenData = None
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGO])
        uuid: str = payload.get('sub')
        method: int = payload.get('method')
        firstName: int = payload.get('firstName')
        lastName: int = payload.get('lastName')
        email: int = payload.get('email')  # email may be None if we support different login methods in future

        if uuid is None or method is None:
            raise HTTP_CREDENTIALS_EXCEPTION
        tokenData = TokenData(uuid=uuid, method=method, firstName=firstName, lastName=lastName, email=email)
    except JWTError:
        raise HTTP_CREDENTIALS_EXCEPTION
    return tokenData


def formatDetailedUserFromReq(reqLogin: ReqLogin, accountId: str) -> DetailedUserTypeAll:
    detailedUser = None
    if reqLogin.loginMethod == LoginMethodType.GOOGLE:
        detailedUser = formatGoogleUserFromReq(reqLogin, accountId)
    if reqLogin.loginMethod == LoginMethodType.AZURE:
        detailedUser = formatAzureUserFromReq(reqLogin, accountId)
    return detailedUser


async def getUserAndDetailedUserByTokenData(db: Session, tokenData: TokenData) -> tuple[UserORM, DetailedUserORMTypeAll]:
    dbUser = await getUserByUUID(db, uuid.UUID(tokenData.uuid))
    dbDetailedUser = await getDetailedUser(db, tokenData.method, dbUser.id)  # pyright: ignore[reportOptionalMemberAccess]
    return dbUser, dbDetailedUser


async def tryToGetDetailedUserOnLogin(db: Session, user: User) -> DetailedUserORMTypeAll | None:
    dbDetailedUser = None
    if user.loginMethod == LoginMethodType.GOOGLE:
        dbDetailedUser = await getGoogleUser(db, user.email)
    if user.loginMethod == LoginMethodType.AZURE:
        dbDetailedUser = await getAzureUser(db, user.email)
    return dbDetailedUser


async def tryToGetUserOnLogin(db: Session, user: DetailedUserTypeAll) -> tuple[UserORM, DetailedUserORMTypeAll] | tuple[None, None]:
    dbDetailedUser = await tryToGetDetailedUserOnLogin(db, user)
    if dbDetailedUser is None:
        return None, None
    dbUser = await getUser(db, dbDetailedUser.userId)
    if dbUser is None:
        return None, None
    return dbUser, dbDetailedUser


async def setupNewUser(db: Session, user: DetailedUserTypeAll) -> tuple[UserORM, DetailedUserORMTypeAll]:
    user.uuid = uuid.uuid4()
    dbUser, dbDetailedUser = await createUser(db, user)
    setting = formatDefaultSetting(dbUser.id)
    await createSetting(db, setting)
    return dbUser, dbDetailedUser
