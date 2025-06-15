import middleware
import uvicorn
from cache import StandardViewCache
from fastapi import FastAPI, UploadFile
from fastapi.requests import Request
from logger import StandardViewLogger
from middleware import StandardViewMiddleware
from settings import StandardViewSettings
from starlette.middleware.sessions import SessionMiddleware

settings = StandardViewSettings()
logger = StandardViewLogger(settings)
cache = StandardViewCache(settings, logger)

app = FastAPI(lifespan=logger.lifespan_config)
app.add_middleware(StandardViewMiddleware, logger=logger)
app.add_middleware(
    SessionMiddleware, secret_key=settings.secret_key, max_age=settings.session_age, https_only=settings.https_only
)


@app.post("/upload")
async def upload(request: Request, upload_file: UploadFile) -> str:
    session_id = middleware.get_session_id(request)

    file_bytes = await upload_file.read()
    file_content = file_bytes.decode()

    if "metadata" in file_content:
        logger.debug(session_id, "File validation passed")
        cache.add(session_id, upload_file)
    else:
        logger.debug(session_id, "File validation failed")
        return "Upload failed"

    return "Upload complete"


@app.delete("/clear")
async def clear(request: Request) -> str:
    session_id = middleware.get_session_id(request)

    cache.remove(session_id)

    request.session.clear()
    logger.debug(session_id, "Cleared session")

    return "Clear complete"


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=80, log_config=None)
