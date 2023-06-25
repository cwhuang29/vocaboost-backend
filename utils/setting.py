from dataclasses import dataclass, field
from datetime import datetime
from utils.enum import HIGHLIGHTER_BG_COLORS, FONT_SIZE, LANGS


@dataclass
class DefaultSetting:
    highlightColor: str = HIGHLIGHTER_BG_COLORS.YELLOW
    language: str = LANGS.en
    fontSize: str = FONT_SIZE.MEDIUM
    showDetail: bool = True
    collectedWords: list[int] = field(default_factory=list)
    suspendedPages: list[int] = field(default_factory=list)
    updatedAt: datetime = datetime(2000, 1, 1, 18, 0, 0)


DEFAULT_SETTING = DefaultSetting()
