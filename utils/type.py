from typing import Union

from structs.models.user import AzureUserORM, GoogleUserORM
from structs.schemas.oauth import AzureOAuthToken, GoogleOAuthToken
from structs.schemas.user import AzureUser, AzureUserOut, GoogleUser, GoogleUserOut


OAuthTokenType = Union[GoogleOAuthToken, AzureOAuthToken]

DetailedUserType = Union[GoogleUser, AzureUser]

DetailedUserOutType = Union[GoogleUserOut, AzureUserOut]

DetailedUserORMType = Union[GoogleUserORM, AzureUserORM]
