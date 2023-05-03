from enum import Enum
from functools import partial


class ERROR_MSG(str, Enum):
    GENERAL_ERR = 'Error'
    UNEXPECTED_ERR = 'Oops, this is unexpected'

    PERMISSION_DENIED = 'You are not allowed to perform this action'

    PAYLOAD_INCORRECT = 'Your request data is not valid'

    TRY_AGAIN = 'Please try again'
    RELOAD_AND_RETRY = 'Please reload the page and try again'
    GO_BACK_AND_RETRY = 'Go back to previous page and try again'
    TRY_TOO_OFTEN = 'You are trying too often'

    DATABASE_ERR = 'An error occurred while writing to DB'

    HEADER_INVALID = 'Header verify failed'

    OAUTH_TOKEN_MALFORMED = 'OAuth token is malformed'
    OAUTH_TOKEN_INVALID = 'Cannot verify OAuth token'

    JWT_ERROR_MALFORMED = 'Token is malformed'
    JWT_ERROR_UNVERIFIABLE = 'Token could not be verified because of signing problems'
    JWT_ERROR_SIGNATURE_INVALID = 'Signature validation failed'
    JWT_ERROR_EXPIRED = 'Login session expired. You have to relogin'  # Token is expired
    JWT_ERROR_NOT_VALID_YET = 'Token is not yet valid before sometime'
    JWT_PAYLOAD_MALFORMED = 'You have to relogin'
    JWT_UNKNOWN = 'Can not handle this token'

    LOGIN_FIRST = 'You should login first'
    LOGIN_NOT_SUPPORT = 'Login type is not supported'

    UPDATE_CONFLICT = 'The data here is outdated, it has been updated'


def getErrMsg(errHead=ERROR_MSG.UNEXPECTED_ERR, errBody='') -> dict:
    return {'errHead': errHead, 'errBody': errBody}


getUnexpectedErrMsg = partial(getErrMsg, ERROR_MSG.UNEXPECTED_ERR, ERROR_MSG.TRY_AGAIN)

getLoginNotSupportMsg = partial(getErrMsg, ERROR_MSG.LOGIN_NOT_SUPPORT)

getNoSourceHeaderMsg = partial(getErrMsg, ERROR_MSG.HEADER_INVALID)

getShouldLoginMsg = partial(getErrMsg, ERROR_MSG.PERMISSION_DENIED, ERROR_MSG.LOGIN_FIRST)
