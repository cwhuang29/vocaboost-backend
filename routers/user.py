from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from databases.setup import getDB
from handlers.auth import getTokenData
from handlers.user import getUserSettings, getDisplayUserByTokenData
from structs.schemas.auth import TokenData
from structs.schemas.setting import Setting
from utils.enum import RouterGroupType

router = APIRouter(prefix="/users", tags=[RouterGroupType.USER])


tokenDataDep = Annotated[TokenData, Depends(getTokenData)]


@router.get("/me")
async def me(tokenData: tokenDataDep, db: Session = Depends(getDB)):
    resp = await getDisplayUserByTokenData(tokenData, db)
    return resp


@router.get("/setting", response_model=Setting)
async def getSettings(tokenData: tokenDataDep, db: Session = Depends(getDB)):
    resp = await getUserSettings(tokenData, db)
    return resp
