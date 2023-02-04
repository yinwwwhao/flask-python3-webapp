import logging


logger = logging.getLogger()

log_format = "[%(levelname)s] %(asctime)s [%(filename)s:%(lineno)d, %(funcName)s] %(message)s"


LOG_FILE = "run_log.log"
logging.basicConfig(filename=LOG_FILE,
                    filemode="a",
                    format=log_format,
                    level=logging.INFO,
                    encoding='utf-8')


logging.info("begin log service")