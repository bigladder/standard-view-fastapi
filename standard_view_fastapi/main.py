import threading

import config
import uvicorn
from cachetools import TTLCache
from fastapi import FastAPI, UploadFile
from fastapi.requests import Request
from middleware import StandardViewMiddleware, get_session_id
from starlette.middleware.sessions import SessionMiddleware
from validation import validate_upload_file

app = FastAPI()
app.add_middleware(StandardViewMiddleware)
app.add_middleware(
    SessionMiddleware, secret_key=config.SECRET_KEY, max_age=config.SESSION_AGE, https_only=config.HTTPS_ONLY
)

upload_file_cache: TTLCache[str, UploadFile] = TTLCache(maxsize=config.CACHE_SIZE, ttl=config.SESSION_AGE)
cache_lock = threading.Lock()


@app.post("/upload")
async def upload(request: Request, upload_file: UploadFile) -> str:
    session_id = get_session_id(request)

    if await validate_upload_file(upload_file):
        print(f"Validation successful for session_id {session_id}")
        with cache_lock:
            upload_file_cache[session_id] = upload_file
            print(f"Cached file for file_id {session_id}")
    else:
        print(f"Validation failed for file_id {session_id}")
        return "Upload failed"

    return "Upload complete"


@app.get("/clear")
async def clear(request: Request) -> str:
    session_id = get_session_id(request)

    with cache_lock:
        if session_id in upload_file_cache:
            upload_file_cache.pop(session_id)
            print(f"Removed session_id {session_id}")

    request.session.clear()
    print("Cleared session")

    return "Clear complete"


if __name__ == "__main__":
    uvicorn.run(app)
