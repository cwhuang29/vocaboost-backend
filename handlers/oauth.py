from datetime import datetime
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt as pyJWT

from config import AZURE_LOGIN_CLIENT_ID, GOOGLE_LOGIN_IOS_CLIENT_ID
from formatter.oauth import formatAzureOauthToken, formatGoogleOauthToken
from structs.schemas.oauth import AzureOAuthToken, GoogleOAuthToken
from utils.constant import OAUTH_AZURE_ISS, OAUTH_AZURE_VER, OAUTH_GOOGLE_ISS
from utils.enum import LoginMethodType
from utils.message import ERROR_MSG
from utils.oauth import isSupportLoginType
from utils.type import OauthTokenTypeAll


def verifyLoginMethod(loginMethod: LoginMethodType):
    if not isSupportLoginType(loginMethod):
        raise ValueError(ERROR_MSG.LOGIN_NOT_SUPPORT)


def getUserIdentifierFromOauthJWT(loginMethod: LoginMethodType, oauthToken: OauthTokenTypeAll) -> str | None:
    if loginMethod == LoginMethodType.GOOGLE:
        return oauthToken.sub
    if loginMethod == LoginMethodType.AZURE:
        return oauthToken.oid
    return None


def getOAuthGoogleToken(idToken) -> GoogleOAuthToken:
    try:
        decoded = id_token.verify_oauth2_token(idToken, requests.Request(), GOOGLE_LOGIN_IOS_CLIENT_ID)
        oauthToken = formatGoogleOauthToken(decoded)
    except Exception:
        raise ValueError(ERROR_MSG.OAUTH_TOKEN_MALFORMED)
    return oauthToken


def getOAuthAzureToken(idToken) -> AzureOAuthToken:
    try:
        # TODO Use Azure service to verify the ID Token issued by Azure's OAuth 2.0 authorization server
        decoded = pyJWT.decode(idToken, options={'verify_signature': False})
        oauthToken = formatAzureOauthToken(decoded)
    except Exception:
        raise ValueError(ERROR_MSG.OAUTH_TOKEN_MALFORMED)
    return oauthToken


def getOAuthToken(loginMethod: LoginMethodType, idToken: str) -> OauthTokenTypeAll:
    oauthToken = None
    if loginMethod == LoginMethodType.GOOGLE:
        oauthToken = getOAuthGoogleToken(idToken)
    if loginMethod == LoginMethodType.AZURE:
        oauthToken = getOAuthAzureToken(idToken)
    return oauthToken


def verifyOAuthGoogleToken(oauthToken: GoogleOAuthToken):
    err = ValueError(ERROR_MSG.OAUTH_TOKEN_INVALID)
    if oauthToken.aud != GOOGLE_LOGIN_IOS_CLIENT_ID:
        raise err
    if oauthToken.iss not in OAUTH_GOOGLE_ISS:
        raise err
    if not oauthToken.sub:
        raise err
    # No need to verify exp here since we have passed it to google oauth verification api
    # if oauthToken.exp < datetime.now().timestamp():  # Not utcnow()
    #     raise err


def verifyOAuthAzureToken(oauthToken: AzureOAuthToken):
    err = ValueError(ERROR_MSG.OAUTH_TOKEN_INVALID)
    if oauthToken.aud != AZURE_LOGIN_CLIENT_ID:
        raise err
    if not oauthToken.iss.startswith(OAUTH_AZURE_ISS):
        raise err
    if oauthToken.ver != OAUTH_AZURE_VER:
        raise err
    if not oauthToken.oid:
        raise err
    if oauthToken.exp < datetime.now().timestamp():  # Not utcnow()
        raise err


def verifyOAuthToken(loginMethod: LoginMethodType, oauthToken: OauthTokenTypeAll):
    if loginMethod == LoginMethodType.GOOGLE:
        verifyOAuthGoogleToken(oauthToken)
    if loginMethod == LoginMethodType.AZURE:
        verifyOAuthAzureToken(oauthToken)
