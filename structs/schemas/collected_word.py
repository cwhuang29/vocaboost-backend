from datetime import datetime

from pydantic import BaseModel, Field, conint


class CollectedWord(BaseModel):
    userId: conint(ge=0)
    wordId: conint(ge=0)
    isValid: Field(1, ge=0, lt=2)
    updatedAt: datetime

    class Config:
        orm_mode = True
