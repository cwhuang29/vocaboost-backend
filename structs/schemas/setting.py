from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, conint, constr


class Setting(BaseModel):
    userId: conint(ge=0)
    highlightColor: Optional[constr(max_length=20)]
    language: Optional[constr(max_length=20)]
    fontSize: Optional[constr(max_length=20)]
    showDetail: Optional[bool]
    collectedWords: Optional[List[int]]
    suspendedPages: Optional[List[str]]
    updatedAt: Optional[datetime] = None

    class Config:
        orm_mode = True
