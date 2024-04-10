import sys

from loguru import logger as loguru_logger

from app.config import settings


class Loggin:
    def __init__(self) -> None:
        if settings.DEBUG:
            self.level = "DEBUG"
        else:
            self.level = "INFO"

    def setup_logger(self):
        loguru_logger.remove()
        loguru_logger.add(sink=sys.stdout, level=self.level)

        if settings.LOG:
            loguru_logger.add(
                settings.LOGS_ROOT + "/log_{time}.log",
                level=self.level,
                rotation="5 MB"
            )
        return loguru_logger


loggin = Loggin()
logger = loggin.setup_logger()
