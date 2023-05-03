from structs.schemas.oauth import AzureOAuthToken, GoogleOAuthToken


def formatGoogleOAuthToken(idInfo) -> GoogleOAuthToken:
    return GoogleOAuthToken(
        iss=idInfo['iss'],
        aud=idInfo['aud'],
        sub=idInfo['sub'],
        email=idInfo['email'],
        firstName=idInfo['given_name'],
        lastName=idInfo['family_name'],
        avatar=idInfo['picture'],
        exp=idInfo['exp'],
    )


def formatAzureOAuthToken(idInfo) -> AzureOAuthToken:
    return AzureOAuthToken(
        ver=idInfo['ver'],
        iss=idInfo['iss'],
        sub=idInfo['sub'],
        aud=idInfo['aud'],
        exp=idInfo['exp'],
        oid=idInfo['oid'],
        email=idInfo['email'],
        firstName=idInfo['given_name'],
        lastName=idInfo['family_name'],
    )
