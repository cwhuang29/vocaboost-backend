from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils.database import getDBURL


url = getDBURL()

db_engine = create_engine(url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
Base = declarative_base()


# An independent database session/connection (SessionLocal) per request, use the same session through all the request then close it after the request is finished
def getDB():
    db = SessionLocal()
    try:
        yield db  # Injected into path operations
    finally:
        db.close()  # Executed after the response has been delivered
