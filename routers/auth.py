from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from handlers.auth import handle_login, handle_logout
from structs.requests.auth import ReqLogin, ReqLogout
# from structs import models, schemas
from databases.setup import SessionLocal  # , db_engine
from structs.schemas.user import User

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/login", response_model=User)
def login(req_login: ReqLogin, db: Session = Depends(get_db)):
    resp = handle_login(req_login, db)
    return resp


@router.post("/logout")
def logout(req_logout: ReqLogout):
    handle_logout(req_logout)
    return {}
