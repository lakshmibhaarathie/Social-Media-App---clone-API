from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from config import settings

# url = "postgresql://<username>:<password>@<host-ip address>/<databasename>"
SQLALCHEMY_DATABASE_URL = f"{settings.DATABASE}://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}/{settings.DATABASE_NAME}"

engine = create_engine(url=SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autocommit=False
                            , autoflush=False)

Base = declarative_base()

def get_db():
    """
     Description: 
        This function makes a connection with database.
    Returns:
        Database object
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()