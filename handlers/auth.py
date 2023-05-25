import logging

from sqlalchemy.orm import Session

from handlers.auth_helper import createNewUser, createAccessToken, parseLoginPayload, getUserAndDetailedUserByUser, verifyLogin
from handlers.oauth import getOAuthToken, getUserIdentifierFromIDToken
from structs.requests.auth import ReqLogin
from structs.schemas.auth import LoginOut, TokenData
from utils.caching.cache_store import CacheStore
from utils.caching.cacheable import cacheable
from utils.caching.helper import makeCacgeStoreConfig
from utils.constant import CACHE_TTL
from utils.enum import ClientSourceType, DevicePlatformType
from utils.exception import HTTP_PAYLOAD_MALFORMED_EXCEPTION
from utils.type import DetailedUserType, OAuthTokenType

logger = logging.getLogger(__name__)

cacheStore = CacheStore(makeCacgeStoreConfig())


@cacheable(cacheStore=cacheStore, ttl=CACHE_TTL['AUTH'])
async def getLoginUser(reqLogin: ReqLogin, source: ClientSourceType, platform: DevicePlatformType) -> tuple[DetailedUserType, OAuthTokenType]:
    oauthToken = getOAuthToken(reqLogin.idToken, reqLogin.loginMethod, source, platform)
    assert oauthToken is not None
    accountId = getUserIdentifierFromIDToken(reqLogin.loginMethod, oauthToken)
    user = parseLoginPayload(reqLogin, accountId)
    assert user is not None
    return user, oauthToken


async def handleLogin(reqLogin: ReqLogin, source: ClientSourceType, platform: DevicePlatformType, db: Session):
    # Note: it is not safe to use cacheable at any places before verifying id token (issued by OpenID connect)
    try:
        user, oauthToken = await getLoginUser(reqLogin, source, platform)
        verifyLogin(reqLogin, user, oauthToken)

        dbUser, dbDetailedUser = await getUserAndDetailedUserByUser(db, user)
        isNewUser = False if dbUser else True
        if not dbUser:
            dbUser, dbDetailedUser = await createNewUser(user, db)

        token = createAccessToken(dbUser, dbDetailedUser)
        return LoginOut(token=token, isNewUser=isNewUser)
    except Exception as err:
        logger.exception(err)
        raise HTTP_PAYLOAD_MALFORMED_EXCEPTION


async def handleLogout(tokenData: TokenData, source: ClientSourceType, db: Session) -> None:
    pass
