from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgres://postgres:sql123@localhost/api_dev"


engine = create_engine(url=SQLALCHEMY_DATABASE_URL,)
SessionLocal = sessionmaker(bine=engine, autocommit=False
                            , autoflush=False)

Base  = declarative_base()

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()
