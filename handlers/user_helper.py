import logging

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from databases.setting import tryUpdateSetting
from handlers.formatter import formatSettingFromORM
from structs.models.user import UserORM
from structs.schemas.setting import Setting, UpdateSettingOut
from utils.message import ERROR_MSG

logger = logging.getLogger(__name__)


async def tryUpdateUserSetting(dbUser: UserORM, setting: Setting, db: Session) -> UpdateSettingOut:
    dbSetting, isStale = await tryUpdateSetting(db, dbUser.id, setting)
    finalSetting = formatSettingFromORM(dbSetting)

    if isStale:
        return jsonable_encoder(UpdateSettingOut(data=finalSetting, isStale=isStale, error=ERROR_MSG.UPDATE_CONFLICT))
    return jsonable_encoder(UpdateSettingOut(data=finalSetting, isStale=isStale))
