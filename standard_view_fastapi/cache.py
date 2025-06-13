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

    def add(self, session_id: str, upload_file: UploadFile) -> None:
        with self.lock:
            if session_id in self.cache:
                self.cache[session_id] = upload_file
                self.logger.debug(session_id, "Updated file in cache")
            else:
                self.cache.setdefault(session_id, upload_file)
                self.logger.debug(session_id, "Added file to cache")

    def remove(self, session_id: str) -> None:
        with self.lock:
            if session_id in self.cache:
                self.cache.pop(session_id)
                self.logger.debug(session_id, "Removed file from cache")
            else:
                self.logger.debug(session_id, "File not found in cache")
