from structs.models.user import GoogleUserORM, UserORM
from structs.requests.auth import ReqLogin
from structs.schemas.user import GoogleUser, GoogleUserOut, User
from utils.enum import LoginMethodType


def formatGoogleUserFromORM(dbUser: UserORM, dbDetailedUser: GoogleUserORM) -> GoogleUserOut:
    return GoogleUserOut(
        uuid=dbUser.uuid,
        firstName=dbUser.firstName,
        lastName=dbUser.lastName,
        createdAt=dbUser.createdAt,
        email=dbDetailedUser.email,
        avatar=dbDetailedUser.avatar,
    )


def formatUserFromORM(dbUser: UserORM, dbDetailedUser):
    user = None
    if LoginMethodType(dbUser.method) == LoginMethodType.GOOGLE:
        user = formatGoogleUserFromORM(dbUser, dbDetailedUser)
    return user


def formatUserFromReq(reqLogin: ReqLogin) -> User:
    return User(
        loginMethod=reqLogin.loginMethod,
        firstName=reqLogin.detail.firstName,
        lastName=reqLogin.detail.lastName,
        createdAt=reqLogin.timeStamp
    )


def formatGoogleUserFromReq(reqLogin: ReqLogin, accountId: str) -> GoogleUser:
    return GoogleUser(
        loginMethod=reqLogin.loginMethod,
        firstName=reqLogin.detail.firstName,
        lastName=reqLogin.detail.lastName,
        createdAt=reqLogin.timeStamp,
        accountId=accountId,
        email=reqLogin.detail.email,
        scopes=reqLogin.detail.scopes,
        avatar=reqLogin.detail.avatar,
    )
