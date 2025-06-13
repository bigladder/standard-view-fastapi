import logging
import logging.config

import click
import yaml
from settings import StandardViewSettings

logger = logging.getLogger("uvicorn.error")


def init(settings: StandardViewSettings) -> None:
    with open(settings.logging_yaml) as fs:
        config = yaml.safe_load(fs)
        logging.config.dictConfig(config)


def log(level: int, message: str, session_id: str | None) -> None:
    color_message = message

    if type(session_id) is str:
        message = f"{message} (session_id: {session_id})"
        color_message = f"{color_message} (session_id: {click.style(session_id, fg='magenta', bold=True)})"

    logger.log(level, message, extra={"color_message": color_message})


def debug(message: str, session_id: str | None) -> None:
    log(logging.DEBUG, message, session_id)


def info(message: str, session_id: str | None) -> None:
    log(logging.INFO, message, session_id)


def warning(message: str, session_id: str | None) -> None:
    log(logging.WARNING, message, session_id)


def error(message: str, session_id: str | None) -> None:
    log(logging.ERROR, message, session_id)


def critical(message: str, session_id: str | None) -> None:
    log(logging.CRITICAL, message, session_id)
