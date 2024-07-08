import logging

from src.core.utils import (LOG_FILE, LOG_FORMATTER, LOGGER_NAME)


log = logging.getLogger(name=LOGGER_NAME)
log.setLevel(logging.DEBUG)

LOG_FILE_HANDLER = logging.FileHandler(filename=LOG_FILE, mode='+a', encoding='utf-8')
LOG_FILE_HANDLER.setFormatter(LOG_FORMATTER)

log.addHandler(LOG_FILE_HANDLER)
log.info(msg='Inicializado.')
