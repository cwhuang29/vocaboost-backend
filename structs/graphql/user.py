from datetime import datetime
from typing import Optional

import strawberry


@strawberry.type(description='User class')
class User:
    id: int
    uuid: str
    firstName: str
    lastName: str
    method: int
    createdAt: Optional[datetime]
    updatedAt: Optional[datetime]


@strawberry.type(description='GoogleUser class')
class GoogleUser:
    userId: int
    accountId: str
    scopes: Optional[str]
    email: str
    avatar: str


@strawberry.type(description='AzureUser class')
class AzureUser:
    userId: int
    accountId: str
    scopes: Optional[str]
    email: str
    avatar: str


DetailedUser = GoogleUser | AzureUser


@strawberry.type(description='User displayed class')
class UserOut:
    uuid: str
    loginMethod: int
    firstName: str
    lastName: Optional[str]
    createdAt: Optional[datetime]
    email: Optional[str]
    avatar: Optional[str]

    @strawberry.field
    def fullName(self) -> str:
        return f"{self.firstName} {self.lastName}"
