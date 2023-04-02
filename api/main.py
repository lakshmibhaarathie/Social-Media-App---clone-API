from fastapi import (FastAPI,Depends, status)
from fastapi.responses import Response
from api.database import get_db
from sqlalchemy.orm import Session


app = FastAPI()

@app.get("/")
def get_posts(db:Session=Depends(get_db)):
    return {"msg":"success"}