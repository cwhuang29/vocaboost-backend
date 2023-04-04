from typing import Annotated

from fastapi import HTTPException, Header

from utils.enum import CLIENT_SOURCE
from utils.message import getNoSourceHeaderMsg


def verifyHeader(x_vh_source: Annotated[str, Header()]):
    try:
        _ = CLIENT_SOURCE(x_vh_source)
    except Exception:
        raise HTTPException(status_code=400, detail=getNoSourceHeaderMsg())
