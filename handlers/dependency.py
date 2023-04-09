from typing import Annotated

from fastapi import Depends, Request
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from databases.setup import getDB
from databases.user import getUserByUUID

from handlers.auth_helper import decodeAccessToken
from structs.models.user import UserORM
from structs.schemas.auth import TokenData
from utils.exception import HTTP_CREDENTIALS_EXCEPTION


oauth2Scheme = OAuth2PasswordBearer(tokenUrl='token')  # Raise exception if token is not valid


def getTokenData(token: Annotated[str, Depends(oauth2Scheme)]) -> TokenData:
    return decodeAccessToken(token)


async def getDbUserByTokenData(token: Annotated[str, Depends(oauth2Scheme)], db: Session = Depends(getDB)) -> UserORM:
    tokenData = decodeAccessToken(token)
    dbUser = await getUserByUUID(db, tokenData.uuid)
    if dbUser is None:
        raise HTTP_CREDENTIALS_EXCEPTION
    return dbUser


async def tryToGetTokenData(req: Request) -> TokenData | None:
    try:
        token = await oauth2Scheme(req)
        tokenData = decodeAccessToken(token)
        return tokenData
    except Exception:
        return None
