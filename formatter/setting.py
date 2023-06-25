import ast
from datetime import datetime

from structs.models.setting import SettingORM
from structs.schemas.setting import Setting
from utils.setting import DEFAULT_SETTING


def formatDefaultSetting(userId: int) -> Setting:
    return Setting(
        userId=userId,
        highlightColor=DEFAULT_SETTING.highlightColor,
        language=DEFAULT_SETTING.language,
        fontSize=DEFAULT_SETTING.fontSize,
        showDetail=DEFAULT_SETTING.showDetail,
        collectedWords=DEFAULT_SETTING.collectedWords,
        suspendedPages=DEFAULT_SETTING.suspendedPages,
        updatedAt=DEFAULT_SETTING.updatedAt,
    )


def formatSettingFromWS(setting: dict, userId: int, ts: datetime) -> Setting:
    return Setting(
        userId=userId,
        highlightColor=setting['highlightColor'],
        language=setting['language'],
        fontSize=setting['fontSize'],
        showDetail=setting['showDetail'],
        collectedWords=setting['collectedWords'],
        suspendedPages=setting['suspendedPages'],
        updatedAt=ts,
    )


def formatSettingFromORM(dbSetting: SettingORM) -> Setting:
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
