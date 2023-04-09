from structs.schemas.oauth import GoogleOAuthToken


def formatGoogleOauthToken(idInfo) -> GoogleOAuthToken:
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
