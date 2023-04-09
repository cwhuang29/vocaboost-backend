import ast
from datetime import datetime
import logging
from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from databases.setting import tryUpdateCollectedWords, tryUpdateSetting
from formatter.setting import formatSettingFromORM
from structs.models.user import UserORM
from structs.schemas.setting import Setting, UpdateCollectedWordsOut, UpdateSettingOut
from utils.message import ERROR_MSG

logger = logging.getLogger(__name__)


async def tryUpdateUserSetting(dbUser: UserORM, setting: Setting, db: Session) -> UpdateSettingOut:
    dbSetting, isStale = await tryUpdateSetting(db, dbUser.id, setting)
    finalSetting = formatSettingFromORM(dbSetting)
    error = None if not isStale else ERROR_MSG.UPDATE_CONFLICT
    resp = UpdateSettingOut(data=finalSetting, isStale=isStale, error=error)
    return jsonable_encoder(resp)


async def tryUpdateUserCollectedWords(dbUser: UserORM, collectedWords: List[int], ts: datetime, db: Session) -> UpdateCollectedWordsOut:
    dbSetting, isStale = await tryUpdateCollectedWords(db, dbUser.id, collectedWords, ts)
    error = None if not isStale else ERROR_MSG.UPDATE_CONFLICT
    resp = UpdateCollectedWordsOut(data=ast.literal_eval(dbSetting.collectedWords), ts=dbSetting.updatedAt, isStale=isStale, error=error)
    return jsonable_encoder(resp)
