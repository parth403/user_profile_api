from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int=30
    SECRET_KEY:str
    ALGORITHM:str
    model_config=SettingsConfigDict(env_file='.env')

settings=Settings()
