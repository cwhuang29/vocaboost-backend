from utils.enum import LoginMethodType


supportLoginType = [LoginMethodType.GOOGLE, LoginMethodType.AZURE]


def isSupportLoginType(loginMethod: LoginMethodType) -> bool:
    return loginMethod in supportLoginType
