from typing import List

from sqlalchemy.orm import Session
from handlers.user import getUserSetting
from structs.models.user import UserORM


async def getUserCollectedWords(dbUser: UserORM, db: Session) -> List[int]:
    setting = getUserSetting(dbUser, db)
    words = setting.collectedWords
    return words
