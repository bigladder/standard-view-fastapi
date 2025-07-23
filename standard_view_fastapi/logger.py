import logging
import logging.config
from logging import Logger
from typing import Any, AsyncIterator, Optional

import click
import yaml
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from settings import StandardViewSettings


class StandardViewLogger:
    logging_yaml: str
    logger: Logger

    def __init__(self, settings: StandardViewSettings) -> None:
        self.logging_yaml = settings.logging_yaml
        self.logger = logging.getLogger(settings.logger)

    @asynccontextmanager
    async def lifespan_config(self, app: FastAPI) -> AsyncIterator[None]:
        with open(self.logging_yaml) as fs:
            config = yaml.safe_load(fs)
            logging.config.dictConfig(config)
        yield

    def _log(self, level: int, message: str, session_id: Optional[Any], file_id: Optional[Any]) -> None:
        color_message = message

        if file_id is not None:
            file_id_str = str(file_id)
            message = f"(file_id: {file_id_str}) {message}"
            color_message = f"(file_id: {click.style(file_id_str, fg='magenta')}) {color_message}"
        if session_id is not None:
            session_id_str = str(session_id)
            message = f"(session_id: {session_id_str}) {message}"
            color_message = f"(session_id: {click.style(session_id_str, fg='magenta')}) {color_message}"

        self.logger.log(level, message, extra={"color_message": color_message})

    def debug(self, message: str, session_id: Optional[Any] = None, file_id: Optional[Any] = None) -> None:
        self._log(logging.DEBUG, message, session_id, file_id)

    def info(self, message: str, session_id: Optional[Any] = None, file_id: Optional[Any] = None) -> None:
        self._log(logging.INFO, message, session_id, file_id)

    def warning(self, message: str, session_id: Optional[Any] = None, file_id: Optional[Any] = None) -> None:
        self._log(logging.WARNING, message, session_id, file_id)

    def error(self, message: str, session_id: Optional[Any] = None, file_id: Optional[Any] = None) -> None:
        self._log(logging.ERROR, message, session_id, file_id)

    def critical(self, message: str, session_id: Optional[Any] = None, file_id: Optional[Any] = None) -> None:
        self._log(logging.CRITICAL, message, session_id, file_id)
