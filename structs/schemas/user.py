from datetime import datetime
from typing import Optional

from pydantic import UUID4, BaseModel, EmailStr, conint, constr

from utils.enum import LoginMethodType


class User(BaseModel):
    uuid: Optional[UUID4]
    loginMethod: LoginMethodType
    firstName: constr(max_length=100)
    lastName: Optional[constr(max_length=100)]
    createdAt: Optional[datetime]

    class Config:
        orm_mode = True


class GoogleUser(User):
    loginMethod = LoginMethodType.GOOGLE
    userId: Optional[conint(ge=0)]
    accountId: str  # Uniquely identify a google account
    email: EmailStr
    scopes: constr(max_length=1000)
    avatar: constr(max_length=600)

    class Config:
        orm_mode = True


class AzureUser(User):
    loginMethod = LoginMethodType.AZURE
    userId: Optional[conint(ge=0)]
    accountId: str  # Uniquely identify a microsoft account
    email: EmailStr
    scopes: constr(max_length=1000)
    avatar: str  # Base64 encoding string

    class Config:
        orm_mode = True


# Contain only values that should be displayed on the client
class UserOut(BaseModel):
    uuid: Optional[UUID4]
    loginMethod: LoginMethodType
    firstName: constr(max_length=100)
    lastName: Optional[constr(max_length=100)]
    createdAt: datetime

    class Config:
        orm_mode = True


class GoogleUserOut(UserOut):
    loginMethod = LoginMethodType.GOOGLE
    email: EmailStr
    avatar: constr(max_length=600)


class AzureUserOut(UserOut):
    loginMethod = LoginMethodType.AZURE
    email: EmailStr
    avatar: str
