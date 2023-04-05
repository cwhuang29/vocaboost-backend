import ast
from sqlalchemy.orm import Session

from databases.user import getGoogleUser, getUser
from structs.models.user import GoogleUserORM, UserORM
from structs.schemas.user import GoogleUser, User
from utils.enum import LoginMethodType


def checkUser(user: User, dbUser: UserORM):
    if user.loginMethod.value != dbUser.method:
        return True
    return False


async def checkGoogleLoginUser(db: Session, user: GoogleUser):
    u = await getGoogleUser(db, user.email)
    if u is None:
        return None
    if sorted(ast.literal_eval(u.scopes)) != sorted(ast.literal_eval(user.scopes)):
        return None
    if u.server_auth_code != user.serverAuthCode:
        return None
    return u


async def checkDetailedLoginUser(db: Session, user: User):
    dbDetailedUser = None
    print(user.loginMethod)
    if user.loginMethod == LoginMethodType.GOOGLE:
        dbDetailedUser = await checkGoogleLoginUser(db, user)
    return dbDetailedUser


async def checkLoginPayload(db: Session, user: User) -> tuple[UserORM, GoogleUserORM] | tuple[None, None]:
    dbDetailedUser = await checkDetailedLoginUser(db, user)
    if dbDetailedUser is None:
        return None, None

    dbUser = await getUser(db, dbDetailedUser.user_id)
    if checkUser(user, dbUser):
        return None, None
    return dbUser, dbDetailedUser
