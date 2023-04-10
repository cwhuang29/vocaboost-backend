from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, conint, constr


class Setting(BaseModel):
    userId: Optional[conint(ge=0)]
    highlightColor: Optional[constr(max_length=20)]
    language: constr(max_length=20)
    fontSize: constr(max_length=20)
    showDetail: Optional[bool]
    collectedWords: List[int]
    suspendedPages: Optional[List[str]]
    updatedAt: datetime = None

    class Config:
        orm_mode = True


class UpdateSettingOut(BaseModel):
    data: Optional[Setting] = None
    isStale: Optional[bool] = None
    error: Optional[str] = None


class UpdateCollectedWordsOut(BaseModel):
    data: Optional[List[int]] = None
    ts: Optional[datetime] = None
    isStale: Optional[bool] = None
    error: Optional[str] = None
