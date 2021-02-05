from os import getenv
from os.path import join, abspath, dirname
import sys


ROOT_PATH = abspath(dirname(__file__))

LOGS_DIR = join(ROOT_PATH, 'logs')
SQL_DIR = join(ROOT_PATH, 'sql')

API_TOKEN = getenv("TELEGRAM_API_TOKEN", "")
PROXY_URL = getenv("TELEGRAM_PROXY_URL")

POSTGRES_USER = getenv("POSTGRES_USER", "user_test")
POSTGRES_PASSWORD = getenv("POSTGRES_USER", "password_test")
POSTGRES_DB = getenv("POSTGRES_USER", "test")
POSTGRES_PORT = getenv("POSTGRES_PORT", 5433)
POSTGRESQL_HOST = getenv("POSTGRESQL_HOST", "localhost")


config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "<white>{time:YYYY-MM-DD at HH:mm:ss} | BOT | {message}</white>",
            "colorize": True
        },
        {
            "sink": join(LOGS_DIR, "file.log"),
            "serialize": True,
            "rotation": "3 days",
            "retention": "7 days",
        },
        {
            "sink": join(LOGS_DIR, "error.log"),
            "rotation": "10 MB",
            "retention": "1 days",
            "level": "ERROR"
        },
    ],
    "extra": {"SEND": "SEND"}
}
