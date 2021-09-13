# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union
from jose import jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status
from app.config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"


def create_jwt_token(expire: datetime, sub: str):
    return jwt.encode(
        {"exp": expire, "sub": str(sub)},
        settings.APP_SECRET_KEY,
        algorithm=ALGORITHM
    )


#
# ----------------------------------------------------------------------------
#
def decode_jwt_token(token: str):
    try:
        return jwt.decode(
            token, settings.APP_SECRET_KEY, algorithms=[ALGORITHM]
        )
    except jwt.JWTError as e:
        return None


#
# ----------------------------------------------------------------------------
#
def create_access_token(
    subject: Union[str, Any],
    expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.APP_JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    return create_jwt_token(expire, subject)


#
# ----------------------------------------------------------------------------
#
def create_password_reset_token(email: str):
    expires = datetime.utcnow() + timedelta(
        hours=settings.APP_EMAIL_RESET_TOKEN_EXPIRE_HOURS
    )
    return create_jwt_token(expires, email)


#
# ----------------------------------------------------------------------------
#
def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = decode_jwt_token(token)
        return decoded_token["sub"]
    except jwt.JWTError as e:
        return None


#
# ----------------------------------------------------------------------------
#
def extract_jwt_token(token: str) -> Dict:
    try:
        payload = decode_jwt_token(token)
        return payload
    except (jwt.JWTError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


#
# ----------------------------------------------------------------------------
#
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


#
# ----------------------------------------------------------------------------
#
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
