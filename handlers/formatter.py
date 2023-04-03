import uuid

from structs.models.user import GoogleUserORM, UserORM
from structs.requests.auth import ReqLogin
from structs.schemas.setting import Setting
from structs.schemas.user import GoogleUser, GoogleUserOut, User
from utils.enum import LoginMethodType
from utils.setting import DEFAULT_SETTING


def formatGoogleUserFromORM(dbUser: UserORM, dbDetailedUser: GoogleUserORM) -> GoogleUser:
    return GoogleUserOut(
        uuid=dbUser.uuid,
        firstName=dbUser.first_name,
        lastName=dbUser.last_name,
        createdAt=dbUser.created_at,
        email=dbDetailedUser.email,
        avatar=dbDetailedUser.avatar,
    )


def formatUserFromORM(dbUser: UserORM, dbDetailedUser) -> User:
    user = None
    if LoginMethodType(dbUser.method) == LoginMethodType.GOOGLE:
        user = formatGoogleUserFromORM(dbUser, dbDetailedUser)
    return user


def formatUserFromReq(reqLogin: ReqLogin) -> User:
    uid = reqLogin.uuid or uuid.uuid4()
    return User(
        uuid=uid,
        loginMethod=reqLogin.loginMethod,
        firstName=reqLogin.detail.firstName,
        lastName=reqLogin.detail.lastName,
        createdAt=reqLogin.timeStamp
    )


def formatGoogleUserFromReq(reqLogin: ReqLogin) -> GoogleUser:
    uid = reqLogin.uuid or uuid.uuid4()
    return GoogleUser(
        uuid=uid,
        loginMethod=reqLogin.loginMethod,
        firstName=reqLogin.detail.firstName,
        lastName=reqLogin.detail.lastName,
        createdAt=reqLogin.timeStamp,
        email=reqLogin.detail.email,
        scopes=reqLogin.detail.scopes,
        serverAuthCode=reqLogin.detail.serverAuthCode,
        avatar=reqLogin.detail.avatar,
    )


def formatDefaultSetting(userId: int) -> Setting:
    return Setting(
        userId=userId,
        highlightColor=DEFAULT_SETTING['highlightColor'],
        language=DEFAULT_SETTING['language'],
        fontSize=DEFAULT_SETTING['fontSize'],
        showDetail=DEFAULT_SETTING['showDetail'],
        collectedWords=DEFAULT_SETTING['collectedWords'],
        suspendedPages=DEFAULT_SETTING['suspendedPages'],
    )