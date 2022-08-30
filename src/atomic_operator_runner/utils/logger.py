"""Logger metaclass and custom formatter."""
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
import logging.config
import os
from logging import DEBUG
from logging import FileHandler
from logging import Formatter
from logging import LogRecord
from typing import Optional

import yaml


class CustomFormatter(Formatter):
    """Logging colored formatter, adapted from https://stackoverflow.com/a/56944256/3638629."""

    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    bold_red = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt: str) -> None:
        """Custom formatter for console output."""
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset,
        }

    def format(self, record: LogRecord) -> str:
        """Used to format a log record object."""
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


class DebugFileHandler(FileHandler):
    """DebugFileHander."""

    def __init__(self, filename: str, mode: str = "a", encoding: Optional[str] = None, delay: bool = False) -> None:
        """Used to debug logging.

        Args:
            filename (str): The filename to log to.
            mode (str, optional): The mode to open the file. Defaults to "a".
            encoding (str, optional): The encoding to use. Defaults to None.
            delay (bool, optional): Delay writing to log file. Defaults to False.
        """
        super().__init__(filename, mode, encoding, delay)

    def emit(self, record: LogRecord) -> None:
        """Used to write a record to a file."""
        if not record.levelno == DEBUG:
            return
        super().emit(record)


class LoggingBase(type):
    """Logging metaclass."""

    def __init__(cls, *args: str) -> None:
        """Logging base metaclass."""
        super().__init__(*args)
        cls.setup_logging()

        # Explicit name mangling
        logger_attribute_name = "_" + cls.__name__ + "__logger"

        # Logger name derived accounting for inheritance for the bonus marks
        logger_name = ".".join([c.__name__ for c in cls.mro()[-2::-1]])

        setattr(cls, logger_attribute_name, logging.getLogger(logger_name))

    def setup_logging(
        cls,
        default_path: str = "./src/atomic_operator_runner/data/logging.yml",
        default_level: int = logging.INFO,
        env_key: str = "LOG_CFG",
    ) -> None:
        """Setup logging configuration."""
        path = os.path.abspath(os.path.expanduser(os.path.expandvars(default_path)))
        value = os.getenv(env_key, None)
        if value:
            path = value
        if os.path.exists(os.path.abspath(path)):
            with open(path) as f:
                config = yaml.safe_load(f.read())
            logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=default_level)
