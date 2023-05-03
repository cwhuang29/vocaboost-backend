from datetime import datetime
from structs.models.auth import AuthHistoryORM
from structs.models.user import AzureUserORM, GoogleUserORM, UserORM
from structs.schemas.user import AzureUser, GoogleUser, User
from utils.enum import ClientSourceType, AuthHistoryType, LoginMethodType
from utils.type import DetailedUserType


def getGoogleUserORM(user: GoogleUser, id: int) -> GoogleUserORM:
    return GoogleUserORM(
        userId=id,
        accountId=user.accountId,
        email=user.email,
        scopes=user.scopes,
        avatar=user.avatar,
    )


def getAzureUserORM(user: AzureUser, id: int) -> AzureUserORM:
    return AzureUserORM(
        userId=id,
        accountId=user.accountId,
        email=user.email,
        scopes=user.scopes,
        avatar=user.avatar,
    )


def getDetailedUserORM(user: DetailedUserType, id: int):
    dbDetailedUser = None
    if user.loginMethod == LoginMethodType.GOOGLE:
        dbDetailedUser = getGoogleUserORM(user, id)
    if user.loginMethod == LoginMethodType.AZURE:
        dbDetailedUser = getAzureUserORM(user, id)
    return dbDetailedUser


def getUserORM(user: User) -> UserORM:
    return UserORM(
        uuid=user.uuid,
        firstName=user.firstName,
        lastName=user.lastName,
        method=user.loginMethod.value,
        createdAt=user.createdAt,
    )


def getAuthHistoryORM(id: int, source: ClientSourceType, authType: AuthHistoryType):
    s = source.value if source != ClientSourceType.UNKNOWN else None
    return AuthHistoryORM(
        userId=id,
        source=s,
        action=authType.value,
        createdAt=datetime.utcnow()  # The default value set by sqlalchemy would be timezone-awared time
    )
