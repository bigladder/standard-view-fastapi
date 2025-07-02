import middleware
import uvicorn
from cache import StandardViewCache, StandardViewCacheFile
from fastapi import FastAPI, UploadFile
from fastapi.requests import Request
from logger import StandardViewLogger
from middleware import StandardViewMiddleware
from settings import StandardViewSettings
from starlette.middleware.sessions import SessionMiddleware
from validation import StandardViewValidator

settings = StandardViewSettings()
logger = StandardViewLogger(settings)
cache = StandardViewCache(settings, logger)
validator = StandardViewValidator(settings, logger)

app = FastAPI(lifespan=logger.lifespan_config)
app.add_middleware(StandardViewMiddleware, logger=logger)
app.add_middleware(
    SessionMiddleware, secret_key=settings.secret_key, max_age=settings.session_age, https_only=settings.https_only
)


@app.get("/exists")
async def exists(request: Request) -> bool:
    session_id = middleware.get_session_id(request)

    return cache.exists(session_id)


@app.post("/upload")
async def upload(request: Request, upload_file: UploadFile) -> str:
    session_id = middleware.get_session_id(request)

    cache_file = StandardViewCacheFile(upload_file)
    is_valid, validation_messages = validator.validate_file(session_id, cache_file)

    if is_valid:
        cache.add(session_id, cache_file)

    return validation_messages


@app.delete("/clear")
async def clear(request: Request) -> None:
    session_id = middleware.get_session_id(request)

    cache.remove(session_id)

    request.session.clear()
    logger.debug(session_id, "Cleared session")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=80, log_config=None)
