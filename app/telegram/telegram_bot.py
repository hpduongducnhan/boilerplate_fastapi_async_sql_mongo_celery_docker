# -*- coding: utf-8 -*-
import logging
from aiogram import Bot, Dispatcher, executor, types
from app.config import settings


if settings.APP_USE_PROXY:
    bot = Bot(token=settings.APP_TELEGRAM_BOT_TOKEN, proxy=settings.APP_PROXY_SERVER)
else:
    bot = Bot(token=settings.APP_TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)


async def send_message(msg: str, channel: str = settings.APP_TELEGRAM_NOTIFICATION_CHANNEL):
    await bot.send_message(channel, msg)
