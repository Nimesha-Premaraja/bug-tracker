import json
import logging
import os
import sys
from datetime import datetime, timezone


_STANDARD_RECORD_FIELDS = set(logging.LogRecord("", 0, "", 0, "", (), None).__dict__)


class JsonFormatter(logging.Formatter):
    def format(self, record):
        payload = {
            "@timestamp": datetime.fromtimestamp(record.created, timezone.utc).isoformat(),
            "log.level": record.levelname.lower(),
            "log.logger": record.name,
            "message": record.getMessage(),
            "process.pid": record.process,
            "thread.name": record.threadName,
            "log.origin.file.name": record.filename,
            "log.origin.file.line": record.lineno,
            "log.origin.function": record.funcName,
        }

        if record.exc_info:
            payload["error.type"] = record.exc_info[0].__name__
            payload["error.message"] = str(record.exc_info[1])
            payload["error.stack_trace"] = self.formatException(record.exc_info)

        if record.stack_info:
            payload["error.stack_trace"] = record.stack_info

        for key, value in record.__dict__.items():
            if key not in _STANDARD_RECORD_FIELDS and key not in payload:
                payload[key] = value

        return json.dumps(payload, default=str)


def configure_logging():
    log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.addHandler(handler)
    root_logger.setLevel(log_level)

    for logger_name in ("flask.app", "werkzeug", "app"):
        named_logger = logging.getLogger(logger_name)
        named_logger.handlers.clear()
        named_logger.propagate = True
        named_logger.setLevel(log_level)

    logging.getLogger("sqlalchemy").setLevel(os.environ.get("SQLALCHEMY_LOG_LEVEL", "WARNING").upper())
