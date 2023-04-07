from datetime import datetime
from structs.models.auth import AuthHistoryORM
from structs.models.user import GoogleUserORM, UserORM
from structs.schemas.user import GoogleUser, User
from utils.enum import ClientSourceType, AuthHistoryType, LoginMethodType


def getGoogleUserORM(user: GoogleUser, id: int) -> GoogleUserORM:
    return GoogleUserORM(
        userId=id,
        email=user.email,
        scopes=user.scopes,
        serverAuthCode=user.serverAuthCode,
        avatar=user.avatar,
    )


def getDetailedUserORM(user: User, id: int):
    dbDetailedUser = None
    if user.loginMethod == LoginMethodType.GOOGLE:
        dbDetailedUser = getGoogleUserORM(user, id)
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
