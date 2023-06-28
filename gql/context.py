import functools
import logging

from strawberry.fastapi import BaseContext
from strawberry.types import Info as _Info
from strawberry.types.info import RootValueType

from handlers.auth_helper import decodeAccessToken
from structs.schemas.auth import TokenData
from utils.message import ERROR_MSG

logger = logging.getLogger(__name__)


class Context(BaseContext):
    @functools.cached_property
    def tokenData(self) -> TokenData | None:
        if not self.request:
            raise ValueError(ERROR_MSG.UNEXPECTED_ERR)

        token = self.request.headers.get("Authorization", None)
        if not token:
            raise ValueError(ERROR_MSG.OAUTH_TOKEN_MALFORMED)

        t = token.split(' ')
        if len(t) != 2:
            raise ValueError(ERROR_MSG.OAUTH_TOKEN_MALFORMED)
        tokenData = decodeAccessToken(t[1])
        return tokenData


async def getContext() -> Context:
    return Context()


Info = _Info[Context, RootValueType]
