from fastapi import Depends, APIRouter, WebSocket
from sqlalchemy.orm import Session

from databases.setup import getDB
from handlers.user import getUserSetting, getDisplayUserByTokenData, updateUserSetting, updateUserSettingWS
from routers.dependency import tokenDataDep, dbUserDep
from structs.schemas.setting import Setting
from structs.schemas.user import UserOut
from utils.enum import RouterGroupType

router = APIRouter(prefix="/users", tags=[RouterGroupType.USER])


@router.get("/me")
async def me(tokenData: tokenDataDep, db: Session = Depends(getDB)) -> UserOut:
    resp = await getDisplayUserByTokenData(tokenData, db)
    return resp


@router.get("/setting", response_model=Setting)
async def getSetting(dbUser: dbUserDep, db: Session = Depends(getDB)) -> Setting:
    resp = await getUserSetting(dbUser, db)
    return resp


@router.put("/setting")
async def updateSetting(setting: Setting, dbUser: dbUserDep, db: Session = Depends(getDB)):
    resp = await updateUserSetting(dbUser, setting, db)
    return resp


@router.websocket("/setting")
async def updateSettingWebSocket(websocket: WebSocket, db: Session = Depends(getDB)):
    await updateUserSettingWS(websocket, db)
