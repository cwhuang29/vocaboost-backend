from sqlalchemy import Column, String, Integer

from databases.setup import Base


class GreWordORM(Base):
    __tablename__ = 'gre_words'

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String)
