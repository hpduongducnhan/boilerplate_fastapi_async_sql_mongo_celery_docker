# -*- coding: utf-8 -*-
import logging
from typing import Any, Dict
import emails
from emails.template import JinjaTemplate
from app.config import settings
import os


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.APP_EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.APP_EMAILS_FROM_NAME, settings.APP_EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.APP_SMTP_HOST, "port": settings.APP_SMTP_PORT}
    if settings.APP_SMTP_TLS:
        smtp_options["tls"] = True
    if settings.APP_SMTP_USER:
        smtp_options["user"] = settings.APP_SMTP_USER
    if settings.APP_SMTP_PASSWORD:
        smtp_options["password"] = settings.APP_SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")
    print(f"send email result: {response}")


def send_test_email(email_to: str) -> None:
    project_name = settings.APP_PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(os.path.join(
        settings.APP_BASE_DIR,
        'app', 'core', 'templates', 'email', 'build',
        'test_email.html'
    ), 'r') as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.APP_PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.APP_PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(os.path.join(
        settings.APP_BASE_DIR,
        'app', 'core', 'templates', 'email', 'build',
        'reset_password.html'
    ), 'r') as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.APP_PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.APP_EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(email_to: str, username: str, password: str) -> None:
    project_name = settings.APP_PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(os.path.join(
        settings.APP_BASE_DIR,
        'app', 'core', 'templates', 'email', 'build',
        'new_account.html'
    ), 'r') as f:
        template_str = f.read()
    link = settings.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.APP_PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )
