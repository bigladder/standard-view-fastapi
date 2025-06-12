import threading

import uvicorn
from cachetools import TTLCache
from fastapi import FastAPI, UploadFile
from fastapi.requests import Request
from log import get_log_level, log_debug
from middleware import StandardViewMiddleware, get_session_id
from settings import StandardViewSettings
from starlette.middleware.sessions import SessionMiddleware
from validation import validate_upload_file

settings = StandardViewSettings()

app = FastAPI()
app.add_middleware(StandardViewMiddleware)
app.add_middleware(
    SessionMiddleware, secret_key=settings.secret_key, max_age=settings.session_age, https_only=settings.https_only
)

upload_file_cache: TTLCache[str, UploadFile] = TTLCache(maxsize=settings.cache_size, ttl=settings.session_age)
cache_lock = threading.Lock()


@app.post("/upload")
async def upload(request: Request, upload_file: UploadFile) -> str:
    session_id = get_session_id(request)

    if await validate_upload_file(upload_file):
        log_debug(session_id, "File validation passed")
        with cache_lock:
            upload_file_cache[session_id] = upload_file
            log_debug(session_id, "Added file to cache")
    else:
        log_debug(session_id, "File validation failed")
        return "Upload failed"

    return "Upload complete"


@app.get("/clear")
async def clear(request: Request) -> str:
    session_id = get_session_id(request)

    with cache_lock:
        if session_id in upload_file_cache:
            upload_file_cache.pop(session_id)
            log_debug(session_id, "Removed file from cache")

    request.session.clear()
    log_debug(session_id, "Cleared session")

    return "Clear complete"


if __name__ == "__main__":
    uvicorn.run(app, log_level=get_log_level(settings.log_level))
