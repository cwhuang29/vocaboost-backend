from typing import Annotated

from fastapi import HTTPException, Header

from utils.enum import CLIENT_SOURCE, ClientSourceType
from utils.message import getNoSourceHeaderMsg


def verifyHeader(x_vh_source: Annotated[str, Header()]):
    try:
        _ = CLIENT_SOURCE(x_vh_source)
    except Exception:
        raise HTTPException(status_code=400, detail=getNoSourceHeaderMsg())


def getSourceHeader(x_vh_source: Annotated[str, Header()]) -> ClientSourceType:
    source = ClientSourceType.UNKNOWN
    try:
        s = CLIENT_SOURCE(x_vh_source)
        if s == CLIENT_SOURCE.MOBILE:
            source = ClientSourceType.MOBILE
        if s == CLIENT_SOURCE.EXTENSION:
            source = ClientSourceType.EXTENSION
    except Exception:
        pass
    return source
