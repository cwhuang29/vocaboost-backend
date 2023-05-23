import functools
import inspect
import logging
from typing import Callable

from utils.caching.cache_store import CacheStore
from utils.caching.helper import makeCacgeStoreConfig, makeCacheKey

logger = logging.getLogger(__name__)


def makeCacheClearKey(prefix: str, takeFirstArg: bool = True):
    return functools.partial(makeCacheKey, cacheKey=None, funcName=prefix, takeFirstArg=takeFirstArg)


def cacheclear(_func=None, *, cacheStore: CacheStore, cacheKey: str | Callable[..., str] = None):
    if _func is None:
        cacheStore = CacheStore(makeCacgeStoreConfig())
        return functools.partial(cacheclear, cacheStore=cacheStore, cacheKey=cacheKey)

    def wrapper(func):
        @functools.wraps(func)
        async def _wrapper(*args, **kwargs):
            key = makeCacheKey(cacheKey, func.__name__, False, *args, **kwargs)
            try:
                await cacheStore.delete(key)
                logger.warning(f'[cacheclear] delete cache. key: {key}')
            except Exception as err:
                logger.exception(f'[cacheclear] delete cache error. key: {key}. error:  {err}')

            value = func(*args, **kwargs)
            if inspect.isawaitable(value):
                value = await value
            return value
        return _wrapper
    return wrapper(_func)
