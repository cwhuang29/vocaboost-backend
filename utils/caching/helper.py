from typing import Callable
from sqlalchemy.orm import Session

from config import REDIS_HOST, REDIS_PASSWORD
from utils.caching.cache_store_config import CacheStoreConfig


def isDesiredType(arg) -> bool:
    if isinstance(arg, Session):
        return False
    return True


def removeIncorrectType(*args, **kwargs):
    args = tuple(filter(lambda arg: isDesiredType(arg), args))
    kwargs = {key: val for key, val in kwargs.items() if isDesiredType(val)}
    return args, kwargs


def transformFuncArg(arg) -> str:
    return repr(arg).strip().lower()

# If cacheable is decorated at FastAPI path operation functions, then args will be empty
def makeCacheKey(cacheKey: str| Callable[..., str], funcName: str, takeFirstArg: bool, *args, **kwargs) -> str:
    key = cacheKey
    if cacheKey and callable(cacheKey):
        key = cacheKey(*args, **kwargs)
    if key and isinstance(key, str):
        return key

    args, kwargs = removeIncorrectType(*args, **kwargs)
    if takeFirstArg:
        parsedArgs1 = transformFuncArg(list(args)[0]) if args else None
        parsedArgs2 = transformFuncArg(list(kwargs.values())[0]) if kwargs else None
    else:
        parsedArgs1 = ':'.join([transformFuncArg(arg) for arg in args])
        parsedArgs2 = ':'.join(map(lambda arg: transformFuncArg(arg), kwargs.values()))
    parsedArgs = parsedArgs1 if parsedArgs1 else parsedArgs2
    return f'{funcName}|{parsedArgs}'


def getCacheStoreURL():
    return f'redis://:{REDIS_PASSWORD}@{REDIS_HOST}'


def makeCacgeStoreConfig() -> CacheStoreConfig:
    url = getCacheStoreURL()
    return CacheStoreConfig(url=url)
