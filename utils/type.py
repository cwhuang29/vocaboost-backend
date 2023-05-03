from typing import Union

from structs.models.user import AzureUserORM, GoogleUserORM
from structs.schemas.oauth import AzureOAuthToken, GoogleOAuthToken
from structs.schemas.user import AzureUser, AzureUserOut, GoogleUser, GoogleUserOut


OauthTokenTypeAll = Union[GoogleOAuthToken, AzureOAuthToken]

DetailedUserTypeAll = Union[GoogleUser, AzureUser]

DetailedUserOutTypeAll = Union[GoogleUserOut, AzureUserOut]

DetailedUserORMTypeAll = Union[GoogleUserORM, AzureUserORM]
