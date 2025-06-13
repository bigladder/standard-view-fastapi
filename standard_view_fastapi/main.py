import threading

import log
import middleware
import uvicorn
import validation
from cachetools import TTLCache
from fastapi import FastAPI, UploadFile
from fastapi.requests import Request
from middleware import StandardViewMiddleware
from settings import StandardViewSettings
from starlette.middleware.sessions import SessionMiddleware

settings = StandardViewSettings()
log.init(settings)
upload_file_cache: TTLCache[str, UploadFile] = TTLCache(maxsize=settings.cache_size, ttl=settings.session_age)
cache_lock = threading.Lock()

app = FastAPI()
app.add_middleware(StandardViewMiddleware)
app.add_middleware(
    SessionMiddleware, secret_key=settings.secret_key, max_age=settings.session_age, https_only=settings.https_only
)


@app.post("/upload")
async def upload(request: Request, upload_file: UploadFile) -> str:
    session_id = middleware.get_session_id(request)

    if await validation.validate_upload_file(upload_file):
        log.debug("File validation passed", session_id)
        with cache_lock:
            upload_file_cache[session_id] = upload_file
            log.debug("Added file to cache", session_id)
    else:
        log.debug("File validation failed", session_id)
        return "Upload failed"

    return "Upload complete"


@app.delete("/clear")
async def clear(request: Request) -> str:
    session_id = middleware.get_session_id(request)

    with cache_lock:
        if session_id in upload_file_cache:
            upload_file_cache.pop(session_id)
            log.debug("Removed file from cache", session_id)

    request.session.clear()
    log.debug("Cleared session", session_id)

    return "Clear complete"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=80, log_config=None)
