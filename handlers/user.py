import logging

from fastapi import HTTPException
from sqlalchemy.orm import Session

from databases.user import getUserByUUID
from databases.setting import getSettingsByUser
from handlers.auth_helper import HTTPCredentialsException, getUserAndDetailedUserByTokenData
from handlers.formatter import formatUserFromORM
from handlers.user_helper import getSettingFromORM
from structs.schemas.auth import TokenData
from structs.schemas.setting import Setting
from structs.schemas.user import UserOut
from utils.message import getShouldLoginMsg, getUnexpectedErrMsg

logger = logging.getLogger(__name__)


async def getDisplayUserByTokenData(tokenData: TokenData, db: Session) -> UserOut:
    dbUser, dbDetailedUser = await getUserAndDetailedUserByTokenData(db, tokenData)
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
            raise HTTPException(status_code=401, detail=getShouldLoginMsg())
    except Exception as err:
        logger.error(str(err))
        raise HTTPException(status_code=500, detail=getUnexpectedErrMsg())
    return setting
