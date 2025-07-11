import threading
from threading import Lock
from typing import Annotated, Optional

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
        self.content_type: Optional[str] = upload_file.content_type


class StandardViewCache:
    def __init__(self, settings: StandardViewSettings, logger: StandardViewLogger) -> None:
        self.cache: TTLCache[str, dict[StandardViewFileId, StandardViewCacheFile]] = TTLCache(
            maxsize=settings.cache_size, ttl=settings.session_age
        )
        self.lock: Lock = threading.Lock()
        self.logger: StandardViewLogger = logger

    def _exists(self, session_id: str, file_id: StandardViewFileId) -> bool:
        return session_id in self.cache and file_id in self.cache[session_id]

    def exists(self, session_id: str, file_id: StandardViewFileId) -> bool:
        with self.lock:
            exists = self._exists(session_id, file_id)

        self.logger.debug(session_id, "File exists in cache" if exists else "File does not exist in cache")
        return exists

    def add(self, session_id: str, file_id: StandardViewFileId, cache_file: StandardViewCacheFile) -> None:
        with self.lock:
            exists = self._exists(session_id, file_id)
            if session_id not in self.cache:
                self.cache[session_id] = {}
            self.cache[session_id][file_id] = cache_file

        self.logger.debug(session_id, "Updated file in cache" if exists else "Added file to cache")

    def remove(self, session_id: str, file_id: StandardViewFileId) -> None:
        with self.lock:
            exists = self._exists(session_id, file_id)
            if exists:
                self.cache[session_id].pop(file_id)

        self.logger.debug(session_id, "Removed file from cache" if exists else "File does not exist in cache")

    def get(self, session_id: str, file_id: StandardViewFileId) -> Optional[StandardViewCacheFile]:
        with self.lock:
            exists = self._exists(session_id, file_id)
            if exists:
                cache_file = self.cache[session_id][file_id]

        self.logger.debug(session_id, "Retrieved file from cache" if exists else "File does not exist in cache")
        return cache_file
