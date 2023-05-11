from pydantic import BaseModel


class GoogleOAuthToken(BaseModel):
    iss: str = None  # Should equal to accounts.google.com or https://accounts.google.com
    aud: str = None  # App's client ID
    sub: str = None  # User account ID
    email: str = None
    firstName: str = None
    lastName: str = None
    avatar: str = None
    exp: int = None

    class Config:
        orm_mode = True


class AzureOAuthToken(BaseModel):
    ver: str = None
    iss: str = None
    sub: str = None  # Uniquely identify an user
    aud: str = None
    exp: int = None
    oid: str = None  # Uniquely identify an user
    email: str = None
    firstName: str = None
    lastName: str = None

    class Config:
        orm_mode = True


'''
GoogleOAuthToken
{
  'iss': '',
  'azp': '',
  'aud': '',
  'sub': '',
  'email': '',
  'email_verified': True,
  'at_hash': '',
  'nonce': '',
  'name': '',
  'picture': '',
  'given_name': '',
  'family_name': '',
  'locale': 'en-GB',
  'iat': <int>,
  'exp': 1680942064
}

AzureOAuthToken. See https://learn.microsoft.com/en-us/azure/active-directory/develop/id-tokens
Use oid to uniquely identify a user. See https://learn.microsoft.com/en-us/azure/active-directory/develop/id-tokens#using-claims-to-reliably-identify-a-user-subject-and-object-id
{
  ver: '2.0',
  iss: 'https://login.microsoftonline.com/.../v2.0',
  sub: '',
  aud: '', // should match client id
  exp: 1683064565,
  iat: 1682977865,
  nbf: 1682977865,
  name: '',
  preferred_username: '',
  oid: '',
  email: '',
  tid: '',
  family_name: '',
  given_name: '',
  aio: '',
}
'''
