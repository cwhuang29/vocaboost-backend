from typing import Optional

import strawberry

import databases.setting as databases
from gql.helpers.misc import getDBConnection
from gql.helpers.transform import transformSettingOut
from structs.graphql.setting import SettingOut


@getDBConnection
async def getSettingByUser(userId: int, *, db: Optional[str] = strawberry.UNSET) -> SettingOut:
    dbSetting = await databases.getSettingByUser(db, userId)
    return transformSettingOut(dbSetting)
