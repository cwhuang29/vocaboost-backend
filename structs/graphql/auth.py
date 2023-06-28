from typing import Optional

import strawberry


@strawberry.type(description='Token data class')
class TokenData:
    uuid: str
    method: int
    firstName: str
    lastName: str
    email: Optional[str]
