import threading
from threading import Lock

from cachetools import TTLCache
from fastapi import UploadFile
from logger import StandardViewLogger
from settings import StandardViewSettings


class StandardViewCache:
    def __init__(self, settings: StandardViewSettings, logger: StandardViewLogger) -> None:
        self.cache: TTLCache[str, UploadFile] = TTLCache(maxsize=settings.cache_size, ttl=settings.session_age)
        self.lock: Lock = threading.Lock()
        self.logger: StandardViewLogger = logger

    def exists(self, session_id: str) -> bool:
        with self.lock:
            exists = session_id in self.cache

        self.logger.debug(session_id, "File exists in cache" if exists else "File does not exist in cache")
        return exists

    def add(self, session_id: str, upload_file: UploadFile) -> None:
        with self.lock:
            exists = session_id in self.cache
            self.cache[session_id] = upload_file

        self.logger.debug(session_id, "Updated file in cache" if exists else "Added file to cache")

    def remove(self, session_id: str) -> None:
        with self.lock:
            exists = session_id in self.cache
            if exists:
                self.cache.pop(session_id)

        self.logger.debug(session_id, "Removed file from cache" if exists else "File does not exist in cache")
