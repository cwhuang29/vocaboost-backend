from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel

from utils.enum import LoginMethodType


class ReqLoginDetail(BaseModel):
    email: str
    firstName: str
    lastName: str
    scopes: str
    serverAuthCode: Optional[str] = None
    avatar: str


class ReqLogin(BaseModel):
    uuid: Optional[UUID4]
    loginMethod: LoginMethodType
    detail: ReqLoginDetail
    timeStamp: datetime
