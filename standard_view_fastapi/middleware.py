import secrets

from fastapi.requests import Request
from logger import StandardViewLogger
from starlette.types import ASGIApp, Receive, Scope, Send


def get_session_id(obj: Request | Scope) -> str:
    if type(obj) is Request:
        return obj.session["session_id"]
    else:
        return obj["session"]["session_id"]


class StandardViewMiddleware:
    def __init__(self, app: ASGIApp, logger: StandardViewLogger) -> None:
        self.app: ASGIApp = app
        self.logger: StandardViewLogger = logger

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        if "session" in scope:
            if "session_id" in scope["session"]:
                session_id = get_session_id(scope)
                self.logger.debug(session_id, "Found existing session")
            else:
                scope["session"]["session_id"] = secrets.token_hex(16)
                session_id = get_session_id(scope)
                self.logger.debug(session_id, "Created new session")

        await self.app(scope, receive, send)
