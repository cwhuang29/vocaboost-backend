from structs.schemas.oauth import GoogleOAuthToken
from structs.schemas.user import GoogleUser
from utils.enum import LoginMethodType
from utils.message import ERROR_MSG


def verifyGoogleLoginPayload(oauthToken: GoogleOAuthToken, user: GoogleUser):
    # if oauthToken.firstName != user.firstName:
    #     raise ValueError(ERROR_MSG.PAYLOAD_INCORRECT)
    # if oauthToken.lastName != user.lastName:
    #     raise ValueError(ERROR_MSG.PAYLOAD_INCORRECT)
    if oauthToken.email != user.email:
        raise ValueError(ERROR_MSG.PAYLOAD_INCORRECT)


def verifyLoginPayload(oauthToken, user):
    if user.loginMethod == LoginMethodType.GOOGLE:
        verifyGoogleLoginPayload(oauthToken, user)
    else:
        raise ValueError(ERROR_MSG.LOGIN_NOT_SUPPORT)
