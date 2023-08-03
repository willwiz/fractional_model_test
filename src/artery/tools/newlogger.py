import sys
import enum
import logging
from typing import Literal
from pathlib import Path


def touch(file:str):
    Path(file).touch()


class LogLevel(enum.Enum):
    NULL = 0
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARN = logging.WARN
    ERROR = logging.ERROR
    FATAL = logging.FATAL
    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

def create_logger(logger_name:str='null', level:LogLevel=LogLevel.NULL, console:bool=True, mode:Literal['a', 'w']='w') -> logging.Logger:
    """
    Method to return a custom logger with the given name and level
    """
    format="%(asctime)s::%(levelname)-8s >> %(module)s-%(lineno)d[%(funcName)s]: %(message)s"
    datefmt="%y-%m-%d %H:%M:%S"
    log_format = logging.Formatter(fmt=format, datefmt=datefmt)
    if (level is LogLevel.NULL) or logger_name == 'null':
        logger = logging.getLogger('null')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logging.NullHandler())  # read below for reason
        logger.propagate = False
    else:
        if mode == 'w':
            open(logger_name, 'w').close()
        logger = logging.getLogger(logger_name)
        logger.setLevel(level.value)
        # Creating and adding the file handler
        file_handler = logging.FileHandler(logger_name, mode='a',encoding='utf-8')
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
    # Creating and adding the console handler
    if console:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)
    return logger