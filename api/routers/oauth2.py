from jose import jwt, JWTError
from datetime import datetime, timedelta


SECRET_KEY = "give@some#random%text"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRY_MINUTES = 30

def create_access_token(data:dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(claims=to_encode, key=SECRET_KEY
                             , algorithm=ALGORITHM) 
    return encoded_jwt