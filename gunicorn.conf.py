import multiprocessing
import os


bind = "0.0.0.0:5000"
workers = int(os.environ.get("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))
accesslog = "-"
errorlog = "-"
loglevel = os.environ.get("LOG_LEVEL", "info").lower()
logconfig_dict = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "json": {
            "()": "app.logging_config.JsonFormatter",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": "ext://sys.stderr",
        },
        "error_console": {
            "class": "logging.StreamHandler",
            "formatter": "json",
            "stream": "ext://sys.stderr",
        },
    },
    "root": {
        "level": loglevel.upper(),
        "handlers": ["console"],
    },
    "loggers": {
        "gunicorn.error": {
            "handlers": ["error_console"],
            "level": loglevel.upper(),
            "propagate": False,
        },
    },
}

access_log_format = (
    '{"log.level":"info",'
    '"log.logger":"gunicorn.access",'
    '"event.dataset":"gunicorn.access",'
    '"client.ip":"%(h)s",'
    '"http.request.method":"%(m)s",'
    '"url.original":"%(U)s%(q)s",'
    '"http.version":"%(H)s",'
    '"http.response.status_code":%(s)s,'
    '"event.duration":%(D)s,'
    '"message":"gunicorn access"}'
)
