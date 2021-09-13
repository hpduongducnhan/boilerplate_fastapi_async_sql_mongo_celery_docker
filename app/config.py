# -*- coding: utf-8 -*-
from typing import Optional, List, Optional
from pydantic import BaseSettings, AnyHttpUrl
import os

DEV_ENV = os.environ.get('DEV_ENV')


class AppConfig(BaseSettings):
    APP_BASE_DIR: Optional[str] = os.getcwd()
    APP_PROJECT_NAME: str = "FastApi-App"
    APP_SECRET_KEY: str
    APP_DEBUG: bool
    APP_USE_PROXY: bool = False
    APP_PROXY_SERVER: str = ""
    APP_NO_PROXY: str = '127.0.0.1,localhost'
    APP_USE_TZ: bool = False
    APP_TIMEZONE: str = 'UTC'
    APP_TOKEN_URL: str = "/user/get-token"

    APP_MIDDLEWARE_TRUSTED_HOST: List[str] = ['localhost', '127.0.0.1']
    APP_MIDDLEWARE_LOCAL_IPS: List[str] = ["127.0.0.1", "localhost"]

    SERVER_NAME: str
    SERVER_HOST: AnyHttpUrl

    APP_DB_MARIADB_ENABLED: bool = False
    APP_DB_MARIADB_NAME: Optional[str]
    APP_DB_MARIADB_USER: Optional[str]
    APP_DB_MARIADB_PASSWORD: Optional[str]
    APP_DB_MARIADB_HOST: Optional[str]
    APP_DB_MARIADB_PORT: Optional[str] = '3306'

    APP_DB_POSTGRE_ENABLED: bool = False
    APP_DB_POSTGRE_NAME: Optional[str]
    APP_DB_POSTGRE_USER: Optional[str]
    APP_DB_POSTGRE_PASSWORD: Optional[str]
    APP_DB_POSTGRE_HOST: Optional[str]
    APP_DB_POSTGRE_PORT: Optional[str] = '5432'

    APP_DB_MONGO_ENABLED: bool = False
    APP_DB_MONGO_URI: Optional[str]
    APP_DB_MONGO_NAME: Optional[str]
    APP_DB_MONGO_USER: Optional[str]
    APP_DB_MONGO_PASSWORD: Optional[str]
    APP_DB_MONGO_HOST: Optional[str]
    APP_DB_MONGO_PORT: Optional[str]

    APP_DB_SQLITE_PATH: str = 'sqlite://db.sqlite3'

    APP_REDIS_HOST: str
    APP_REDIS_PORT: str = '6379'
    APP_REDIS_DB: str
    APP_REDIS_PASSWORD: str

    APP_TELEGRAM_BOT_TOKEN: str
    APP_TELEGRAM_NOTIFICATION_CHANNEL: str

    APP_JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    APP_EMAILS_ENABLED: bool = False
    APP_EMAILS_FROM_NAME: Optional[str] = None
    APP_EMAILS_FROM_EMAIL: Optional[str] = None
    APP_EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 1

    APP_SMTP_TLS: bool = True
    APP_SMTP_PORT: Optional[int] = None
    APP_SMTP_HOST: Optional[str] = None
    APP_SMTP_USER: Optional[str] = None
    APP_SMTP_PASSWORD: Optional[str] = None

    class Config:
        case_sensitive = True


# to auto renew data from .env -> keep call command when run some thing
if DEV_ENV:
    settings = AppConfig(_env_file='dev.env')
else:
    settings = AppConfig(_env_file='.env')


if __name__ == "__main__":
    pass
