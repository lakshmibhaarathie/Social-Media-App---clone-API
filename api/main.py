from fastapi import FastAPI

from api import models
from api.database import engine
from api.routers import (posts,users)

# to create the table if not exists
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)

@app.get("/")
def home():
    return {"msg":"Welcome Home"}


