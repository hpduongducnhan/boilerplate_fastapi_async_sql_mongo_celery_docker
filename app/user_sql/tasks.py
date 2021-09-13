# -*- coding: utf-8 -*-
from celery import shared_task
from app.utils import strings
from core.templates.email.tools import send_reset_password_email


@shared_task(strings.CTASK_SEND_RESET_PASSWORD_EMAIL)
def ctask_send_reset_password_email(email_to: str, email: str, token: str):
    send_reset_password_email(email_to, email, token)
