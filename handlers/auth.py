from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import logging
from handlers.auth_helper import getGoogleUserFromReq

from structs.requests.auth import ReqLogin, ReqLogout
from utils.enum import LoginMethodType
from databases.auth import createLoginRecord, createLogoutRecord, createUser, getUser

logger = logging.getLogger(__name__)


def handle_google_login(reqLogin: ReqLogin, db: Session):
    try:
        user = getGoogleUserFromReq(reqLogin)
    except Exception as err:
        raise HTTPException(status_code=400, detail=str(err))

    try:
        dbUser = getUser(db, reqLogin.uuid)
        if not dbUser:
            dbUser = createUser(db, user)
        createLoginRecord(db, dbUser.id)
        user.uuid = dbUser.uuid
    except IntegrityError:  # e.g., email is not unique
        raise HTTPException(status_code=400)
    except Exception as err:
        logger.error(err)
        raise HTTPException(status_code=500)
    return user


def handle_login(req_login: ReqLogin, db: Session):
    user = None
    if req_login.loginMethod == LoginMethodType.GOOGLE:
        user = handle_google_login(req_login, db)
    else:
        raise HTTPException(status_code=400)
    return user


def handle_logout(req_logout: ReqLogout, db: Session):
    dbUser = getUser(db, req_logout.uuid)
    if dbUser:
        createLogoutRecord(db, dbUser.id)
