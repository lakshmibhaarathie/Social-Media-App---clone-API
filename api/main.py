from fastapi import FastAPI

from api import models
from api.database import engine
from api.routers import (posts,users,auth,votes)

# to create the table if not exists
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
def home():
    return {"msg":"Welcome Home"}


