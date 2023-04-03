import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from databases.user import getUserByUUID
from databases.setting import getSettingsByUser
from handlers.auth_helper import HTTPCredentialsException, authenticateUserByTokenData
from handlers.formatter import formatUserFromORM
from handlers.user_helper import getSettingFromORM
from structs.schemas.auth import TokenData
from structs.schemas.setting import Setting
from structs.schemas.user import User
from utils.message import HTTP_ERROR_MSG

logger = logging.getLogger(__name__)


async def getUserByTokenData(tokenData: TokenData, db: Session) -> User:
    dbUser, dbDetailedUser = await authenticateUserByTokenData(db, tokenData)
    if dbUser is None:
        raise HTTPCredentialsException
    return formatUserFromORM(dbUser, dbDetailedUser)


async def getUserSettings(tokenData: TokenData, db: Session) -> Setting:
    setting = None
    try:
        dbUser = await getUserByUUID(db, tokenData.uuid)
        if dbUser:
            dbSetting = await getSettingsByUser(db, dbUser.id)
            setting = getSettingFromORM(dbSetting)
        else:
            raise HTTPException(status_code=401, detail=HTTP_ERROR_MSG.LOGIN_FIRST)
    except Exception as err:
        logger.error(str(err))
        raise HTTPException(status_code=500)
    return setting
