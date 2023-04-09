from datetime import datetime
from sqlalchemy.orm import Session
from databases.user import getUserByUUID
from handlers.auth_helper import decodeAccessToken
from formatter.setting import formatSettingFromWS

from structs.schemas.auth import TokenData
from structs.schemas.setting import Setting
from utils.message import ERROR_MSG


async def getWSUpdateSettingPayload(payload, db: Session):
    tokenData: TokenData = None
    setting: Setting = None
    error: str = None

    try:
        tokenData = decodeAccessToken(payload['accessToken'])
        dbUser = await getUserByUUID(db, tokenData.uuid)
    except Exception:
        error = ERROR_MSG.LOGIN_FIRST
        return {'dbUser': None, 'setting': None, 'error': error}

    if dbUser is None:
        error = ERROR_MSG.LOGIN_FIRST
        return {'dbUser': None, 'setting': None, 'error': error}

    try:
        ts = datetime.strptime(payload['ts'], '%Y-%m-%dT%H:%M:%S.%fZ')
        setting = formatSettingFromWS(payload['config'], dbUser.id, ts)
    except Exception:
        return {'error': ERROR_MSG.PAYLOAD_INCORRECT}
    return {'dbUser': dbUser, 'setting': setting, 'error': error}
