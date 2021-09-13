# -*- coding: utf-8 -*-
from app.core.database.sql import connect_databases
from app.telegram.telegram_bot import send_message
from app.config import settings
from app.celery import send_task
from app.utils import strings


async def event_01_connect_sql_database():
    await connect_databases()


async def event_02_connect_mongo_database():
    if settings.APP_DB_MONGO_ENABLED:
        from app.core.database.mongo import umongo_cnx


async def event_99_notify_app_stopped():
    await send_message('FastApi-Celery-App Stopped')


events = [v for k, v in locals().items() if k.startswith('event_')]
