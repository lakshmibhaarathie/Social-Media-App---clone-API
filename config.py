from pydantic import BaseSettings


class Settings(BaseSettings):
    DATABASE_NAME:str
    DATABASE_HOST:str
    DATABASE_PORT:int
    DATABASE_USERNAME:str
    DATABASE_PASSWORD:str
    DATABASE:str
    ALGORITHM:str
    SECRET_KEY:str
    ACCESS_TOKEN_EXPIRY_TIME:int

    class Config:
        env_file = ".env"

    

settings = Settings()  #type:ignore