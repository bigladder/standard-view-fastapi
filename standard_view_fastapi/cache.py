import threading
from threading import Lock
from typing import Annotated

import annotated_types
from cachetools import TTLCache
from fastapi import UploadFile
from logger import StandardViewLogger
from settings import StandardViewSettings

StandardViewFileId = Annotated[int, annotated_types.Ge(0), annotated_types.Le(1)]


class StandardViewCacheFile:
    def __init__(self, upload_file: UploadFile):
        self.content: bytes = upload_file.file.read()
        self.filename: str = upload_file.filename or str()
        self.content_type: str | None = upload_file.content_type


class StandardViewCache:
    def __init__(self, settings: StandardViewSettings, logger: StandardViewLogger) -> None:
        self.cache: TTLCache[str, StandardViewCacheFile] = TTLCache(
            maxsize=settings.cache_size, ttl=settings.session_age
        )
        self.lock: Lock = threading.Lock()
        self.logger: StandardViewLogger = logger

    def exists(self, session_id: str) -> bool:
        with self.lock:
            exists = session_id in self.cache

        self.logger.debug(session_id, "File exists in cache" if exists else "File does not exist in cache")
        return exists

    def add(self, session_id: str, cache_file: StandardViewCacheFile) -> None:
        with self.lock:
            exists = session_id in self.cache
            self.cache[session_id] = cache_file

        self.logger.debug(session_id, "Updated file in cache" if exists else "Added file to cache")

    def get(self, session_id: str) -> StandardViewCacheFile | None:
        with self.lock:
            exists = session_id in self.cache
            cache_file = self.cache.get(session_id)

        self.logger.debug(session_id, "Retrieved file from cache" if exists else "File does not exist in cache")
        return cache_file

    def remove(self, session_id: str) -> None:
        with self.lock:
            exists = session_id in self.cache
            if exists:
                self.cache.pop(session_id)

        self.logger.debug(session_id, "Removed file from cache" if exists else "File does not exist in cache")
