from time import strftime
import logging


def format_datetime_fields(datetimefield):
    return datetimefield.strftime('%d-%m-%Y')


logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "console": {
                "format": "%(asctime)s - level: %(levelname)s - message: %(message)s from: %(funcName)-8s - %(name)-8s",
                "datefmt": "%H:%M:%S",
            },
            "file": {
                "format": "%(asctime)s %(levelname)-8s - message: %(message)8s - from: %(funcName)-8s - (%(filename)-12s)",
                "datefmt": "%d-%b-%Y %H:%M:%S",
            },
        },
        "handlers": {
            "console": {"class": "logging.StreamHandler", "formatter": "console"},
            "file": {
                "level": "DEBUG",
                "class": "logging.FileHandler",
                "formatter": "file",
                "filename": "./recipe_blog.log",
            },
        },
        "loggers": {"": {"level": "DEBUG", "handlers": ["console", "file"]}},
    }
)

logger = logging.getLogger(__name__)