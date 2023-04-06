# global-modules
from fastapi import (Depends,status, APIRouter)
from fastapi.responses import Response
from sqlalchemy.orm import Session


# user-defined modules
from api import models
from api.utils import EncoDec
from api.schemas import (User, UserResponse)
from api.database import get_db


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/{id}", response_model=UserResponse)
def get_user(id:int, db:Session=Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id==id).first()
    return user

@router.post("/",response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user:User, db:Session=Depends(get_db)):

    user.password = EncoDec.pwd_encrypt(user.password)
    user_dict = user.dict()
    new_user = models.Users(**user_dict)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

