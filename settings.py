import os
import logging
from logging.config import dictConfig

if os.name == "nt":
    client_log_file_path = 'logs/client.log'
    debug_log_file_fath = 'logs/debug.log'
elif os.name == "posix" :
    log_file_path = '/home/admin/logs/client.log'
    debug_log_file_fath = '/home/admin/logs/debug.log'
else:
    log_file_path = 'logs/client.log'
    debug_log_file_fath = 'logs/debug.log'

LOGGING_CONFIG = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": " %(asctime)-1s %(levelname)s - %(module)-1s : %(message)s"
        },
        "standard": {
            "format": "%(levelname)-1s - %(name)-1s : %(message)s"
            },
    },
    "handlers": {
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
        "console2": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": client_log_file_path,
            "mode": "w",
            "formatter": "standard",
        },
        "file2": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "filename": debug_log_file_fath,
            "mode": "w",
            "formatter": "verbose",
        },
    },
    "loggers": {
        "client": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": False
            },
        "debug": {
            "handlers": ["console2", "file2"],
            "level": "DEBUG",
            "propagate": False
            },
        "discord": {
            "handlers": ["console2", "file2"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

dictConfig(LOGGING_CONFIG)