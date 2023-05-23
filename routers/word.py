from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from databases.setup import getDB
from handlers.header import verifyHeader
from handlers.word import getUserCollectedWords
from routers.dependency import dbUserDep
from utils.caching.cache_store import CacheStore
from utils.caching.cacheable import cacheable
from utils.caching.helper import makeCacgeStoreConfig
from utils.constant import CACHE_TTL

from utils.enum import RouterGroupType

router = APIRouter(prefix='/collected-words', tags=[RouterGroupType.WORD], dependencies=[Depends(verifyHeader)])

cacheStore = CacheStore(makeCacgeStoreConfig())


@router.get('')
@cacheable(cacheStore=cacheStore, ttl=CACHE_TTL['WORD'])
async def getCollectedWords(dbUser: dbUserDep, db: Session = Depends(getDB)) -> List[int]:
    wordIds = await getUserCollectedWords(dbUser, db)
    return wordIds
