from pydantic import UUID4
from sqlalchemy.orm import Session

from databases.auth_helper import getDetailedUserORM, getUserORM
from structs.models.user import AzureUserORM, GoogleUserORM, UserORM
from utils.enum import LoginMethodType
from utils.type import DetailedUserORMTypeAll, DetailedUserTypeAll


async def getUser(db: Session, id: int):
    return db.query(UserORM).filter(UserORM.id == id).first()


async def getUserByUUID(db: Session, uuid: UUID4):
    return db.query(UserORM).filter(UserORM.uuid == str(uuid)).first()


async def getDetailedUser(db: Session, loginMethod: int, userId: int):
    entity = None
    if loginMethod == LoginMethodType.GOOGLE.value:
        entity = GoogleUserORM
    if loginMethod == LoginMethodType.AZURE.value:
        entity = AzureUserORM

    if not entity:
        return None
    return db.query(entity).filter(entity.userId == userId).first()


async def getGoogleUser(db: Session, email: str):
    return db.query(GoogleUserORM).filter(GoogleUserORM.email == email).first()


async def getAzureUser(db: Session, email: str):
    return db.query(AzureUserORM).filter(AzureUserORM.email == email).first()


async def getUsers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(UserORM).order_by(UserORM.id.asc()).offset(skip).limit(limit).all()


async def createUser(db: Session, user: DetailedUserTypeAll) -> tuple[UserORM, DetailedUserORMTypeAll]:
    dbUser = getUserORM(user)
    db.add(dbUser)
    db.flush()  # Without this, the dbUser.id would not match in two tables

    dbDetailedUser = getDetailedUserORM(user, dbUser.id)
    if dbDetailedUser:
        db.add(dbDetailedUser)
    db.commit()

    db.refresh(dbUser)
    return dbUser, dbDetailedUser
