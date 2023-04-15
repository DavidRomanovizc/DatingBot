import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=1)

formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')

handler.setFormatter(formatter)

handler.setLevel(logging.ERROR)

logger = logging.getLogger('myapp')

logger.setLevel(logging.INFO)

logger.addHandler(handler)
