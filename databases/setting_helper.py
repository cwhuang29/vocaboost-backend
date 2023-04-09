from datetime import datetime

from structs.models.setting import SettingORM
from structs.schemas.setting import Setting


def getSettingORM(setting: Setting) -> SettingORM:
    return SettingORM(
        userId=setting.userId,
        highlightColor=setting.highlightColor,
        language=setting.language,
        fontSize=setting.fontSize,
        showDetail=1 if setting.showDetail else 0,
        collectedWords=str(setting.collectedWords),
        suspendedPages=str(setting.suspendedPages),
        updatedAt=setting.updatedAt or datetime.utcnow()
    )
