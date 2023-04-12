from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import models
from api.database import engine
from api.routers import (posts,users,auth,votes)

# to create the table if not exists
models.Base.metadata.create_all(bind=engine) # this command can be removed after we have using alembic 


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware
    , allow_origins=origins
    , allow_credentials=True
    , allow_methods=["*"]
    , allow_headers=["*"]
)
app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(votes.router)

@app.get("/")
async def home():
    return {"msg":"Welcome Home"}


