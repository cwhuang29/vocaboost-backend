from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from databases.setup import getDB
from handlers.auth import getTokenData
from handlers.word import getUserCollectedWords
from structs.schemas.auth import TokenData

from utils.enum import RouterGroupType

router = APIRouter(prefix="/manage-words", tags=[RouterGroupType.WORD])


@router.get("")
async def getCollectedWords(tokenData: Annotated[TokenData, Depends(getTokenData)], db: Session = Depends(getDB)):
    await getUserCollectedWords(tokenData, db)
    return {"num_of_words": 0}
