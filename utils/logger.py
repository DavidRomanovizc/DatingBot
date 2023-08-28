import logging

import betterlogging as bl
import loguru

log_format = "{time:MMMM D, YYYY > HH:mm:ss} | {level} | {message}"
log_levels = ["INFO", "ERROR", "DEBUG"]

for l_level in log_levels:
    loguru.logger.add(
        f"./logs/{l_level.lower()}.log",
        level=l_level,
        colorize=False,
        format=log_format,
        encoding="utf-8",
    )


def setup_logger(level=logging.INFO, ignored=""):
    bl.basic_colorized_config(level=level)
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    for ignore in ignored:
        loguru.logger.disable(ignore)
