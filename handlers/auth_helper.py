from datetime import datetime, timedelta
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from sqlalchemy.orm import Session

from config import JWT_SECRET_KEY, JWT_ALGO, JWT_ACCESS_TOKEN_EXPIRE_MINUTES
from databases.setting import createSetting
from databases.user import createUser, getDetailedUser, getUserByUUID
from handlers.formatter import formatDefaultSetting
from structs.models.user import GoogleUserORM, UserORM
from structs.requests.auth import ReqLogin
from structs.schemas.auth import Token, TokenData
from structs.schemas.user import User
from utils.enum import LoginMethodType
from utils.message import HTTP_ERROR_MSG

oauth2Scheme = OAuth2PasswordBearer(tokenUrl="token")

HTTPCredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=HTTP_ERROR_MSG.CREDENTIAL_MISS,
    headers={"WWW-Authenticate": "Bearer"},
)


def createAccessToken(tokenData: TokenData, expiresDelta: timedelta | None = None) -> Token:
    payload = {
        "sub": tokenData.uuid,
        "method": tokenData.method,
        "email": tokenData.email
    }
    lifespan = expiresDelta if expiresDelta else timedelta(minutes=int(JWT_ACCESS_TOKEN_EXPIRE_MINUTES))
    expire = datetime.utcnow() + lifespan

    p = payload.copy()
    p.update({"exp": expire})
    encodedJWT = jwt.encode(p, JWT_SECRET_KEY, algorithm=JWT_ALGO)
    return Token(accessToken=encodedJWT, tokenType="bearer")


def decodeAccessToken(token: Annotated[str, Depends(oauth2Scheme)]) -> TokenData:
    tokenData = None
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGO])
        uuid: str = payload.get("sub")
        method: int = payload.get("method")
        email: int = payload.get("email")  # email may be None if we support different login methods in future

        if uuid is None or method is None:
            raise HTTPCredentialsException
        tokenData = TokenData(uuid=uuid, method=method, email=email)
    except JWTError:
        raise HTTPCredentialsException
    return tokenData


def loginPayloadMalformed(reqLogin: ReqLogin, dbUser: UserORM, dbDetailedUser: GoogleUserORM):
    if reqLogin.loginMethod.value != dbUser.method:
        return None
    if reqLogin.loginMethod == LoginMethodType.GOOGLE:
        if reqLogin.detail.email != dbDetailedUser.email:
            return None


async def authenticateUser(db: Session, reqLogin: ReqLogin):
    dbUser = await getUserByUUID(db, reqLogin.uuid)
    if not dbUser:
        return None, None
    dbDetailedUser = await getDetailedUser(db, dbUser.method, dbUser.id)
    if not dbDetailedUser:
        return None, None
    if loginPayloadMalformed(reqLogin, dbUser, dbDetailedUser):
        return None, None
    return dbUser, dbDetailedUser


async def authenticateUserByTokenData(db: Session, tokenData: TokenData):
    dbUser = await getUserByUUID(db, tokenData.uuid)
    if not dbUser:
        return None
    dbDetailedUser = await getDetailedUser(db, tokenData.method, dbUser.id)
    if not dbDetailedUser:
        return None
    return dbUser, dbDetailedUser


async def setupNewUser(db: Session, user: User) -> tuple[UserORM, GoogleUserORM]:
    dbUser, dbDetailedUser = await createUser(db, user)
    setting = formatDefaultSetting(dbUser.id)
    await createSetting(db, setting)
    return dbUser, dbDetailedUser
