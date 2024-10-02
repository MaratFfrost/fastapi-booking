from pydantic import  model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_NAME: str
    DB_PASS: str
    DATABASE_URL: str = ""
    KEY: str
    ALGORITM: str
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_PORT: int

    @model_validator(mode='after')
    def get_database_url(cls, values):
        values.DATABASE_URL = (
            f"postgresql+asyncpg://{values.DB_USER}:{values.DB_PASS}@{values.DB_HOST}:{values.DB_PORT}/{values.DB_NAME}"
        )
        return values

    class Config:
        env_file = ".env"


settings = Settings()
