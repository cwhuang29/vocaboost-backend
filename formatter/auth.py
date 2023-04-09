from structs.schemas.auth import TokenData


def createTokenData(uuid: str, method: int, firstName: str, lastName: str, email: str | None = '') -> TokenData:
    return TokenData(
        uuid=uuid,
        method=method,
        firstName=firstName,
        lastName=lastName,
        email=email
    )
