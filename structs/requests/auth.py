from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from utils.enum import LoginMethodType


class ReqLoginDetail(BaseModel):
    email: str
    firstName: str
    lastName: str
    scopes: str
    avatar: str


class ReqLogin(BaseModel):
    loginMethod: LoginMethodType
    idToken: Optional[str]   # App login
    accountId: Optional[str]  # Ext login
    detail: ReqLoginDetail
    timeStamp: Optional[datetime]
