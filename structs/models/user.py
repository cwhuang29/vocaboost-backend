from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from databases.setup import Base


class UserORM(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, unique=True, index=True)
    firstName = Column('first_name', String)
    lastName = Column('last_name', String)
    method = Column(Integer)
    createdAt = Column('created_at', DateTime, default=func.now())
    updatedAt = Column('updated_at', DateTime)

    def __repr__(self):
        return f'{self.__module__}-{type(self).__qualname__}-{self.id}'


class GoogleUserORM(Base):
    __tablename__ = 'users_google'

    userId = Column('user_id', Integer, primary_key=True, index=True)
    accountId = Column('account_id', String)
    scopes = Column(String)
    email = Column(String)
    avatar = Column(String)


class AzureUserORM(Base):
    __tablename__ = 'users_azure'

    userId = Column('user_id', Integer, primary_key=True, index=True)
    accountId = Column('account_id', String)
    scopes = Column(String)
    email = Column(String)
    avatar = Column(Text)  # Base64 encoding string
