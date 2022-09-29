# -*-coding:utf-8-*-

import logging


def init_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    #logger.addFilter(HostnameFilter())
    f = logging.Formatter('%(asctime)s %(levelname)s [%(pathname)s/%(funcName)s] ==> %(message)s')
    s = logging.StreamHandler()
    s.setFormatter(f)
    logger.addHandler(s)
    return logger


logger = init_logger()
