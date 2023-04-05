from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func

from databases.setup import Base


class AuthHistoryORM(Base):
    __tablename__ = "auth_history"

    id = Column(Integer, primary_key=True)
    userId = Column('user_id', Integer)
    action = Column(Integer)
    source = Column(Integer)
    createdAt = Column('created_at', DateTime, default=func.now())
