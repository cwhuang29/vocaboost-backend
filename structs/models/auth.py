from sqlalchemy import Column, DateTime, Integer
from sqlalchemy.sql import func

from databases.setup import Base


class AuthHistoryORM(Base):
    __tablename__ = "auth_history"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer)
    action = Column(Integer)
    created_at = Column(DateTime, default=func.now())
