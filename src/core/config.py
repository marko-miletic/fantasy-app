from typing import Optional, Any
from pydantic import (
    BaseSettings,
    BaseModel,
    PostgresDsn,
    validator
)

from os import getenv
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "dash-stats-app"

    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn]

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str]) -> Any:
        if isinstance(v, str):
            return v
        
        return PostgresDsn.build(
            scheme="postgresql",
            user=getenv("POSTGRES_USER"),
            password=getenv("POSTGRES_PASSWORD"),
            host=getenv('POSTGRES_HOST'),
            port=getenv("POSTGRES_PORT"),
            path=f"/{getenv('POSTGRES_DB') or ''}"
        )

    class Config:
        case_sensitive = True
        env_file = ".env"


class AppServerSettings(BaseModel):
    DEBUG: bool = False
    HOST: str = '0.0.0.0'
    PORT: int = 5000


class AdminDefaultAccount(BaseModel):
    USER: str = 'admin'
    MAIL: str = getenv('DEFAULT_ADMIN_USER_MAIL')
    PASSWORD: str = getenv('DEFAULT_ADMIN_USER_PASSWORD')


settings = Settings()
app_server_settings = AppServerSettings()
admin_default_account = AdminDefaultAccount()
