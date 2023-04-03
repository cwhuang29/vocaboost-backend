from structs.models.auth import AuthHistoryORM
from structs.models.user import GoogleUserORM, UserORM
from structs.schemas.user import GoogleUser, User
from utils.enum import AuthHistoryType, LoginMethodType


def getGoogleUserORM(user: GoogleUser, id: int) -> GoogleUserORM:
    return GoogleUserORM(
        user_id=id,
        email=user.email,
        scopes=user.scopes,
        server_auth_code=user.serverAuthCode,
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
        first_name=user.firstName,
        last_name=user.lastName,
        method=user.loginMethod.value,
        created_at=user.createdAt,
    )


def getAuthHistoryORM(id: int, authType: AuthHistoryType):
    return AuthHistoryORM(
        user_id=id,
        action=authType.value
    )
