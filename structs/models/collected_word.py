from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func

from databases.setup import Base


class CollectedWordORM(Base):
    __tablename__ = 'collected_words'

    userId = Column('user_id', Integer, primary_key=True, index=True)
    wordId = Column('word_id', Integer, primary_key=True, index=True)
    isValid = Column('is_valid', Integer)
    updatedAt = Column('updated_at', DateTime, default=func.now())
