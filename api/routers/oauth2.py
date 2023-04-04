from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from api import schemas, models
from api.database import get_db


ouath2_scheme = OAuth2PasswordBearer(tokenUrl="login")  # tokenUrl = give login base url

SECRET_KEY = "give@some#random%text"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 30

def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY
                             , algorithm=ALGORITHM) 
    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=ALGORITHM)
        id:str = payload.get("user_id")    # type:ignore

        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)

        return token_data
    except JWTError:
        raise credentials_exception
    
def get_current_user(token:str=Depends(ouath2_scheme), db:Session = Depends(get_db)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials"
        , headers={"WWW-Authenticate":"Bearer"}
    )
    
    user_token = verify_access_token(
        token=token, credentials_exception=credentials_exception)
    
    current_user = db.query(models.Users).filter(models.Users.id==user_token.id).first()
    print(type(current_user))
    return current_user