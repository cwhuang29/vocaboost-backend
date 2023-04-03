from typing import Annotated

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from databases.setup import get_db
from handlers.auth import getTokenData
from handlers.word import getUserCollectedWords
from structs.schemas.auth import TokenData

from utils.enum import RouterGroupType

router = APIRouter(prefix="/manage-words")


@router.get("/", tags=[RouterGroupType.WORD])
def getCollectedWords(tokenData: Annotated[TokenData, Depends(getTokenData)], db: Session = Depends(get_db)):
    getUserCollectedWords(tokenData, db)
    return {"num_of_words": 0}
