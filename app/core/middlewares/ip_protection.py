# -*- coding: utf-8 -*-
from typing import Sequence, Dict, Any
import ipaddress
from fastapi.exceptions import HTTPException
from starlette.datastructures import Headers
from starlette.types import ASGIApp, Message, Receive, Scope, Send
from fastapi.responses import PlainTextResponse, JSONResponse


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
class IpProtectionMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        allowed: Dict[str, Sequence] = None       # (path, [ip])
    ) -> None:
        self.app = app
        self.allowed = allowed
        self.allowed_keys = self.allowed.keys() if self.allowed else None

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> Any:
        if not self.allowed or scope['type'] not in ('http', 'websocket'):
            # pragma: no cover
            await self.app(scope, receive, send)
            return

        matched_path = None
        for path in self.allowed_keys:
            if scope['path'].startswith(path):
                matched_path = path
                break

        if matched_path:
            headers = Headers(scope=scope)
            ip = get_ip(headers)
            if ip != '127.0.0.1' and ip not in self.allowed.get(matched_path):
                response = PlainTextResponse(
                    "Not allowed, contact admin for more information",
                    status_code=403
                )
                await response(scope, receive, send)
                return

        await self.app(scope, receive, send)
