import logging

logger = logging.getLogger("uvicorn.error")


def get_log_level(log_level_name: str) -> int:
    return logging.getLevelNamesMapping().get(log_level_name, 20)


def format_message(session_id: str, message: str) -> str:
    return f"session_id={session_id} - {message}"


def log_debug(session_id: str, message: str) -> None:
    logger.debug(format_message(session_id, message))


def log_info(session_id: str, message: str) -> None:
    logger.info(format_message(session_id, message))


def log_warning(session_id: str, message: str) -> None:
    logger.warning(format_message(session_id, message))


def log_error(session_id: str, message: str) -> None:
    logger.error(format_message(session_id, message))


def log_critical(session_id: str, message: str) -> None:
    logger.critical(format_message(session_id, message))
