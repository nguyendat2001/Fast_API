import logging.config

logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "file": {
            "class": "logging.FileHandler",
            "filename": "app_log.txt",  # Log file with .txt extension
            "formatter": "default",
        },
    },
    "loggers": {
        "": {  # root logger
            "handlers": ["file"],
            "level": "DEBUG",  # Capture all log levels
        },
    },
}

logging.config.dictConfig(logging_config)

# Example log messages
