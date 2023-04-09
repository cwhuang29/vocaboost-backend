import logging

from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session

from databases.setting import getSettingByUser
from handlers.auth_helper import getUserAndDetailedUserByTokenData
from formatter.user import formatUserFromORM
from formatter.setting import formatSettingFromORM
from handlers.user_helper import tryUpdateUserCollectedWords, tryUpdateUserSetting
from handlers.websocket_helper import getWSUpdateCollectedWordsPayload, getWSUpdateSettingPayload
from structs.models.user import UserORM
from structs.schemas.auth import TokenData
from structs.schemas.setting import Setting, UpdateSettingOut
from utils.exception import HTTP_CREDENTIALS_EXCEPTION

logger = logging.getLogger(__name__)


async def getDisplayUserByTokenData(tokenData: TokenData, db: Session):
    dbUser, dbDetailedUser = await getUserAndDetailedUserByTokenData(db, tokenData)
    if dbUser is None:
        raise HTTP_CREDENTIALS_EXCEPTION
    return formatUserFromORM(dbUser, dbDetailedUser)


async def getUserSetting(dbUser: UserORM, db: Session) -> Setting:
    dbSetting = await getSettingByUser(db, dbUser.id)
    setting = formatSettingFromORM(dbSetting)
    return setting


async def updateUserSetting(dbUser: UserORM, setting: Setting, db: Session) -> UpdateSettingOut:
    result = await tryUpdateUserSetting(dbUser, setting, db)
    return result


async def updateUserCollectedWordsWS(websocket: WebSocket, db: Session):
    '''
    Payload from client ought to look like:
    {
        'collectedWords': [1, 39, 1233],
        'accessToken': '<JWT token>',
        'ts': '2023-04-05T08:21:00.713Z'
    }
    '''
    await websocket.accept()
    try:
        while True:
            json = await websocket.receive_json()
            parsed = await getWSUpdateCollectedWordsPayload(json, db)
            if parsed['error']:
                resp = parsed
            else:
                resp = await tryUpdateUserCollectedWords(parsed['dbUser'], parsed['collectedWords'], parsed['ts'], db)
            await websocket.send_json(resp)
    except WebSocketDisconnect:
        pass


async def updateUserSettingWS(websocket: WebSocket, db: Session):
    '''
    Payload from client ought to look like:
    {
        'config': {'collectedWords': [39], ...},
        'accessToken': '<JWT token>',
        'ts': '2023-04-05T08:21:00.713Z'
    }
    '''
    await websocket.accept()
    try:
        while True:
            json = await websocket.receive_json()
            parsed = await getWSUpdateSettingPayload(json, db)
            if parsed['error']:
                resp = parsed
            else:
                resp = await updateUserSetting(parsed['dbUser'], parsed['setting'], db)
            await websocket.send_json(resp)
    except WebSocketDisconnect:
        pass
