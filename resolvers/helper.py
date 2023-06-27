import functools
import inspect
from typing import Type, TypeVar

from databases.setup import getDB
from utils.bean_utils import getProperties


T = TypeVar('T')
S = TypeVar('S')

excludeFields = {'metadata', 'registry'}


def transformToGraphql(*, source: T, targetClass: Type[S]) -> S:
    target = targetClass(**getProperties(source, forbidden=excludeFields))
    return target


def getDBConnection(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        db = next(getDB())
        value = func(db=db, *args, **kwargs)
        if inspect.isawaitable(value):
            value = await value
        return value
    return wrapper
