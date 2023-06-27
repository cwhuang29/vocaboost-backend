from datetime import datetime
from typing import List, Optional

import strawberry


@strawberry.type(description='User stting class')
class Setting:
    userId: int
    highlightColor: str
    language: str
    fontSize: str
    showDetail: bool
    collectedWords: List[int]
    suspendedPages: List[str]
    updatedAt: Optional[datetime]
