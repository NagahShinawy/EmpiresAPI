import logging
from logging import handlers

logger = logging.getLogger('')
logger.setLevel(logging.INFO)
format = logging.Formatter("%(process)d || %(module)s || %(lineno)d || %(funcName)s %(asctime)s || %(name)s || %(levelname)s || %(message)s", datefmt="%d-%b-%y %H:%M:%S")

ch = logging.StreamHandler()
ch.setFormatter(format)
logger.addHandler(ch)

fh = handlers.RotatingFileHandler('logs.log', maxBytes=(1048576*5), backupCount=7)
fh.setFormatter(format)
logger.addHandler(fh)
