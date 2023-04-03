from pydantic import BaseModel, EmailStr
from typing import Optional


# **************************************    Post Schema   ********************************************
class Post(BaseModel):
    title:str
    content:str
    published:bool=True  
    """
    The default value for publihed column has already been set as server_default\
          to bypass database error on direct access.
    The default value for published column has again set as True in the Post schema\
          to bypass schema error through vscode.
    """

class UpdatePost(BaseModel):
    title:Optional[str]
    content:Optional[str]
    published:Optional[bool]


class PostResponse(BaseModel):
    title:str
    published:bool

    class Config:
        orm_mode=True

    
# **************************************    User Schema   ********************************************

class User(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id:int
    email:EmailStr

    class Config:
        orm_mode = True

# **************************************    JWT Schema   ********************************************

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class LoginResponse(BaseModel):
    secret_key:str
    token:str