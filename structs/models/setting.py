from sqlalchemy import Column, DateTime, Integer, SmallInteger, String, Text
from sqlalchemy.sql import func

from databases.setup import Base


class SettingORM(Base):
    __tablename__ = "settings"

    user_id = Column(Integer, primary_key=True, index=True)
    highlight_color = Column(String)
    language = Column(String)
    font_size = Column(String)
    show_detail = Column(SmallInteger)
    collected_words = Column(String)
    suspended_pages = Column(Text)
    updated_at = Column(DateTime, default=func.now())
