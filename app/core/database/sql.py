# -*- coding: utf-8 -*-
from typing import Type
from tortoise.models import Model
from tortoise import Tortoise
from app.config import settings


# detail in link bellow
# https://tortoise.github.io/getting_started.html
# https://github.com/tortoise/tortoise-orm
# https://github.com/tortoise/aerich


class TortoiseRouter:
    def db_for_read(self, model: Type[Model]):
        # switch between model to get database for reading purpose
        return "default"

    def db_for_write(self, model: Type[Model]):
        # switch between model to get database for reading purpose
        return "default"


TORTOISE_ORM_CONFIG = {
    'connections': {
        # Dict format for connection
        'default': settings.APP_DB_SQLITE_PATH,
        # 'postgresql': {
        #     'engine': 'tortoise.backends.asyncpg',
        #     'credentials': {
        #         'host': settings.APP_DB_POSTGRE_HOST,
        #         'port': settings.APP_DB_POSTGRE_PORT,
        #         'user': settings.APP_DB_POSTGRE_USER,
        #         'password': settings.APP_DB_POSTGRE_PASSWORD,
        #         'database': settings.APP_DB_POSTGRE_NAME,
        #     }
        # },
        # 'mariadb': {
        #     'engine': 'tortoise.backends.mysql',
        #     'credentials': {
        #         'host': settings.APP_DB_MARIADB_HOST,
        #         'port': settings.APP_DB_MARIADB_PORT,
        #         'user': settings.APP_DB_MARIADB_USER,
        #         'password': settings.APP_DB_MARIADB_PASSWORD,
        #         'database': settings.APP_DB_MARIADB_NAME,
        #     }
        # }
    },
    'apps': {
        'user': {
            'models': [
                'app.user_sql.models',
            ],
            'default_connection': 'default',
        },
        # 'user_postgresql': {
        #     'models': [
        #         'app.user_postgresql.models',
        #     ],
        #     'default_connection': 'postgresql',
        # },
        # 'user_mariadb': {
        #     'models': [
        #         'app.user_mariadb.models',
        #     ],
        #     'default_connection': 'mariadb',
        # },
        'aerich': {
            'models': [
                "aerich.models"
            ],
            'default_connection': 'default',
        }
    },
    # change class above TortoiseRouter if you need
    # be carefull! if you enable routers
    # router will decide which database model should work with
    # https://tortoise.github.io/router.html
    # 'routers': ['app.database.sql.TortoiseRouter'],
    'use_tz': settings.APP_USE_TZ,
    'timezone': settings.APP_TIMEZONE
}


async def connect_databases():
    await Tortoise.init(TORTOISE_ORM_CONFIG)


async def init_db():
    # run this after connect
    # ignore this function if you use aerich commandline aerich init-db
    await Tortoise.generate_schemas()
