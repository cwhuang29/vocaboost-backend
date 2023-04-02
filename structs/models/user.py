from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from databases.setup import Base


class UserORM(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    method = Column(Integer)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime)


class GoogleUserORM(Base):
    __tablename__ = "users_google"

    user_id = Column(Integer, primary_key=True, index=True)
    scopes = Column(String)
    serverAuthCode = Column(String)
    email = Column(String)
    avatar = Column(String)
