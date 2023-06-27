import ast
from typing import Optional

import strawberry

import databases.setting as databases
from resolvers.helper import getDBConnection
from structs.graphql.setting import Setting


@getDBConnection
async def getSettingByUser(userId: int, *, db: Optional[str] = strawberry.UNSET):
    dbSetting = await databases.getSettingByUser(db, userId)
    assert dbSetting is not None

    return Setting(
        userId=dbSetting.userId,
        highlightColor=dbSetting.highlightColor,
        language=dbSetting.language,
        fontSize=dbSetting.fontSize,
        showDetail=True if dbSetting.showDetail == 1 else False,
        collectedWords=ast.literal_eval(dbSetting.collectedWords),
        suspendedPages=ast.literal_eval(dbSetting.suspendedPages),
        updatedAt=dbSetting.updatedAt,
    )
