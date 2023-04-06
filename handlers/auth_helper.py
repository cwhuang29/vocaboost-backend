from datetime import datetime, timedelta
from typing import Annotated
import uuid

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from config import JWT_SECRET_KEY, JWT_ALGO, JWT_ACCESS_TOKEN_EXPIRE_MINUTES
from databases.setting import createSetting
from databases.user import createUser, getDetailedUser, getUserByUUID
from handlers.formatter import formatDefaultSetting
from structs.models.user import GoogleUserORM, UserORM
from structs.schemas.auth import Token, TokenData
from structs.schemas.user import User
from utils.message import getShouldLoginMsg

oauth2Scheme = OAuth2PasswordBearer(tokenUrl='token')

HTTPCredentialsException = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=getShouldLoginMsg(),
    headers={'WWW-Authenticate': 'Bearer'},
)


def createAccessToken(tokenData: TokenData, expiresDelta: timedelta | None = None) -> Token:
    payload = {
        'sub': tokenData.uuid,
        'method': tokenData.method,
        'firstName': tokenData.firstName,
        'lastName': tokenData.lastName,
        'email': tokenData.email,
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
            raise HTTPCredentialsException
        tokenData = TokenData(uuid=uuid, method=method, firstName=firstName, lastName=lastName, email=email)
    except JWTError:
        raise HTTPCredentialsException
    return tokenData


def createTokenData(uuid: str, method: int, firstName: str, lastName: str, email: str | None = '') -> TokenData:
    return TokenData(
        uuid=uuid,
        method=method,
        firstName=firstName,
        lastName=lastName,
        email=email
    )


async def getUserAndDetailedUserByTokenData(db: Session, tokenData: TokenData) -> tuple[UserORM, GoogleUserORM]:
    dbUser = await getUserByUUID(db, uuid.UUID(tokenData.uuid))
    dbDetailedUser = await getDetailedUser(db, tokenData.method, dbUser.id)  # pyright: ignore[reportOptionalMemberAccess]
    return dbUser, dbDetailedUser


async def setupNewUser(db: Session, user: User) -> tuple[UserORM, GoogleUserORM]:
    user.uuid = uuid.uuid4()
    dbUser, dbDetailedUser = await createUser(db, user)

    setting = formatDefaultSetting(dbUser.id)
    await createSetting(db, setting)
    return dbUser, dbDetailedUser
