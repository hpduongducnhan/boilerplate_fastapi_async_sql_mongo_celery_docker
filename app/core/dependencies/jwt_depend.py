# -*- coding: utf-8 -*-
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.security import jwt_tools
from app.config import settings


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=settings.APP_TOKEN_URL
)


async def verify_token(token: str = Depends(oauth2_scheme)):
    payload = jwt_tools.extract_jwt_token(token)
    print('payload', payload)
    return payload
