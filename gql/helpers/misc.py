import functools
import inspect

from databases.setup import getDB


def getDBConnection(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        db = next(getDB())
        value = func(db=db, *args, **kwargs)
        if inspect.isawaitable(value):
            value = await value
        return value
    return wrapper
