import logging
from logging import INFO


class Logs:
        #create a logger to show the execution summary
        logging.basicConfig(level=INFO)
        log_name = 'logs'
        logger = logging.getLogger(log_name)