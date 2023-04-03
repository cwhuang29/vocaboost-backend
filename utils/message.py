from enum import Enum


class HTTP_ERROR_MSG(str, Enum):
    CREDENTIAL_MISS = 'Could not validate credentials'
    LOGIN_FIRST = 'You should login first'
    LOGIN_NOT_SUPPORT = 'Login type is not supported'
