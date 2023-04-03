from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from utils.enum import LoginMethodType


class ReqLoginDetail(BaseModel):
    email: str
    firstName: str
    lastName: str
    scopes: str
    serverAuthCode: Optional[str] = None
    avatar: str


class ReqLogin(BaseModel):
    loginMethod: LoginMethodType
    detail: ReqLoginDetail
    timeStamp: datetime
