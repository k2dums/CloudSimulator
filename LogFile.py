import logging


def createLogHandler(job_name,log_file):
    logger = logging.getLogger(job_name)
    logger.setLevel(logging.INFO)
    ## create a file handler ##
    handler = logging.FileHandler(log_file)
    ## create a logging format ##
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
