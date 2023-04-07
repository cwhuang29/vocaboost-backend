from pydantic import BaseModel


class Token(BaseModel):
    accessToken: str
    tokenType: str


class TokenData(BaseModel):
    uuid: str | None = None
    method: int | None = None
    firstName: str | None = None
    lastName: str | None = None
    email: str | None = None


class LoginOut(BaseModel):
    token: Token
    isNewUser: bool
