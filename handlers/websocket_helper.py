from sqlalchemy.orm import Session

from datetime import datetime
from databases.user import getUserByUUID
from formatter.setting import formatSettingFromWS
from handlers.auth_helper import decodeAccessToken
from utils.message import ERROR_MSG


def parseWSTimeStamp(ts) -> datetime:
    return datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S.%fZ')


async def verifyWSToken(payload, db: Session):
    try:
        tokenData = decodeAccessToken(payload['accessToken'])
        dbUser = await getUserByUUID(db, tokenData.uuid)
    except Exception:
        return None, ERROR_MSG.LOGIN_FIRST
    return dbUser, None


async def getWSUpdateCollectedWordsPayload(payload, db: Session):
    dbUser, error = await verifyWSToken(payload, db)
    if error is not None:
        return {'dbUser': None, 'setting': None, 'error': error}

    try:
        ts = parseWSTimeStamp(payload['ts'])
        collectedWords = payload['data']
        return {'dbUser': dbUser, 'collectedWords': collectedWords, 'ts': ts, 'error': error}
    except Exception:
        return {'error': ERROR_MSG.PAYLOAD_INCORRECT}


async def getWSUpdateSettingPayload(payload, db: Session):
    dbUser, error = await verifyWSToken(payload, db)
    if dbUser is None:
        return {'dbUser': None, 'setting': None, 'error': error}

    try:
        ts = parseWSTimeStamp(payload['ts'])
        setting = formatSettingFromWS(payload['data'], dbUser.id, ts)
        return {'dbUser': dbUser, 'setting': setting, 'error': error}
    except Exception:
        return {'error': ERROR_MSG.PAYLOAD_INCORRECT}
