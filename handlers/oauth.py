from google.oauth2 import id_token
from google.auth.transport import requests
import jwt as pyJWT

from config import GOOGLE_LOGIN_IOS_CLIENT_ID
from formatter.oauth import formatAzureOAuthToken, formatGoogleOAuthToken
from structs.schemas.oauth import AzureOAuthToken, GoogleOAuthToken
from utils.enum import LoginMethodType
from utils.message import ERROR_MSG
from utils.oauth import isSupportLoginType
from utils.type import OAuthTokenType


def verifyLoginMethod(loginMethod: LoginMethodType):
    if not isSupportLoginType(loginMethod):
        raise ValueError(ERROR_MSG.LOGIN_NOT_SUPPORT)


def getUserIdentifierFromOAuthJWT(loginMethod: LoginMethodType, oauthToken: OAuthTokenType) -> str | None:
    if loginMethod == LoginMethodType.GOOGLE:
        return oauthToken.sub
    if loginMethod == LoginMethodType.AZURE:
        return oauthToken.oid
    return None


def getOAuthGoogleToken(idToken) -> GoogleOAuthToken:
    try:
        decoded = id_token.verify_oauth2_token(idToken, requests.Request(), GOOGLE_LOGIN_IOS_CLIENT_ID)
        oauthToken = formatGoogleOAuthToken(decoded)
    except Exception:
        raise ValueError(ERROR_MSG.OAUTH_TOKEN_MALFORMED)
    return oauthToken


def getOAuthAzureToken(idToken) -> AzureOAuthToken:
    try:
        # TODO Use Azure service to verify the ID Token issued by Azure's OAuth 2.0 authorization server
        decoded = pyJWT.decode(idToken, options={'verify_signature': False})
        oauthToken = formatAzureOAuthToken(decoded)
    except Exception:
        raise ValueError(ERROR_MSG.OAUTH_TOKEN_MALFORMED)
    return oauthToken


def getOAuthToken(loginMethod: LoginMethodType, idToken: str) -> OAuthTokenType:
    oauthToken = None
    if loginMethod == LoginMethodType.GOOGLE:
        oauthToken = getOAuthGoogleToken(idToken)
    if loginMethod == LoginMethodType.AZURE:
        oauthToken = getOAuthAzureToken(idToken)
    return oauthToken
