import logging
import logging.config
from pathlib import Path

import yaml


class LoggerFactory:
    _CONFIG_PATH = Path(__file__).parent / "logging.yaml"

    TRACE = logging.DEBUG - 5
    SUCCESS = logging.INFO + 5
    FATAL = logging.CRITICAL + 10

    logging.addLevelName(TRACE, "TRACE")
    logging.addLevelName(SUCCESS, "SUCCESS")
    logging.addLevelName(FATAL, "FATAL")

    def _trace(self, message, *args, **kwargs):
        if self.isEnabledFor(5):
            self._log(5, message, args, **kwargs)

    def _success(self, message, *args, **kwargs):
        if self.isEnabledFor(logging.INFO + 5):
            self._log(logging.INFO + 5, message, args, **kwargs)

    def _fatal(self, message, *args, **kwargs):
        if self.isEnabledFor(logging.CRITICAL + 10):
            self._log(logging.CRITICAL + 10, message, args, **kwargs)

    logging.Logger.trace = _trace
    logging.Logger.success = _success
    logging.Logger.fatal = _fatal

    with open(_CONFIG_PATH) as _f:
        logging.config.dictConfig(yaml.safe_load(_f))

    @classmethod
    def get_logger(cls, identifier: str):
        return logging.getLogger(identifier)


class LoggingObject:
    logger: logging.Logger

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.logger = LoggerFactory.get_logger(cls.__name__)

    def __init__(self):
        self.logger = LoggerFactory.get_logger(self.__class__.__name__)
