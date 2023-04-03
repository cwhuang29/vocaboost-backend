from sqlalchemy.orm import Session
from structs.schemas.auth import TokenData


async def getUserCollectedWords(tokenData: TokenData, db: Session):
    pass
