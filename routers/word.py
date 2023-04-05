from typing import List

from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session

from databases.setup import getDB
from handlers.header import verifyHeader
from routers.dependency import dbUserDep
from handlers.word import getUserCollectedWords

from utils.enum import RouterGroupType

router = APIRouter(prefix="/collected-words", tags=[RouterGroupType.WORD], dependencies=[Depends(verifyHeader)])


@router.get("")
async def getCollectedWords(dbUser: dbUserDep, db: Session = Depends(getDB)) -> List[int]:
    wordIds = await getUserCollectedWords(dbUser, db)
    return wordIds
