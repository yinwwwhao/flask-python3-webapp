import logging
from sql_configs import mode


if mode == 'dev':
    level = logging.INFO
else:
    level = logging.ERROR

logger = logging.getLogger()

log_format = "[%(levelname)s] %(asctime)s [%(filename)s:%(lineno)d, %(funcName)s] %(message)s"


LOG_FILE = "run_log.log"
logging.basicConfig(filename=LOG_FILE,
                    filemode="a",
                    format=log_format,
                    level=level,
                    encoding='utf-8')


logging.info("begin service")