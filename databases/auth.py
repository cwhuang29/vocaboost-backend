from pydantic import UUID4
from sqlalchemy.orm import Session

from databases.auth_helper import getAuthHistoryORM
from databases.user import getUserByUUID
from utils.enum import AuthHistoryType, ClientSourceType


async def createAuthHistory(db: Session, uuid: UUID4, source: ClientSourceType, authHistoryType: AuthHistoryType):
    dbUser = await getUserByUUID(db, uuid)
    if dbUser:
        dbAuthHistoryRecord = getAuthHistoryORM(dbUser.id, source, authHistoryType)
        db.add(dbAuthHistoryRecord)
        db.commit()


# Note: this will be moved to a separate analytics server
async def createLoginRecord(db: Session, uuid: UUID4, source: ClientSourceType):
    await createAuthHistory(db, uuid, source, AuthHistoryType.SIGNEDIN)


# Note: this will be moved to a separate analytics server
async def createLogoutRecord(db: Session, uuid: UUID4, source: ClientSourceType):
    await createAuthHistory(db, uuid, source, AuthHistoryType.SIGNEDOUT)
