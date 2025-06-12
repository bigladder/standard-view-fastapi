import secrets

from fastapi.requests import Request
from log import log_debug
from starlette.types import ASGIApp, Receive, Scope, Send


def get_session_id(obj: Request | Scope) -> str:
    if type(obj) is Request:
        return obj.session["session_id"]
    else:
        return obj["session"]["session_id"]


class StandardViewMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        if "session" in scope:
            if "session_id" in scope["session"]:
                log_debug(get_session_id(scope), "Found existing session")
            else:
                scope["session"]["session_id"] = secrets.token_hex(16)
                log_debug(get_session_id(scope), "Created new session")

        await self.app(scope, receive, send)
