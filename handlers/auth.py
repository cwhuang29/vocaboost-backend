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
from utils.exception import HTTP_PAYLOAD_MALFORMED_EXCEPTION
from utils.type import DetailedUserORMType, DetailedUserType, OAuthTokenType

logger = logging.getLogger(__name__)

cacheStore = CacheStore(makeCacgeStoreConfig())


async def handleLogin(reqLogin: ReqLogin, tokenData: TokenData | None, source: ClientSourceType, platform: DevicePlatformType, db: Session):
    # Note: it is not safe to use cacheable at any places before verifying OpenID connect's ID tokens
    try:
        user, oauthToken = await getLoginUser(reqLogin, source, platform)
        verifyLogin(reqLogin, user, oauthToken)
        dbUser, dbDetailedUser, isNewUser = await loadUserFromDB(user, tokenData, db)
        token = createAccessToken(dbUser.uuid, dbUser.method, dbUser.firstName, dbUser.lastName, dbDetailedUser.email)
        return LoginOut(token=token, isNewUser=isNewUser)
    except Exception as err:
        logger.exception(err)
        raise HTTP_PAYLOAD_MALFORMED_EXCEPTION


async def handleLogout(tokenData: TokenData, source: ClientSourceType, db: Session) -> None:
    pass


@cacheable(cacheStore=cacheStore, ttl=CACHE_TTL['AUTH'])
async def getLoginUser(reqLogin: ReqLogin, source: ClientSourceType, platform: DevicePlatformType) -> tuple[DetailedUserType, OAuthTokenType]:
    oauthToken = getOAuthToken(reqLogin.idToken, reqLogin.loginMethod, source, platform)
    assert oauthToken is not None
    accountId = getUserIdentifierFromIDToken(reqLogin.loginMethod, oauthToken)
    user = parseLoginPayload(reqLogin, accountId)
    assert user is not None
    return user, oauthToken


# Note: if a new user just created the account, logout, then re-login, sqlalchemy throws this error:
# sqlalchemy.orm.exc.DetachedInstanceError: Instance <UserORM at 0x10a4e84d0> is not bound to a Session; attribute refresh operation cannot proceed
# One trick to solve this issue is 'use' the cached value (e.g., print it out) inside cacheable, so it raises error immediately and
# we fall back to reading data from database. For now I choose to only apply cacheable to functions which do not have side-effect
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
