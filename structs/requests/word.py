from datetime import datetime
from typing import Union

from pydantic import BaseModel

from utils.enum import ManageWordType


class ReqManageWord(BaseModel):
    userId: int
    wordId: int
    action: ManageWordType
    UpdatedAt: Union[datetime, None] = None
