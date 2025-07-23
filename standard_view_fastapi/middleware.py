import secrets
from typing import Union

from fastapi.requests import Request
from logger import StandardViewLogger
from starlette.types import ASGIApp, Receive, Scope, Send


def get_session_id(obj: Union[Request, Scope]) -> str:
    if isinstance(obj, Request):
        return obj.session["session_id"]
    else:
        return obj["session"]["session_id"]


class StandardViewMiddleware:
    app: ASGIApp
    logger: StandardViewLogger

    def __init__(self, app: ASGIApp, logger: StandardViewLogger) -> None:
        self.app = app
        self.logger = logger

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        if "session" in scope:
            exists = "session_id" in scope["session"]
            if not exists:
                scope["session"]["session_id"] = secrets.token_hex(16)

            session_id = get_session_id(scope)
            self.logger.debug("Found existing session" if exists else "Created new session", session_id)

        await self.app(scope, receive, send)
