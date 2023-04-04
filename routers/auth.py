from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from handlers.auth import getTokenData, handleLogin, handleLogout, tryToGetTokenData
from structs.requests.auth import ReqLogin
from databases.setup import getDB
from structs.schemas.auth import Token, TokenData
from utils.enum import RouterGroupType

router = APIRouter(tags=[RouterGroupType.AUTH])


@router.post("/login", response_model=Token)
async def login(req_login: ReqLogin, tokenData: Annotated[bool, Depends(tryToGetTokenData)], db: Session = Depends(getDB)):
    resp = await handleLogin(req_login, tokenData, db)
    return resp


@router.post("/logout")
async def logout(tokenData: Annotated[TokenData, Depends(getTokenData)], db: Session = Depends(getDB)):
    await handleLogout(tokenData, db)
    return {"result": "success"}
