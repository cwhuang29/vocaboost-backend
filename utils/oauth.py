from config import GOOGLE_LOGIN_ANDROID_CLIENT_ID, GOOGLE_LOGIN_IOS_CLIENT_ID, GOOGLE_LOGIN_WEB_CLIENT_ID
from utils.enum import ClientSourceType, DevicePlatformType, LoginMethodType


supportLoginType = [LoginMethodType.GOOGLE, LoginMethodType.AZURE]


def isSupportLoginType(loginMethod: LoginMethodType) -> bool:
    return loginMethod in supportLoginType


def getGoogleOAuthClientID(source: ClientSourceType, platform: DevicePlatformType) -> str:
    if source == ClientSourceType.EXTENSION:
        return GOOGLE_LOGIN_WEB_CLIENT_ID

    if source == ClientSourceType.MOBILE:
        if platform == DevicePlatformType.ANDROID:
            return GOOGLE_LOGIN_ANDROID_CLIENT_ID

        if platform == DevicePlatformType.IOS:
            return GOOGLE_LOGIN_IOS_CLIENT_ID

    return ''
