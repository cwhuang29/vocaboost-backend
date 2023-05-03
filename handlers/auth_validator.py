from structs.schemas.oauth import AzureOAuthToken, GoogleOAuthToken
from structs.schemas.user import AzureUser, GoogleUser
from utils.enum import LoginMethodType
from utils.message import ERROR_MSG


def verifyGoogleLoginPayload(oauthToken: GoogleOAuthToken, user: GoogleUser):
    # if oauthToken.firstName != user.firstName:
    #     raise ValueError(ERROR_MSG.PAYLOAD_INCORRECT)
    # if oauthToken.lastName != user.lastName:
    #     raise ValueError(ERROR_MSG.PAYLOAD_INCORRECT)
    if oauthToken.email != user.email:
        raise ValueError(ERROR_MSG.PAYLOAD_INCORRECT)


def verifyAzureLoginPayload(oauthToken: AzureOAuthToken, user: AzureUser):
    if oauthToken.email != user.email:
        raise ValueError(ERROR_MSG.PAYLOAD_INCORRECT)


def verifyLoginPayload(oauthToken, user):
    if user.loginMethod == LoginMethodType.GOOGLE:
        verifyGoogleLoginPayload(oauthToken, user)
    if user.loginMethod == LoginMethodType.AZURE:
        verifyAzureLoginPayload(oauthToken, user)
