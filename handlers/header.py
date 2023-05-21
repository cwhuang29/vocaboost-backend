from typing import Annotated
import logging

from fastapi import HTTPException, Header

from utils.enum import ClientSourceHeaderType, ClientSourceType, DevicePlatformType
from utils.message import getNoSourceHeaderMsg

logger = logging.getLogger(__name__)


def verifyHeader(x_vh_source: Annotated[str, Header()]):
    try:
        _ = ClientSourceHeaderType(x_vh_source)
    except Exception as err:
        logger.exception(err)
        raise HTTPException(status_code=400, detail=getNoSourceHeaderMsg())


def getSourceHeader(x_vh_source: Annotated[str, Header()]) -> ClientSourceType:
    source = ClientSourceType.UNKNOWN
    try:
        s = ClientSourceHeaderType(x_vh_source)
        if s == ClientSourceHeaderType.MOBILE:
            source = ClientSourceType.MOBILE
        if s == ClientSourceHeaderType.EXTENSION:
            source = ClientSourceType.EXTENSION
    except Exception:
        pass
    return source


def getDevicePlatformHeader(x_vh_platform: Annotated[str, Header()]) -> DevicePlatformType:
    source = DevicePlatformType.UNKNOWN
    try:
        source = DevicePlatformType(x_vh_platform)
    except Exception:
        # We only support iOS at first. So if this header is missing, then the user probably did not update
        source = DevicePlatformType.IOS
    return source
