from typing import Optional

from pydantic import UUID4
import strawberry

import databases.user as databases
from resolvers.helper import getDBConnection, transformToGraphql
from structs.graphql.user import User, GoogleUser, AzureUser
from utils.enum import LoginMethodType


@getDBConnection
async def getUser(id: int, *, db: Optional[str] = strawberry.UNSET):
    dbUser = await databases.getUser(db, id)
    return transformToGraphql(source=dbUser, targetClass=User)


@getDBConnection
async def getUserByUUID(uuid: str, db: Optional[str] = strawberry.UNSET):
    dbUser = await databases.getUserByUUID(db, UUID4(uuid))
    return transformToGraphql(source=dbUser, targetClass=User)


@getDBConnection
async def getDetailedUser(method: int, email: str, *, db: Optional[str] = strawberry.UNSET):
    dbDetailedUser = None
    targetClass = None
    loginMethod = LoginMethodType(method)

    if loginMethod == LoginMethodType.GOOGLE:
        dbDetailedUser = await databases.getGoogleUser(db, email)
        targetClass = GoogleUser
    if loginMethod == LoginMethodType.AZURE:
        dbDetailedUser = await databases.getAzureUser(db, email)
        targetClass = AzureUser

    return transformToGraphql(source=dbDetailedUser, targetClass=targetClass)
