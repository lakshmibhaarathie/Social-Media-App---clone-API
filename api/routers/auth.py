from fastapi import (APIRouter, Depends, status, HTTPException)
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from api.schemas import Token
from api.database import get_db
from api import models
from api.utils import EnDec
from api.routers import oauth2


router = APIRouter(tags=["Authentication"])

@router.post("/login",response_model=Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends()
                         , db:Session=Depends(get_db)):
    
    user = db.query(models.Users).filter(
        models.Users.email==user_credentials.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN
                            , detail="Invalid credentials...!")
    
    good_credentials =  EnDec.password_verification(
                        current_password=user_credentials.password
                        , encrypted_password=user.password)
    if not good_credentials:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN
                            , detail="Invalid credentials...!")
    
    access_token = oauth2.create_access_token(data={"user_id":user.id})
    
    return {"access_token":access_token, "token_type":"bearer"}

