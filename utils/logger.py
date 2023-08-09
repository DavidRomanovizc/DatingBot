import logging

import loguru

from loader import logger

log_format = "{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message}"
log_levels = ["INFO", "ERROR", "DEBUG"]

for l_level in log_levels:
    loguru.logger.add(f"./logs/{l_level.lower()}.log", level=l_level,
                      colorize=False, format=log_format, encoding="utf-8")


class InterceptHandler(logging.Handler):
    def emit(self, record):
        try:
            level = loguru.logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        loguru.logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


def setup_logger(level="", ignored=""):
    logging.basicConfig(handlers=[InterceptHandler()], level=logging.getLevelName(level))

    for ignore in ignored:
        loguru.logger.disable(ignore)
