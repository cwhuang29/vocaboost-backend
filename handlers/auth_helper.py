import uuid

from structs.requests.auth import ReqLogin
from structs.schemas.user import GoogleUser, User


def getUserFromReq(reqLogin: ReqLogin) -> User:
    return User(
        uuid=uuid.uuid4(),
        loginMethod=reqLogin.loginMethod,
        firstName=reqLogin.detail.firstName,
        lastName=reqLogin.detail.lastName,
        createdAt=reqLogin.timeStamp
    )


def getGoogleUserFromReq(reqLogin: ReqLogin) -> GoogleUser:
    return GoogleUser(
        uuid=uuid.uuid4(),
        loginMethod=reqLogin.loginMethod,
        firstName=reqLogin.detail.firstName,
        lastName=reqLogin.detail.lastName,
        createdAt=reqLogin.timeStamp,
        email=reqLogin.detail.email,
        scopes=reqLogin.detail.scopes,
        serverAuthCode=reqLogin.detail.serverAuthCode,
        avatar=reqLogin.detail.avatar,
    )
