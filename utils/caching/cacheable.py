import functools
import inspect
import logging
import pickle
from typing import Callable

from utils.caching.cache_store import CacheStore
from utils.caching.helper import makeCacgeStoreConfig, makeCacheKey

logger = logging.getLogger(__name__)

DEFAULT_SHORT_TTL = 60 * 2  # For preventing cache penetration

# Note: since we have to "await" cache operations, functions applied to the decorator
#       have to be awaited (even if originally we do not)


def cacheable(_func=None, *, cacheStore: CacheStore, cacheKey: str | Callable[..., str] = None, ttl: int = DEFAULT_SHORT_TTL):
    if _func is None:
        cacheStore = CacheStore(makeCacgeStoreConfig())
        return functools.partial(cacheable, cacheStore=cacheStore, cacheKey=cacheKey, ttl=ttl)

    def wrapper(func):
        @functools.wraps(func)
        async def _wrapper(*args, **kwargs):
            cacheStoreIsLive = True
            key = makeCacheKey(cacheKey, func.__name__, False, *args, **kwargs)
            try:
                cachedValue = await cacheStore.get(key)
                if cachedValue:
                    logger.warning(f'[cacheable] cache hit. key: {key}')
                    return pickle.loads(cachedValue)
            except Exception as err:
                logger.exception(f'[cacheable] read cache error. key: {key}. error: {err}')
                cacheStoreIsLive = False

            value = func(*args, **kwargs)
            if inspect.isawaitable(value):  # Alternative: inspect.iscoroutinefunction(func)
                value = await value

            if cacheStoreIsLive:
                valueStr = pickle.dumps(value)
                try:
                    if value:
                        logger.warning(f'[cacheable] cache missed. Update cache with latest value. key: {key}')
                        await cacheStore.set(key=key, value=valueStr, ttl=ttl)
                    else:
                        logger.warning(f'[cacheable] cache missed. Latest data is empty (update with short ttl). key: {key}')
                        await cacheStore.set(key=key, value=valueStr, ttl=DEFAULT_SHORT_TTL)
                except Exception as err:
                    logger.exception(f'[cacheable] set cache error. key: {key}. error:  {err}')
            return value
        return _wrapper
    return wrapper(_func)
