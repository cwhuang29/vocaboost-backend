from sqlalchemy import Column, DateTime, Integer, SmallInteger, String, Text
from sqlalchemy.sql import func

from databases.setup import Base


class SettingORM(Base):
    __tablename__ = "settings"

    userId = Column('user_id', Integer, primary_key=True, index=True)
    highlightColor = Column('highlight_color', String)
    language = Column('language', String)
    fontSize = Column('font_size', String)
    showDetail = Column('show_detail', SmallInteger)
    collectedWords = Column('collected_words', String)
    suspendedPages = Column('suspended_pages', Text)
    updatedAt = Column('updated_at', DateTime, default=func.now())
