from fastapi import HTTPException, status

from utils.message import ERROR_MSG, getErrMsg, getShouldLoginMsg


HTTP_CREDENTIALS_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=getShouldLoginMsg(),
    headers={'WWW-Authenticate': 'Bearer'},
)

HTTP_PAYLOAD_MALFORMED_EXCEPTION = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail=getErrMsg(errHead=ERROR_MSG.PAYLOAD_INCORRECT, errBody=ERROR_MSG.TRY_AGAIN),
)


HTTP_SERVER_EXCEPTION = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=getErrMsg(errHead=ERROR_MSG.UNEXPECTED_ERR, errBody=ERROR_MSG.TRY_AGAIN),
)
