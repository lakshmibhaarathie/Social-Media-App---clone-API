from sqlalchemy import (Column, Integer
                        , Boolean, String, ForeignKey)
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship
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
    user_id = Column(Integer
                     , ForeignKey(column="users.id", ondelete="CASCADE")
                     , nullable=False)
    user_info = relationship("Users")  # this defines the relationship with the below class Users

class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True
                , nullable=False, unique=True)
    email = Column(String, nullable=False
                   , unique=True)
    password = Column(String, nullable=False)

    created_at = Column(TIMESTAMP, server_default=text('now()')
                        , nullable=False)

class Votes(Base):
    __tablename__ = "votes"
    
    user_id = Column(Integer
                     , ForeignKey(column="users.id", ondelete="CASCADE")
                     , nullable=False, primary_key=True)
    post_id = Column(Integer
                     , ForeignKey(column="posts.id", ondelete="CASCADE")
                     , nullable=False, primary_key=True)
    vote = Column(Integer, nullable=False)
    
    user_info = relationship("Users")
    posts_info = relationship("Posts")
