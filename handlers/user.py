import logging

from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from databases.setting import getSettingByUser
from handlers.auth_helper import HTTPCredentialsException, getUserAndDetailedUserByTokenData
from handlers.formatter import formatUserFromORM, formatSettingFromORM
from handlers.user_helper import tryUpdateUserSetting
from handlers.websocket_helper import getWSUpdateSettingPayload
from structs.models.user import UserORM
from structs.schemas.auth import TokenData
from structs.schemas.setting import Setting, UpdateSettingOut

logger = logging.getLogger(__name__)


async def getDisplayUserByTokenData(tokenData: TokenData, db: Session):
    dbUser, dbDetailedUser = await getUserAndDetailedUserByTokenData(db, tokenData)
    if dbUser is None:
        raise HTTPCredentialsException
    return formatUserFromORM(dbUser, dbDetailedUser)


async def getUserSetting(dbUser: UserORM, db: Session) -> Setting:
    dbSetting = await getSettingByUser(db, dbUser.id)
    setting = formatSettingFromORM(dbSetting)
    return setting


async def updateUserSetting(dbUser: UserORM, setting: Setting, db: Session) -> UpdateSettingOut:
    result = await tryUpdateUserSetting(dbUser, setting, db)
    return result


async def updateUserSettingWS(websocket: WebSocket, db: Session):
    '''
    Payload from client ought to look like:
    {
        'config': {'highlightColor': 'PINK', 'language': 'en', 'fontSize': 'MEDIUM', 'showDetail': True, 'collectedWords': [39], 'suspendedPages': []},
        'accessToken': '<JWT token>',
        'ts': '2023-04-05T08:21:00.713Z'
    }
    '''
    await websocket.accept()
    try:
        while True:
            json = await websocket.receive_json()

            resp = {}
            parsed = await getWSUpdateSettingPayload(json, db)
            if parsed['error']:
                resp = parsed
            else:
                dbUser, setting = parsed['dbUser'], parsed['setting']
                resp = await tryUpdateUserSetting(dbUser, setting, db)
            await websocket.send_json(resp)
    except WebSocketDisconnect:
        pass
