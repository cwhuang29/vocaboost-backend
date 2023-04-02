from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func

from databases.setup import Base


class CollectedWordORM(Base):
    __tablename__ = "collected_words"

    user_id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, primary_key=True, index=True)
    is_valid = Column(Integer)
    updated_at = Column(DateTime, default=func.now())
