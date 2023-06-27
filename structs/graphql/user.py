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
    createdAt: datetime
    updatedAt: Optional[datetime]

    @strawberry.field
    def fullName(self) -> str:
        return f"{self.firstName} {self.lastName}"


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
