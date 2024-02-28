import os
import logging
from logging import config as logging_config

from dotenv import load_dotenv


load_dotenv()


class Settings:
    """Класс настроек сервиса."""

    default_dollar_rate: int = 50
    cbr_api_url: str = "https://www.cbr-xml-daily.ru/daily_json.js"

    # настройки redis
    redis_host: str = os.getenv("REDIS_HOST")
    redis_port: int = 6379
    redis_cache_time: int = 10

    # настройки mysql
    mysql_host: str = os.getenv("MYSQL_HOST")
    mysql_port: int = 3306
    mysql_user: str = os.getenv("MYSQL_USER")
    mysql_password: str = os.getenv("MYSQL_PASSWORD")
    mysql_database: str = "api"

    # настройки rabbit
    rabbit_hostname: str = os.getenv("RABBIT_HOST")
    rabbit_port: int = 5672
    rabbit_queue: str = "api_queue"
    rabbit_username: str = os.getenv("RABBIT_USERNAME")
    rabbit_password: str = os.getenv("RABBIT_PASSWORD")

    # настройки логгера
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_DEFAULT_HANDLERS = ["console"]
    LOGGING = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "verbose": {"format": LOG_FORMAT},
        },
        "handlers": {
            "console": {
                "level": "DEBUG",
                "class": "logging.StreamHandler",
                "formatter": "verbose",
            },
        },
        "loggers": {
            "": {
                "handlers": LOG_DEFAULT_HANDLERS,
                "level": "INFO",
            },
            "pika": {
                "propagate": False,
            },
            "backoff": {
                "propagate": False,
            },
        },
        "root": {
            "level": "INFO",
            "formatter": "verbose",
            "handlers": LOG_DEFAULT_HANDLERS,
        },
    }


settings = Settings()

logging_config.dictConfig(settings.LOGGING)
mylogger = logging.getLogger("Consumer")
