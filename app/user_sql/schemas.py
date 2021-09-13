# -*- coding: utf-8 -*-
from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None


class RegisterUserModel(BaseModel):
    username: str
    password: str
    full_name: Optional[str]
    email: Optional[EmailStr]
    phone_number: Optional[str]
    date_of_birth: Optional[datetime]


class RegisterUserOutModel(BaseModel):
    username: str
    detail: str


class ChangePasswordOutModel(RegisterUserOutModel):
    pass


class RecoverPasswordOutModel(BaseModel):
    detail: str


class ResetPasswordModel(BaseModel):
    reset_token: str
    new_password: str


class ResetPasswordOutModel(BaseModel):
    detail: str


class ChangePasswordModel(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str
