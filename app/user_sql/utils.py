# -*- coding: utf-8 -*-
from typing import Optional
from fastapi import HTTPException
from fastapi.param_functions import Depends
from app.core.security import jwt_tools
from app.core.dependencies import jwt_depend
from .models import User, UserCredentials


async def authenticate_user(username: str, password: str) -> Optional[User]:
    incorect_user_pass = "Incorrect username or password"
    # get user from db
    user = await User.get_or_none(username=username)
    if not user:
        raise HTTPException(401, incorect_user_pass)
    # check user active
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")
    # get user credentials from db
    user_credentials = await UserCredentials.get_or_none(user=user)
    if not user_credentials:
        raise HTTPException(401, incorect_user_pass)
    # verify password
    if not jwt_tools.verify_password(password, user_credentials.password):
        raise HTTPException(401, incorect_user_pass)
    return user


#
# ----------------------------------------------------------------------------
#
async def is_username_existed(username: str) -> bool:
    user = await User.get_or_none(username=username)
    if user:
        return True
    return False


#
# ----------------------------------------------------------------------------
#
async def get_user_jwt(jwt_payload: str = Depends(jwt_depend.verify_token)):
    if not jwt_payload:
        raise HTTPException(status_code=401, detail="Token is undefined")

    user = await User.get_or_none(id=jwt_payload.get('sub'))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="Inactive user")
    return user
