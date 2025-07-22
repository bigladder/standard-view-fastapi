import middleware
import uvicorn
from cache import StandardViewCache, StandardViewCacheFile, StandardViewFileId
from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.requests import Request
from logger import StandardViewLogger
from middleware import StandardViewMiddleware
from settings import StandardViewSettings
from starlette.middleware.sessions import SessionMiddleware
from tree import StandardViewTree, StandardViewTrees
from validation import StandardViewValidator

settings = StandardViewSettings()
logger = StandardViewLogger(settings)
cache = StandardViewCache(settings, logger)
validator = StandardViewValidator(settings, logger)

# Configure logging via lifespan so that it still works when using the fastapi CLI (which is what the Dockerfile uses)
app = FastAPI(lifespan=logger.lifespan_config)
app.add_middleware(StandardViewMiddleware, logger=logger)
app.add_middleware(GZipMiddleware)
app.add_middleware(
    SessionMiddleware, secret_key=settings.secret_key, max_age=settings.session_age, https_only=settings.https_only
)
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], allow_credentials=True
)


@app.get("/exists")
async def exists(request: Request, file_id: StandardViewFileId) -> bool:
    session_id = middleware.get_session_id(request)

    return cache.exists(session_id, file_id)


@app.post("/upload")
async def upload(request: Request, file_id: StandardViewFileId, upload_file: UploadFile) -> None:
    session_id = middleware.get_session_id(request)

    cache_file = StandardViewCacheFile(upload_file)
    cache.add(session_id, file_id, cache_file)

    validator.validate_file(session_id, cache_file)


@app.delete("/remove")
async def remove(request: Request, file_id: StandardViewFileId) -> None:
    session_id = middleware.get_session_id(request)

    cache.remove(session_id, file_id)


@app.get("/tree", response_model_exclude_none=True)
async def tree(request: Request, file_id: StandardViewFileId) -> StandardViewTree:
    session_id = middleware.get_session_id(request)

    cache_file = cache.get(session_id, file_id)

    return StandardViewTree(cache_file)


@app.get("/trees", response_model_exclude_none=True)
async def trees(request: Request) -> StandardViewTrees:
    session_id = middleware.get_session_id(request)

    cache_file0 = cache.get(session_id, 0)
    cache_file1 = cache.get(session_id, 1)

    return StandardViewTrees(cache_file0, cache_file1)


@app.delete("/clear")
async def clear(request: Request) -> None:
    session_id = middleware.get_session_id(request)

    cache.remove(session_id, 0)
    cache.remove(session_id, 1)

    request.session.clear()
    logger.debug(session_id, "Cleared session")


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=80, log_config=None)
