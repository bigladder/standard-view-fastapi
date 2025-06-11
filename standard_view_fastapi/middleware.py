import secrets

from fastapi.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send


def get_session_id(request: Request) -> str:
    return request.session["session_id"]


class StandardViewMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        if "session" in scope:
            if "session_id" in scope["session"]:
                print(f"Found session_id {scope['session']['session_id']}")
            else:
                scope["session"]["session_id"] = secrets.token_hex(16)
                print(f"Created session_id {scope['session']['session_id']}")

        await self.app(scope, receive, send)
