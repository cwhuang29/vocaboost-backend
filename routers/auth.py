from typing import Annotated
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from handlers.auth import getTokenData, handleLogin, handleLogout
from structs.requests.auth import ReqLogin
from databases.setup import get_db
from structs.schemas.auth import Token, TokenData
from utils.enum import RouterGroupType

router = APIRouter()


@router.post("/login", tags=[RouterGroupType.AUTH], response_model=Token)
def login(req_login: ReqLogin, db: Session = Depends(get_db)):
    resp = handleLogin(req_login, db)
    return resp


@router.post("/logout", tags=[RouterGroupType.AUTH])
def logout(tokenData: Annotated[TokenData, Depends(getTokenData)], db: Session = Depends(get_db)):
    handleLogout(tokenData, db)
    return {"result": "success"}
