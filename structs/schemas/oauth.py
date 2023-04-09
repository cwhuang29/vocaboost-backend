from typing import Optional

from pydantic import BaseModel


class GoogleOAuthToken(BaseModel):
    iss: Optional[str] = None  # Should equal to accounts.google.com or https://accounts.google.com
    aud: Optional[str] = None  # App's client ID
    sub: Optional[str] = None  # User account ID
    email: Optional[str] = None
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    avatar: Optional[str] = None
    exp: Optional[str] = None

    class Config:
        orm_mode = True


'''
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
'''
