from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from utils.enum import LoginMethodType


class ReqLoginDetail(BaseModel):
    email: str
    firstName: str
    lastName: Optional[str]
    scopes: str
    avatar: str


class ReqLogin(BaseModel):
    loginMethod: LoginMethodType
    idToken: str
    detail: ReqLoginDetail
    timeStamp: Optional[datetime]

    def __repr__(self):
        return f'{self.__module__}-{type(self).__qualname__}-{self.loginMethod}-{self.detail.email}'
