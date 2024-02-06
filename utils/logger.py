import logging

import betterlogging as bl


def setup_logger(level=logging.INFO, ignored=""):
    bl.basic_colorized_config(level=level)
    logging.basicConfig(
        level=logging.INFO,
        format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
    )
    for ignore in ignored:
        logging.getLogger(ignore).disabled = True
