from pydantic import UUID4
from sqlalchemy.orm import Session
from databases.auth_helper import getDetailedUserORM, getUserORM

from structs.models.user import GoogleUserORM, UserORM
from structs.schemas.user import User
from utils.enum import LoginMethodType


async def getUser(db: Session, id: int):
    return db.query(UserORM).filter(UserORM.id == id).first()


async def getDetailedUser(db: Session, login_method: int, user_id: int):
    if login_method == LoginMethodType.GOOGLE.value:
        return db.query(GoogleUserORM).filter(GoogleUserORM.user_id == user_id).first()
    return None


async def getUserByUUID(db: Session, uuid: UUID4):
    return db.query(UserORM).filter(UserORM.uuid == str(uuid)).first()


async def getUsers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserORM).order_by(UserORM.id.asc()).offset(skip).limit(limit).all()


async def createUser(db: Session, user: User) -> tuple[UserORM, GoogleUserORM]:
    dbUser = getUserORM(user)
    db.add(dbUser)
    db.flush()  # Without this, the dbUser.id would not match in two tables

    dbDetailedUser = getDetailedUserORM(user, dbUser.id)
    if dbDetailedUser:
        db.add(dbDetailedUser)
    db.commit()

    db.refresh(dbUser)
    return dbUser, dbDetailedUser
