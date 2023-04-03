from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# url = "postgresql://<username>:<password>@<host-ip address>/<databasename>"
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:sql123@localhost/api_dev"

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