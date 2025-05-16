import logging
import logging.handlers
from typing import Union
import os
import sys
from config import LOG_LEVEL, MS_NAME

# basicConfig = logging.basicConfig
# DEBUG = logging.DEBUG
# INFO = logging.INFO
# WARN = logging.WARN
# WARNING = logging.WARNING
# ERROR = logging.ERROR
# CRITICAL = logging.CRITICAL

try:
    import colorlog

    my_fmt: Union[
        colorlog.ColoredFormatter, logging.Formatter
    ] = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime).22s %(name)s:%(levelname).4s:%(module)s: %(lineno)d: %(msg)s"
    )
except ImportError:
    my_fmt = logging.Formatter(
        "%(asctime).22s %(name)s:%(levelname).4s:%(module)s: %(lineno)d: %(msg)s"
    )


def getSysLogger(name="root", loglevel=LOG_LEVEL):
    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(int(loglevel))
    if logger.handlers:
        return logger
    hdlr = logging.StreamHandler()
    hdlr.setFormatter(my_fmt)
    logger.addHandler(hdlr)

    if logger.name == "root":
        logger.info(
            "Running: {} {}".format(
                os.path.basename(sys.argv[0]), " ".join(sys.argv[1:])
            )
        )
    return logger


class CustomGCPFormatter(logging.Formatter):
    _default_fmt = "%(asctime).22s %(name)s:%(levelname).4s:%(module)s: %(lineno)d: %(msg)s"  # noqa
    def __init__(self):
        super().__init__(
            fmt=CustomGCPFormatter._default_fmt, datefmt="%H:%M:%S", style="%"
        )

    def format(self, record):
        # args = record.args.copy()
        # record.args = {}
        # print(record.__dict__)
        # print(args)
        logmsg = super(CustomGCPFormatter, self).format(record)
        return {"msg": logmsg, "args": record.args}


def getGCPLogger(name="root", loglevel=LOG_LEVEL):

    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(int(loglevel))

    if logger.handlers:
        return logger

    import google.cloud.logging

    client = google.cloud.logging.Client()
    hdlr = client.get_default_handler()

    hdlr.setFormatter(my_fmt)
    logger.addHandler(hdlr)

    return logger


def getGCPJsonLogger(name="root", loglevel=LOG_LEVEL):

    logger = logging.getLogger(name)
    logger.propagate = False
    logger.setLevel(int(loglevel))

    if logger.handlers:
        return logger

    import google.cloud.logging

    client = google.cloud.logging.Client()
    hdlr = client.get_default_handler()

    hdlr.setFormatter(CustomGCPFormatter())
    logger.addHandler(hdlr)
    return logger


logger_name = MS_NAME

if os.environ.get("OP_ENV") == "GCP":
    getLogger = getGCPLogger
    logger = getGCPLogger(logger_name)
    logger_g = getGCPJsonLogger(logger_name + "-gcp")
else:
    getLogger = getSysLogger
    logger = getSysLogger(logger_name)
    logger_g = logger

logger.info(f"logger level is {logger.level}")
