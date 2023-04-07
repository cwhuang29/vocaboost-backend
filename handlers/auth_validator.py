from sqlalchemy.orm import Session

from databases.user import getGoogleUser, getUser
from structs.models.user import GoogleUserORM, UserORM
from structs.schemas.user import GoogleUser, User
from utils.enum import LoginMethodType


async def checkUser(db: Session, user: User, userId: int) -> UserORM | None:
    u = await getUser(db, userId)
    if u is None:
        return None
    if LoginMethodType(u.method) != user.loginMethod:
        return None
    return u


async def checkGoogleLoginUser(db: Session, user: GoogleUser) -> GoogleUserORM | None:
    u = await getGoogleUser(db, user.email)
    if u is None:
        return None
    return u


async def checkDetailedLoginUser(db: Session, user: User):
    dbDetailedUser = None
    if user.loginMethod == LoginMethodType.GOOGLE:
        dbDetailedUser = await checkGoogleLoginUser(db, user)
    return dbDetailedUser


async def checkLoginPayload(db: Session, user: User) -> tuple[UserORM, GoogleUserORM] | tuple[None, None]:
    dbDetailedUser = await checkDetailedLoginUser(db, user)
    if dbDetailedUser is None:
        return None, None
    dbUser = await checkUser(db, user, dbDetailedUser.userId)
    if dbUser is None:
        return None, None
    return dbUser, dbDetailedUser
