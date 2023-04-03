from structs.models.setting import SettingORM
from structs.schemas.setting import Setting


def getSettingORM(setting: Setting) -> SettingORM:
    return SettingORM(
        user_id=setting.userId,
        highlight_color=setting.highlightColor,
        language=setting.language,
        font_size=setting.fontSize,
        show_detail=1 if setting.showDetail else 0,
        collected_words=str(setting.collectedWords),
        suspended_pages=str(setting.suspendedPages),
    )
