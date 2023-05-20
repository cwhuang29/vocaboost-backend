from azure_ad_verify_token import verify_jwt
from google.oauth2 import id_token
from google.auth.transport import requests
import jwt as pyJWT

from config import AZURE_ISSUER, AZURE_LOGIN_CLIENT_ID
from formatter.oauth import formatAzureOAuthToken, formatGoogleOAuthToken
from structs.schemas.oauth import AzureOAuthToken, GoogleOAuthToken
from utils.constant import OAUTH_AZURE_JWKS_URI
from utils.enum import ClientSourceType, DevicePlatformType, LoginMethodType
from utils.message import ERROR_MSG
from utils.oauth import getGoogleOAuthClientID
from utils.type import OAuthTokenType


def decodeUnverifiedJWT(token):
    decoded = pyJWT.decode(token, options={'verify_signature': False})
    return decoded


def getUserIdentifierFromIDToken(loginMethod: LoginMethodType, oauthToken: OAuthTokenType) -> str | None:
    if loginMethod == LoginMethodType.GOOGLE:
        return oauthToken.sub
    if loginMethod == LoginMethodType.AZURE:
        return oauthToken.oid
    return None


def decodeGoogleIDToken(idToken, source: ClientSourceType, platform: DevicePlatformType) -> GoogleOAuthToken:
    try:
        audience = getGoogleOAuthClientID(source, platform)
        decoded = id_token.verify_oauth2_token(idToken, requests.Request(), audience)
        oauthToken = formatGoogleOAuthToken(decoded)
    except Exception:
        raise ValueError(ERROR_MSG.OAUTH_TOKEN_MALFORMED)
    return oauthToken


def decodeAzureIDToken(idToken) -> AzureOAuthToken:
    try:
        decoded = verify_jwt(
            token=idToken,
            valid_audiences=[AZURE_LOGIN_CLIENT_ID],
            issuer=AZURE_ISSUER,
            jwks_uri=OAUTH_AZURE_JWKS_URI,
            verify=True,
        )
        oauthToken = formatAzureOAuthToken(decoded)
    except Exception:
        raise ValueError(ERROR_MSG.OAUTH_TOKEN_MALFORMED)
    return oauthToken


def getOAuthToken(idToken: str, loginMethod: LoginMethodType, source: ClientSourceType, platform: DevicePlatformType) -> OAuthTokenType:
    oauthToken = None
    if source == ClientSourceType.EXTENSION:
        if loginMethod == LoginMethodType.GOOGLE:
            oauthToken = decodeGoogleIDToken(idToken, source, platform)
        if loginMethod == LoginMethodType.AZURE:
            oauthToken = decodeAzureIDToken(idToken)
    else:
        if loginMethod == LoginMethodType.GOOGLE:
            oauthToken = decodeGoogleIDToken(idToken, source, platform)
        if loginMethod == LoginMethodType.AZURE:
            oauthToken = decodeAzureIDToken(idToken)
    return oauthToken
