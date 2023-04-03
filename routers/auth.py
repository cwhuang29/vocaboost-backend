from typing import Annotated
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from handlers.auth import getTokenData, handleLogin, handleLogout, tryToGetTokenData
from structs.requests.auth import ReqLogin
from databases.setup import get_db
from structs.schemas.auth import Token, TokenData
from utils.enum import RouterGroupType

router = APIRouter()


@router.post("/login", tags=[RouterGroupType.AUTH], response_model=Token)
async def login(req_login: ReqLogin, tokenData: Annotated[bool, Depends(tryToGetTokenData)], db: Session = Depends(get_db)):
    resp = await handleLogin(req_login, tokenData, db)
    return resp


@router.post("/logout", tags=[RouterGroupType.AUTH])
async def logout(tokenData: Annotated[TokenData, Depends(getTokenData)], db: Session = Depends(get_db)):
    await handleLogout(tokenData, db)
    return {"result": "success"}
