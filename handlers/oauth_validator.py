from google.oauth2 import id_token
from google.auth.transport import requests

from config import GOOGLE_LOGIN_IOS_CLIENT_ID
from formatter.oauth import formatGoogleOauthToken
from structs.schemas.oauth import GoogleOAuthToken
from utils.constant import OAUTH_GOOGLE_ISS
from utils.enum import LoginMethodType
from utils.message import ERROR_MSG


def getOAuthGoogleToken(idToken):
    try:
        idInfo = id_token.verify_oauth2_token(idToken, requests.Request(), GOOGLE_LOGIN_IOS_CLIENT_ID)
        oauthToken = formatGoogleOauthToken(idInfo)
    except Exception:
        raise ValueError(ERROR_MSG.OAUTH_TOKEN_MALFORMED)
    return oauthToken


def getOAuthToken(loginMethod: LoginMethodType, idToken: str):
    oauthToken = None
    if loginMethod == LoginMethodType.GOOGLE:
        oauthToken = getOAuthGoogleToken(idToken)
    else:
        raise ValueError(ERROR_MSG.LOGIN_NOT_SUPPORT)
    return oauthToken


def verifyOAuthGoogleToken(oauthToken: GoogleOAuthToken):
    if oauthToken.aud != GOOGLE_LOGIN_IOS_CLIENT_ID:
        raise ValueError(ERROR_MSG.OAUTH_TOKEN_INVALID)
    if oauthToken.iss not in OAUTH_GOOGLE_ISS:
        raise ValueError(ERROR_MSG.OAUTH_TOKEN_INVALID)


def verifyOAuthToken(loginMethod: LoginMethodType, oauthToken):
    if loginMethod == LoginMethodType.GOOGLE:
        oauthToken = verifyOAuthGoogleToken(oauthToken)
    else:
        raise ValueError(ERROR_MSG.LOGIN_NOT_SUPPORT)
