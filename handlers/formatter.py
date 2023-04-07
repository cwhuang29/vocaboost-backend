import ast
from datetime import datetime

from structs.models.setting import SettingORM
from structs.models.user import GoogleUserORM, UserORM
from structs.requests.auth import ReqLogin
from structs.schemas.setting import Setting
from structs.schemas.user import GoogleUser, GoogleUserOut, User
from utils.enum import LoginMethodType
from utils.setting import DEFAULT_SETTING


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


def formatGoogleUserFromReq(reqLogin: ReqLogin) -> GoogleUser:
    return GoogleUser(
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
        updatedAt=DEFAULT_SETTING['updatedAt'],
    )


def formatSettingFromWS(setting: dict, userId: int, ts: datetime) -> Setting:
    return Setting(
        userId=userId,
        highlightColor=setting['highlightColor'],
        language=setting['language'],
        fontSize=setting['fontSize'],
        showDetail=setting['showDetail'],
        collectedWords=setting['collectedWords'],
        suspendedPages=setting['suspendedPages'],
        updatedAt=ts,
    )


def formatSettingFromORM(dbSetting: SettingORM) -> Setting:
    return Setting(
        userId=dbSetting.userId,
        highlightColor=dbSetting.highlightColor,
        language=dbSetting.language,
        fontSize=dbSetting.fontSize,
        showDetail=True if dbSetting.showDetail == 1 else False,
        collectedWords=ast.literal_eval(dbSetting.collectedWords),
        suspendedPages=ast.literal_eval(dbSetting.suspendedPages),
        updatedAt=dbSetting.updatedAt,
    )
