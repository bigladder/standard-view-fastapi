import logging
import logging.config
from logging import Logger
from typing import AsyncIterator

import click
import yaml
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from settings import StandardViewSettings


class StandardViewLogger:
    def __init__(self, settings: StandardViewSettings) -> None:
        self.logging_yaml: str = settings.logging_yaml
        self.logger: Logger = logging.getLogger(settings.logger)

    @asynccontextmanager
    async def lifespan_config(self, app: FastAPI) -> AsyncIterator[None]:
        with open(self.logging_yaml) as fs:
            config = yaml.safe_load(fs)
            logging.config.dictConfig(config)
        yield

    def log(self, level: int, session_id: str | None, message: str) -> None:
        color_message = message

        if type(session_id) is str:
            message = f"{message} (session_id: {session_id})"
            color_message = f"{color_message} (session_id: {click.style(session_id, fg='magenta', bold=True)})"

        self.logger.log(level, message, extra={"color_message": color_message})

    def debug(self, session_id: str | None, message: str) -> None:
        self.log(logging.DEBUG, session_id, message)

    def info(self, session_id: str | None, message: str) -> None:
        self.log(logging.INFO, session_id, message)

    def warning(self, session_id: str | None, message: str) -> None:
        self.log(logging.WARNING, session_id, message)

    def error(self, session_id: str | None, message: str) -> None:
        self.log(logging.ERROR, session_id, message)

    def critical(self, session_id: str | None, message: str) -> None:
        self.log(logging.CRITICAL, session_id, message)
