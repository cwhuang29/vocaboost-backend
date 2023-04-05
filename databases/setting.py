from sqlalchemy.orm import Session

from databases.setting_helper import getSettingORM
from structs.models.setting import SettingORM
from structs.schemas.setting import Setting


async def getSettingByUser(db: Session, userId: int):
    return db.query(SettingORM).filter(SettingORM.userId == userId).first()


async def tryUpdateSetting(db: Session, userId: int, setting: Setting) -> SettingORM:
    '''
    Only update the entity if argument's updatedAt is newer, otherwise return the original value
    '''
    dbSetting = await getSettingByUser(db, userId)
    if dbSetting.updatedAt > setting.updatedAt:  # pyright: ignore[reportOptionalMemberAccess]
        return dbSetting

    for key, value in setting.dict(exclude_unset=True).items():
        if type(value) is list:
            value = str(value)
        setattr(dbSetting, key, value)
    setattr(dbSetting, 'showDetail', 1 if setting.showDetail else 0)

    db.add(dbSetting)
    db.commit()
    return dbSetting


async def createSetting(db: Session, setting: Setting) -> SettingORM:
    dbSetting = getSettingORM(setting)
    db.add(dbSetting)
    db.commit()
    db.refresh(dbSetting)
    return dbSetting
