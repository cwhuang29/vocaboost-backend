from pydantic import UUID4
from sqlalchemy.orm import Session

from databases.auth_helper import getAuthHistoryORM
from databases.user import getUserByUUID
from utils.enum import AuthHistoryType


async def createAuthHistory(db: Session, uuid: UUID4, authHistoryType: AuthHistoryType):
    dbUser = await getUserByUUID(db, uuid)
    if dbUser:
        dbAuthHistoryRecord = getAuthHistoryORM(dbUser.id, authHistoryType)
        db.add(dbAuthHistoryRecord)
        db.commit()


async def createLoginRecord(db: Session, uuid: UUID4):
    await createAuthHistory(db, uuid, AuthHistoryType.SIGNEDIN)


async def createLogoutRecord(db: Session, uuid: UUID4):
    await createAuthHistory(db, uuid, AuthHistoryType.SIGNEDOUT)
