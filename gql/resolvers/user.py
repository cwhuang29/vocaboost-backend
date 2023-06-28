from typing import Optional
import uuid

import strawberry
from strawberry.types import Info

import databases.user as databases
from gql.helpers.misc import getDBConnection
from gql.helpers.transform import transformToGraphqlSchema, transformUserOut
from handlers.auth_helper import getUserAndDetailedUserByTokenData
from structs.graphql.user import User, GoogleUser, AzureUser
from utils.enum import LoginMethodType


def getDummy(info: Info) -> str:
    headers = info.context.request.headers
    return f'Hello Graphql. Your request header: {str(headers)}'


@getDBConnection
async def getUser(info: Info, id: Optional[int] = strawberry.UNSET, *, db: Optional[str] = strawberry.UNSET):
    if id:
        dbUser = await databases.getUser(db, id)
    else:
        _uuid = uuid.UUID(info.context.tokenData.uuid)
        dbUser = await databases.getUserByUUID(db, _uuid)
    return transformToGraphqlSchema(source=dbUser, targetClass=User)


@getDBConnection
async def getMe(info: Info, *, db: Optional[str] = strawberry.UNSET):
    dbUser, dbDetailedUser = await getUserAndDetailedUserByTokenData(db, info.context.tokenData)
    return transformUserOut(dbUser, dbDetailedUser)


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

    return transformToGraphqlSchema(source=dbDetailedUser, targetClass=targetClass)
