from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from databases.setup import get_db
from handlers.auth import getTokenData
from handlers.user import getUserSettings, getUserByTokenData
from structs.schemas.auth import TokenData
from structs.schemas.setting import Setting
from utils.enum import RouterGroupType

router = APIRouter(prefix="/users")


@router.get("/me", tags=[RouterGroupType.USER])
def me(tokenData: Annotated[TokenData, Depends(getTokenData)], db: Session = Depends(get_db)):
    resp = getUserByTokenData(tokenData, db)
    return resp


@router.get("/setting", tags=[RouterGroupType.USER], response_model=Setting)
def getSettings(tokenData: Annotated[TokenData, Depends(getTokenData)], db: Session = Depends(get_db)):
    resp = getUserSettings(tokenData, db)
    return resp
