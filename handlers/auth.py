from datetime import datetime
import logging

from sqlalchemy.orm import Session

from handlers.auth_helper import createNewUser, getUserAndDetailedUserByTokenData, createAccessToken, parseLoginPayload, getUserAndDetailedUserByUser, verifyLogin
from handlers.oauth import getOAuthToken, getUserIdentifierFromIDToken
from structs.models.user import UserORM
from structs.requests.auth import ReqLogin
from structs.schemas.auth import LoginOut, TokenData
from utils.caching.cache_store import CacheStore
from utils.caching.cacheable import cacheable
from utils.caching.helper import makeCacgeStoreConfig
from utils.constant import CACHE_TTL
from utils.enum import ClientSourceType, DevicePlatformType
from databases.auth import createLoginRecord, createLogoutRecord
from utils.exception import HTTP_PAYLOAD_MALFORMED_EXCEPTION
from utils.type import DetailedUserORMType, DetailedUserType

logger = logging.getLogger(__name__)

cacheStore = CacheStore(makeCacgeStoreConfig())


@cacheable(cacheStore=cacheStore, ttl=CACHE_TTL['AUTH'])
def getLoginUser(reqLogin: ReqLogin, source: ClientSourceType, platform: DevicePlatformType) -> DetailedUserType:
    try:
        oauthToken = getOAuthToken(reqLogin.idToken, reqLogin.loginMethod, source, platform)
        assert oauthToken is not None
        accountId = getUserIdentifierFromIDToken(reqLogin.loginMethod, oauthToken)
        user = parseLoginPayload(reqLogin, accountId)
        assert user is not None
        verifyLogin(reqLogin, user, oauthToken)
        return user
    except Exception as err:
        logger.exception(err)
        raise HTTP_PAYLOAD_MALFORMED_EXCEPTION


@cacheable(cacheStore=cacheStore, ttl=CACHE_TTL['AUTH'])
async def loadUserFromDB(user: DetailedUserType, tokenData: TokenData | None, db: Session) -> tuple[UserORM, DetailedUserORMType, bool]:
    isNewUser = False
    if tokenData:
        # This is a valid and signed in user
        dbUser, dbDetailedUser = await getUserAndDetailedUserByTokenData(db, tokenData)
    else:
        # This is a new user or old user whose auth token had expired
        dbUser, dbDetailedUser = await getUserAndDetailedUserByUser(db, user)
        if not dbUser:
            isNewUser = True
            dbUser, dbDetailedUser = await createNewUser(user, db)
    return dbUser, dbDetailedUser, isNewUser


async def handleLogin(reqLogin: ReqLogin, tokenData: TokenData | None, source: ClientSourceType, platform: DevicePlatformType, db: Session):
    reqLogin.timeStamp = datetime.utcnow()
    user = await getLoginUser(reqLogin, source, platform)
    dbUser, dbDetailedUser, isNewUser = await loadUserFromDB(user, tokenData, db)
    await createLoginRecord(db, dbUser.uuid, source)
    token = createAccessToken(dbUser.uuid, dbUser.method, dbUser.firstName, dbUser.lastName, dbDetailedUser.email)
    return LoginOut(token=token, isNewUser=isNewUser)


async def handleLogout(tokenData: TokenData, source: ClientSourceType, db: Session) -> None:
    await createLogoutRecord(db, tokenData.uuid, source)  # Without await, the db query will not be executed even if server responds success
