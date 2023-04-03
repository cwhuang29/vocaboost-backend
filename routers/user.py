from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from databases.setup import get_db
from handlers.auth import getTokenData
from handlers.user import getUserSettings, getDisplayUserByTokenData
from structs.schemas.auth import TokenData
from structs.schemas.setting import Setting
from utils.enum import RouterGroupType

router = APIRouter(prefix="/users")


tokenDataDep = Annotated[TokenData, Depends(getTokenData)]


@router.get("/me", tags=[RouterGroupType.USER])
async def me(tokenData: tokenDataDep, db: Session = Depends(get_db)):
    resp = await getDisplayUserByTokenData(tokenData, db)
    return resp


@router.get("/setting", tags=[RouterGroupType.USER], response_model=Setting)
async def getSettings(tokenData: tokenDataDep, db: Session = Depends(get_db)):
    resp = await getUserSettings(tokenData, db)
    return resp
