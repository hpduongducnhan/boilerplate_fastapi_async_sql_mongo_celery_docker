# -*- coding: utf-8 -*-
from typing import Sequence, Dict, Any
import ipaddress
from datetime import timedelta
from fastapi.exceptions import HTTPException
from starlette.datastructures import Headers
from starlette.requests import Request
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from starlette.responses import HTMLResponse
from fastapi.responses import PlainTextResponse
from app.core.database.redis import redis_client


#
# ----------------------------------------------------------------------------
#
def get_ip(headers: Headers):
    ip = headers.get('x-real-ip')
    if ip and isinstance(ip, str) and ipaddress.ip_address(ip):
        return ip
    ip = headers.get('x-forwarded-for')
    if ip and isinstance(ip, str):
        ip = ip.split(',')[0]
        if ipaddress.ip_address(ip):
            return ip
    ip = headers.get('REMOTE_ADDR')
    if ip and isinstance(ip, str):
        return ip.strip()
    return '127.0.0.1'


#
# ----------------------------------------------------------------------------
#
async def is_ip_blocked(ip: str) -> bool:
    if await redis_client.get(f'brute_force_defender_lock_{ip}'):
        return True
    return False


#
# ----------------------------------------------------------------------------
#
async def got_error_at_protected(
    ip: str,
    limitation: int,
    checking_minutes: int,
    lock_time_minutes: int
) -> bool:
    failure_counter = await redis_client.get(
        f'brute_force_defender_failure_{ip}_counter'
    )
    print('got_error_at_protected ip', ip, failure_counter)
    if not failure_counter:
        # keep check key in redis
        await redis_client.setex(
            f'brute_force_defender_failure_{ip}_counter',
            timedelta(minutes=checking_minutes),
            1
        )
        print('add checking')
    else:
        try:
            failure_counter = int(failure_counter)
        except Exception as e:
            raise e

        ttl_key = await redis_client.ttl(f'brute_force_defender_failure_{ip}_counter')

        if failure_counter >= limitation:
            await block_ip(ip, lock_time_minutes)
            await redis_client.delete(f'brute_force_defender_failure_{ip}_counter')
        else:
            await redis_client.setex(
                f'brute_force_defender_failure_{ip}_counter',
                timedelta(seconds=ttl_key if ttl_key else 60*checking_minutes),
                failure_counter + 1
            )
#
# ----------------------------------------------------------------------------
#


async def block_ip(ip: str, lock_minutes) -> None:
    await redis_client.setex(
        f'brute_force_defender_lock_{ip}',
        timedelta(minutes=lock_minutes),
        1
    )


# def mark_login_error(ip: str, username: str) -> bool:
#     pass


# async def set_body(request: Request, body: bytes):
#     async def receive() -> Message:
#         return {"type": "http.request", "body": body}
#     request._receive = receive


# async def get_body(request: Request) -> bytes:
#     body = await request.body()
#     await set_body(request, body)
#     return body


#
# ----------------------------------------------------------------------------
#
class BruteForceDefenderMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        protected_paths: Dict[str, int] = None,      # Dict[url_path, error_code],
        lock_time_minutes: int = 60,                  # 0 means lock forever
        failure_limit: int = 10,
        checking_time_minutes: int = 60
    ) -> None:
        self.app = app
        self.protected_paths = protected_paths
        self.lock_time_minutes = lock_time_minutes
        self.failure_limit = failure_limit
        self.checking_time_minutes = checking_time_minutes

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> Any:
        if (
            not self.protected_paths
            or scope['type'] not in ('http', 'websocket')
        ):
            # pragma: no cover
            await self.app(scope, receive, send)
            return

        got_protected_path = False
        if scope['path'] in self.protected_paths:
            got_protected_path = True
            ip = get_ip(Headers(scope=scope))
            # check if ip is blocked
            if await is_ip_blocked(ip):
                response = PlainTextResponse(
                    "You are blocked, Try again later",
                    status_code=403
                )
                await response(scope, receive, send)
                return

        # print('come here')
        # before view
        async def _send(message: Message):
            if got_protected_path:
                if (
                    message.get('status')
                    and message.get('status') == self.protected_paths[scope['path']]
                ):
                    await got_error_at_protected(
                        ip,
                        self.failure_limit,
                        self.checking_time_minutes,
                        self.lock_time_minutes
                    )
            await send(message)

        await self.app(scope, receive, _send)
