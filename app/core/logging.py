import json
import logging
import os
from logging.config import dictConfig
from typing import Any, Mapping

from app.core.config import settings


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log: dict[str, Any] = {
            "timestamp": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        data = getattr(record, "data", None)
        if data is not None:
            log["data"] = data

        return json.dumps(log, ensure_ascii=False, default=str)


def setup_logging() -> None:
    os.makedirs(settings.log_dir, exist_ok=True)
    dict_config: Mapping[str, Any] = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": JsonFormatter,
                "datefmt": "%Y-%m-%dT%H:%M:%S",
            },
        },
        "handlers": {
            "file": {
                "class": "logging.handlers.RotatingFileHandler",
                "formatter": "json",
                "filename": os.path.join(settings.log_dir, "app.log"),
                "maxBytes": 5 * 1024 * 1024,
                "backupCount": 5,
                "encoding": "utf-8",
            },
        },
        "root": {
            "level": settings.log_level,
            "handlers": ["file"],
        },
    }

    dictConfig(dict_config)


def get_logger(name: str | None = None) -> logging.Logger:
    return logging.getLogger(name if name else __name__)
