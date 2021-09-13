# -*- coding: utf-8 -*-
from typing import Sequence
from fastapi.middleware import Middleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from .ip_protection import IpProtectionMiddleware
from .brute_force_defender import BruteForceDefenderMiddleware
from app.config import settings


middlewares = [
    Middleware(
        BruteForceDefenderMiddleware,
        lock_time_minutes=5,
        checking_time_minutes=60,
        failure_limit=10,
        protected_paths={
            '/user/get-token': 401,
        }
    ),
    Middleware(
        IpProtectionMiddleware,
        allowed={
            '/docs': settings.APP_MIDDLEWARE_LOCAL_IPS,
            '/admin': settings.APP_MIDDLEWARE_LOCAL_IPS
        }
    ),
    Middleware(
        TrustedHostMiddleware,
        allowed_hosts=settings.APP_MIDDLEWARE_TRUSTED_HOST,
        www_redirect=True
    ),
    Middleware(
        CORSMiddleware,
        allow_origins=(),         # : typing.Sequence[str]
        allow_methods=("GET",),   # : typing.Sequence[str]
        allow_headers=(),         # : typing.Sequence[str]
        allow_credentials=False,   # : bool
        allow_origin_regex=None,  # : str
        expose_headers=(),        # : typing.Sequence[str]
        max_age=600,              # : int
    ),
    Middleware(
        SessionMiddleware,
        secret_key=settings.APP_SECRET_KEY,   # : typing.Union[str, Secret]
        session_cookie="session",             # : str
        max_age=14 * 24 * 60 * 60,            # : int # 14 days, in seconds
        same_site="lax",                      # : str
        https_only=False,                     # : bool
    )
]
