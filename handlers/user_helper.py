import ast

from structs.schemas.setting import Setting
from structs.models.setting import SettingORM


def getSettingFromORM(dbSetting: SettingORM) -> Setting:
    return Setting(
        userId=dbSetting.user_id,
        highlightColor=dbSetting.highlight_color,
        language=dbSetting.language,
        fontSize=dbSetting.font_size,
        showDetail=True if dbSetting.show_detail == 1 else False,
        collectedWords=ast.literal_eval(dbSetting.collected_words),
        suspendedPages=ast.literal_eval(dbSetting.suspended_pages),
        updatedAt=dbSetting.updated_at,
    )
