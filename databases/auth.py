from sqlalchemy.orm import Session
from databases.auth_helper import getAuthStatusORM, getDetailedUserORM, getUserORM

from structs.models.user import UserORM
from structs.schemas.user import User
from utils.enum import AuthHistoryType


def getUser(db: Session, uuid: int):
    return db.query(UserORM).filter(UserORM.uuid == uuid).first()


def getUsers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserORM).order_by(UserORM.id.asc()).offset(skip).limit(limit).all()


def createUser(db: Session, user: User):
    dbUser = getUserORM(user)
    db.add(dbUser)
    db.flush()  # Without this, the dbUser.id would not match in two tables

    dbUserDetailed = getDetailedUserORM(user, dbUser.id)
    if dbUserDetailed:
        db.add(dbUserDetailed)
    db.commit()

    db.refresh(dbUser)
    db.refresh(dbUserDetailed)
    return dbUser


def createLoginRecord(db: Session, id: int):
    dbAuthStatus = getAuthStatusORM(id, AuthHistoryType.SIGNEDIN)
    db.add(dbAuthStatus)
    db.commit()


def createLogoutRecord(db: Session, id: int):
    dbAuthStatus = getAuthStatusORM(id, AuthHistoryType.SIGNEDOUT)
    db.add(dbAuthStatus)
    db.commit()
