from fastapi import Depends, APIRouter, WebSocket
from sqlalchemy.orm import Session

from databases.setup import getDB
from handlers.user import getUserSetting, getMe, updateUserCollectedWordsWS, updateUserSetting, updateUserSettingWS
from routers.dependency import tokenDataDep, dbUserDep
from structs.schemas.setting import Setting, UpdateSettingOut
from utils.caching.cache_store import CacheStore
from utils.caching.cacheable import cacheable
from utils.caching.cacheclear import cacheclear, makeCacheClearKey
from utils.caching.helper import makeCacgeStoreConfig
from utils.constant import CACHE_TTL
from utils.enum import RouterGroupType

router = APIRouter(prefix='/users', tags=[RouterGroupType.USER])

cacheStore = CacheStore(makeCacgeStoreConfig())


@router.get('/me')
@cacheable(cacheStore=cacheStore, ttl=CACHE_TTL['USER'])
async def me(tokenData: tokenDataDep, db: Session = Depends(getDB)):
    resp = await getMe(tokenData, db)
    return resp


@router.get('/setting', response_model=Setting)
@cacheable(cacheStore=cacheStore, ttl=CACHE_TTL['SETTING'])
async def getSetting(dbUser: dbUserDep, db: Session = Depends(getDB)) -> Setting:
    resp = await getUserSetting(dbUser, db)
    return resp


@router.put('/setting')
@cacheclear(cacheStore=cacheStore, cacheKey=makeCacheClearKey(prefix=getSetting.__name__))
async def updateSetting(dbUser: dbUserDep, setting: Setting, db: Session = Depends(getDB)) -> UpdateSettingOut:
    # Note that the datetime object had been transformed to UTC timezone by fastapi already
    resp = await updateUserSetting(dbUser, setting, db)
    return resp


@router.websocket('/setting')
async def updateSettingWebSocket(websocket: WebSocket, db: Session = Depends(getDB)) -> None:
    await updateUserSettingWS(websocket, db)


@router.websocket('/setting/collected-words')
async def updateCollectedWordsWebSocket(websocket: WebSocket, db: Session = Depends(getDB)) -> None:
    await updateUserCollectedWordsWS(websocket, db)
