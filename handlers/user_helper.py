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
    dbSetting = await tryUpdateSetting(db, dbUser.id, setting)
    finalSetting = formatSettingFromORM(dbSetting)

    if finalSetting.updatedAt != setting.updatedAt:
        return UpdateSettingOut(data=jsonable_encoder(finalSetting), isStale=True, error=ERROR_MSG.UPDATE_CONFLICT)
    return UpdateSettingOut(data=jsonable_encoder(finalSetting), isStale=False)
