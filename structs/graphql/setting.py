from datetime import datetime
from typing import List, Optional

import strawberry


@strawberry.type(description='User setting class')
class Setting:
    userId: int
    highlightColor: str
    language: str
    fontSize: str
    showDetail: bool
    collectedWords: List[int]
    suspendedPages: List[str]
    updatedAt: Optional[datetime]


@strawberry.type(description='User setting displayed class')
class SettingOut:
    highlightColor: str
    language: str
    fontSize: str
    showDetail: bool
    collectedWords: List[int]
    suspendedPages: List[str]
    updatedAt: Optional[datetime]
