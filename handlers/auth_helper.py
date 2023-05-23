from datetime import datetime, timedelta
import logging
from typing import Annotated
import uuid

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from config import JWT_SECRET_KEY, JWT_ALGO, JWT_ACCESS_TOKEN_EXPIRE_MINUTES
from databases.setting import createSetting
from databases.user import createUser, getAzureUser, getDetailedUser, getGoogleUser, getUser, getUserByUUID
from formatter.setting import formatDefaultSetting
from formatter.user import formatAzureUserFromReq, formatGoogleUserFromReq
from handlers.auth_validator import verifyLoginMethod, verifyLoginPayload
from handlers.oauth_validator import verifyOAuthToken
from structs.models.user import UserORM
from structs.requests.auth import ReqLogin
from structs.schemas.auth import Token, TokenData
from structs.schemas.user import User
from utils.caching.cache_store import CacheStore
from utils.caching.cacheable import cacheable
from utils.caching.helper import makeCacgeStoreConfig
from utils.constant import CACHE_TTL
from utils.enum import LoginMethodType
from utils.exception import HTTP_CREDENTIALS_EXCEPTION, HTTP_PAYLOAD_MALFORMED_EXCEPTION, HTTP_SERVER_EXCEPTION
from utils.type import DetailedUserORMType, DetailedUserType

logger = logging.getLogger(__name__)

oauth2Scheme = OAuth2PasswordBearer(tokenUrl='token')

cacheStore = CacheStore(makeCacgeStoreConfig())


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
            logger.exception('Error: JWT token malformed')
            raise HTTP_CREDENTIALS_EXCEPTION
        tokenData = TokenData(uuid=uuid, method=method, firstName=firstName, lastName=lastName, email=email)
    except JWTError as err:
        logger.exception(err)
        raise HTTP_CREDENTIALS_EXCEPTION
    return tokenData


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


@cacheable(cacheStore=cacheStore, ttl=CACHE_TTL['AUTH'])
async def getUserAndDetailedUserByTokenData(db: Session, tokenData: TokenData) -> tuple[UserORM, DetailedUserORMType]:
    dbUser = await getUserByUUID(db, uuid.UUID(tokenData.uuid))
    dbDetailedUser = await getDetailedUser(db, tokenData.method, dbUser.id)  # pyright: ignore[reportOptionalMemberAccess]
    return dbUser, dbDetailedUser


@cacheable(cacheStore=cacheStore, ttl=CACHE_TTL['AUTH'])
async def getUserAndDetailedUserByUser(db: Session, user: DetailedUserType) -> tuple[UserORM, DetailedUserORMType] | tuple[None, None]:
    dbDetailedUser = await getDetailedUserByUser(db, user)
    if dbDetailedUser is None:
        return None, None
    dbUser = await getUser(db, dbDetailedUser.userId)
    if dbUser is None:
        return None, None
    return dbUser, dbDetailedUser


async def getDetailedUserByUser(db: Session, user: User) -> DetailedUserORMType | None:
    dbDetailedUser = None
    if user.loginMethod == LoginMethodType.GOOGLE:
        dbDetailedUser = await getGoogleUser(db, user.email)
    if user.loginMethod == LoginMethodType.AZURE:
        dbDetailedUser = await getAzureUser(db, user.email)
    return dbDetailedUser


async def createNewUser(user: DetailedUserType, db: Session) -> tuple[UserORM, DetailedUserORMType]:
    try:
        dbUser, dbDetailedUser = await setupNewUser(db, user)
        return dbUser, dbDetailedUser
    except IntegrityError as err:  # e.g., email is not unique
        logger.exception(err)
        raise HTTP_PAYLOAD_MALFORMED_EXCEPTION
    except Exception as err:
        logger.exception(err)
        raise HTTP_SERVER_EXCEPTION


async def setupNewUser(db: Session, user: DetailedUserType) -> tuple[UserORM, DetailedUserORMType]:
    user.uuid = uuid.uuid4()
    dbUser, dbDetailedUser = await createUser(db, user)
    setting = formatDefaultSetting(dbUser.id)
    await createSetting(db, setting)
    return dbUser, dbDetailedUser


def formatDetailedUserFromReq(reqLogin: ReqLogin, accountId: str) -> DetailedUserType:
    detailedUser = None
    if reqLogin.loginMethod == LoginMethodType.GOOGLE:
        detailedUser = formatGoogleUserFromReq(reqLogin, accountId)
    if reqLogin.loginMethod == LoginMethodType.AZURE:
        detailedUser = formatAzureUserFromReq(reqLogin, accountId)
    return detailedUser
