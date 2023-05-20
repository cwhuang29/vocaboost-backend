from typing import Annotated

from fastapi import Depends

from handlers.dependency import getDbUserByTokenData, getTokenData, tryToGetTokenData
from handlers.header import getDevicePlatformHeader, getSourceHeader
from structs.models.user import UserORM
from structs.schemas.auth import TokenData
from utils.enum import ClientSourceType, DevicePlatformType

tokenDataDep = Annotated[TokenData, Depends(getTokenData)]

tryToGetTokenDataDep = Annotated[TokenData | None, Depends(tryToGetTokenData)]

dbUserDep = Annotated[UserORM, Depends(getDbUserByTokenData)]

sourceHeaderDep = Annotated[ClientSourceType, Depends(getSourceHeader)]

deivcePlatformHeaderDep = Annotated[DevicePlatformType, Depends(getDevicePlatformHeader)]
