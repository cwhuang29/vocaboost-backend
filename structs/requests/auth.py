from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from utils.enum import LoginMethodType


class ReqLoginDetail(BaseModel):
    email: str
    firstName: str
    lastName: str
    scopes: str
    serverAuthCode: str
    avatar: str


class ReqLogin(BaseModel):
    uuid: Optional[str]
    loginMethod: LoginMethodType
    detail: ReqLoginDetail
    timeStamp: datetime


class ReqLogout(BaseModel):
    uuid: str
