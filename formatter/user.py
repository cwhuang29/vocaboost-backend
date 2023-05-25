from datetime import datetime
from structs.models.user import AzureUserORM, GoogleUserORM, UserORM
from structs.requests.auth import ReqLogin
from structs.schemas.user import AzureUser, AzureUserOut, GoogleUser, GoogleUserOut, User
from utils.enum import LoginMethodType
from utils.type import DetailedUserOutType


def formatDisplayGoogleUserFromORM(dbUser: UserORM, dbDetailedUser: GoogleUserORM) -> GoogleUserOut:
    return GoogleUserOut(
        uuid=dbUser.uuid,
        firstName=dbUser.firstName,
        lastName=dbUser.lastName,
        createdAt=dbUser.createdAt,
        email=dbDetailedUser.email,
        avatar=dbDetailedUser.avatar,
    )


def formatDisplayAzureUserFromORM(dbUser: UserORM, dbDetailedUser: AzureUserORM) -> AzureUserOut:
    return AzureUserOut(
        uuid=dbUser.uuid,
        firstName=dbUser.firstName,
        lastName=dbUser.lastName,
        createdAt=dbUser.createdAt,
        email=dbDetailedUser.email,
        avatar=dbDetailedUser.avatar,
    )


def formatDisplayedUserFromORM(dbUser: UserORM, dbDetailedUser) -> DetailedUserOutType:
    user = None
    if LoginMethodType(dbUser.method) == LoginMethodType.GOOGLE:
        user = formatDisplayGoogleUserFromORM(dbUser, dbDetailedUser)
    if LoginMethodType(dbUser.method) == LoginMethodType.AZURE:
        user = formatDisplayAzureUserFromORM(dbUser, dbDetailedUser)
    return user


def formatUserFromReq(reqLogin: ReqLogin) -> User:
    return User(
        loginMethod=reqLogin.loginMethod,
        firstName=reqLogin.detail.firstName,
        lastName=reqLogin.detail.lastName,
        createdAt=reqLogin.timeStamp or datetime.utcnow()
    )


def formatGoogleUserFromReq(reqLogin: ReqLogin, accountId: str) -> GoogleUser:
    return GoogleUser(
        accountId=accountId,
        loginMethod=reqLogin.loginMethod,
        firstName=reqLogin.detail.firstName,
        lastName=reqLogin.detail.lastName,
        email=reqLogin.detail.email,
        scopes=reqLogin.detail.scopes,
        avatar=reqLogin.detail.avatar,
        createdAt=reqLogin.timeStamp or datetime.utcnow(),
    )


def formatAzureUserFromReq(reqLogin: ReqLogin, accountId: str) -> AzureUser:
    return AzureUser(
        accountId=accountId,
        loginMethod=reqLogin.loginMethod,
        firstName=reqLogin.detail.firstName,
        lastName=reqLogin.detail.lastName,
        email=reqLogin.detail.email,
        scopes=reqLogin.detail.scopes,
        avatar=reqLogin.detail.avatar,
        createdAt=reqLogin.timeStamp or datetime.utcnow(),
    )
