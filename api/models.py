from sqlalchemy import (Column, Integer
                        , Boolean, String)
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from api.database import Base


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True
                , nullable=False, unique=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False,
                       server_default="True")
    created_at = Column(TIMESTAMP, server_default=text("now()")
                        , nullable=False)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True
                , nullable=False, unique=True)
    email = Column(String, nullable=False
                   , unique=True)
    password = Column(String, nullable=False)

