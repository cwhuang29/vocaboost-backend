from datetime import datetime, timezone
from typing import List, Tuple
from sqlalchemy.orm import Session

from databases.setting_helper import getSettingORM
from structs.models.setting import SettingORM
from structs.schemas.setting import Setting


async def getSettingByUser(db: Session, userId: int):
    return db.query(SettingORM).filter(SettingORM.userId == userId).first()


async def tryUpdateCollectedWords(db: Session, userId: int, collectedWords: List[int], ts: datetime) -> Tuple[SettingORM, bool]:
    dbSetting = await getSettingByUser(db, userId)
    assert dbSetting is not None

    tsUTC = ts.replace(tzinfo=timezone.utc)
    if dbSetting.updatedAt.replace(tzinfo=timezone.utc) > tsUTC:
        return dbSetting, True

    setattr(dbSetting, 'collectedWords', str(collectedWords))
    setattr(dbSetting, 'updatedAt', tsUTC)
    db.add(dbSetting)
    db.commit()
    return dbSetting, False


async def tryUpdateSetting(db: Session, userId: int, setting: Setting) -> Tuple[SettingORM, bool]:
    dbSetting = await getSettingByUser(db, userId)
    assert dbSetting is not None

    if dbSetting.updatedAt.replace(tzinfo=timezone.utc) > setting.updatedAt.replace(tzinfo=timezone.utc):
        return dbSetting, True

    for key, value in setting.dict(exclude_unset=True).items():
        if isinstance(value, list):
            value = str(value)
        setattr(dbSetting, key, value)
    setattr(dbSetting, 'showDetail', 1 if setting.showDetail else 0)

    db.add(dbSetting)
    db.commit()
    return dbSetting, False


async def createSetting(db: Session, setting: Setting) -> SettingORM:
    dbSetting = getSettingORM(setting)
    db.add(dbSetting)
    db.commit()
    db.refresh(dbSetting)
    return dbSetting
