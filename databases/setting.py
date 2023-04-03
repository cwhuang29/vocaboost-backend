from sqlalchemy.orm import Session

from databases.setting_helper import getSettingORM
from structs.models.setting import SettingORM
from structs.schemas.setting import Setting


async def getSettingsByUser(db: Session, id: int):
    return db.query(SettingORM).filter(SettingORM.user_id == id).first()


async def createSetting(db: Session, setting: Setting) -> SettingORM:
    dbSetting = getSettingORM(setting)
    db.add(dbSetting)
    db.commit()
    db.refresh(dbSetting)
    return dbSetting
