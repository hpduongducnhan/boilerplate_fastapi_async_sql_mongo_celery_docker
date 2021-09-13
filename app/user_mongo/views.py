# -*- coding: utf-8 -*-
import time
from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, APIRouter
from app.config import settings
from app.celery import send_task
from app.utils import strings
from app.core.security import jwt_tools
from app.core.templates.email.tools import send_reset_password_email
from .schemas import ChangePasswordOutModel, RecoverPasswordOutModel
from .schemas import RegisterUserModel, RegisterUserOutModel, Token
from .schemas import ChangePasswordModel, ResetPasswordOutModel
from .schemas import ResetPasswordModel
from .utils import authenticate_user, is_username_existed, get_user_jwt
from .models import User, UserCredentials


router = APIRouter()


#
# ----------------------------------------------------------------------------
#
@router.post('/get-token', response_model=Token)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """OAuth2 compatible token login, get an access token for future requests
    """
    user = await authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(
        minutes=settings.APP_JWT_ACCESS_TOKEN_EXPIRE_MINUTES
    )
    return {
        "access_token": jwt_tools.create_access_token(
            str(user.id), expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


#
# ----------------------------------------------------------------------------
#
@router.post('/google-login', response_model=Token)
async def google_login():
    pass


#
# ----------------------------------------------------------------------------
#
@router.post('/facebook-login', response_model=Token)
async def google_login():
    pass


#
# ----------------------------------------------------------------------------
#
@router.post('/create-user', response_model=RegisterUserOutModel)
async def create_user(user: RegisterUserModel):
    """Create new user"""
    if await is_username_existed(user.username):
        raise HTTPException(402, f"username {user.username} existed")
    # create new user
    new_user = User(**user.dict(exclude={'password'}))
    await new_user.commit()
    # create credential
    new_credential = UserCredentials(
        password=jwt_tools.get_password_hash(user.password),
        user_id=new_user.id
    )
    await new_credential.commit()
    return {'detail': 'created new user', 'username': user.username}


#
# ----------------------------------------------------------------------------
#
@router.post('/verify-token')
async def test_token(user: User = Depends(get_user_jwt)):
    """
    Test jwt token
    """
    print('user', user)
    return {'user_id': str(user.id)}


#
# ----------------------------------------------------------------------------
#
@router.post('/change-password', response_model=ChangePasswordOutModel)
async def change_password(
    payload: ChangePasswordModel,
    user: User = Depends(get_user_jwt)
):
    """Change user password"""

    # check new password matched
    if payload.confirm_password != payload.new_password:
        raise HTTPException(404, "new password is not matched")
    # check old password diff from new password
    if payload.confirm_password == payload.old_password:
        raise HTTPException(404, "new password is old password")
    # check old password is right
    user_credentials = await UserCredentials.find_one({'user_id': user.id})
    if not user_credentials:
        raise HTTPException(404, "User credential not found")

    if not jwt_tools.verify_password(
        payload.old_password,
        user_credentials.password
    ):
        raise HTTPException(404, "wrong old password")

    # save new password
    user_credentials.password = jwt_tools.get_password_hash(
        payload.confirm_password
    )
    await user_credentials.commit()
    return {'detail': 'changed password', 'username': user.username}


#
# ----------------------------------------------------------------------------
#
@router.post(
    '/password-recovery/{email}',
    response_model=RecoverPasswordOutModel
)
async def recover_password(email: str):
    """Recover user password"""
    user = await User.find_one({'email': email})
    if not user:
        raise HTTPException(
            404,
            "The user with this email does not exist in the system.",
        )

    password_reset_token = jwt_tools.create_password_reset_token(email)
    # should use celery to send email for good performance
    send_task(
        strings.CTASK_SEND_RESET_PASSWORD_EMAIL,
        task_args=[email, email, password_reset_token]
    )
    return {"detail": "Password recovery email sent"}


#
# ----------------------------------------------------------------------------
#
@router.post('/reset-password', response_model=ResetPasswordOutModel)
async def reset_password(data: ResetPasswordModel):
    email = jwt_tools.verify_password_reset_token(data.reset_token)
    if not email:
        raise HTTPException(400, "Invalid token")

    user = await User.find_one({'email': email})
    if not user:
        raise HTTPException(400, "User of this email does not exist")

    if not user.is_active:
        raise HTTPException(400, "Inactive user")

    user_credentials = await UserCredentials.find_one({'user_id': user.id})
    if not user_credentials:
        raise HTTPException(404, "UserCredentials not found")

    user_credentials.password = jwt_tools.get_password_hash(data.new_password)
    await user_credentials.commit()
    return {"detail": "new password set"}


# async def delete_user():
#     pass
