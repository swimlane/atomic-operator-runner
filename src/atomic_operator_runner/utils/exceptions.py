"""Exceptions."""
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)

from typing import Any

from paramiko.ssh_exception import AuthenticationException
from paramiko.ssh_exception import BadAuthenticationType
from paramiko.ssh_exception import NoValidConnectionsError
from paramiko.ssh_exception import PasswordRequiredException
from pypsrp.exceptions import AuthenticationError
from pypsrp.exceptions import WinRMTransportError
from pypsrp.exceptions import WSManFaultError
from requests.exceptions import RequestException


class IncorrectExecutorError(Exception):
    """Raised when the incorrect executor is used."""

    pass


class IncorrectPlatformError(Exception):
    """Raised when the incorrect platform is provided."""

    def __init__(self, provided_platform: str) -> None:
        """Raises when the provided platforms is not correct."""
        from ..base import Base

        Base.__logger.critical(
            f"The provided platform of '{provided_platform}' is not one of macos, linux, windows or aws"
        )


class RemoteRunnerExecutionError(Exception):
    """Raised when an error occurs executing a command remotely."""

    def __init__(self, exception: Any) -> None:
        """Raises when an error occurs running a command remotely."""
        from ..base import Base

        if exception is NoValidConnectionsError:
            error_string = (
                f"SSH Error - Unable to connect to {Base.config.hostname} - Received {type(exception).__name__}"
            )
            Base.__logger.debug(f"Full stack trace: {exception}")
            Base.__logger.warning(error_string)
        elif exception is AuthenticationException:
            error_string = f"SSH Error - Unable to authenticate to host - {Base.config.hostname} "
            error_string += f"- Received {type(exception).__name__}"
            Base.__logger.debug(f"Full stack trace: {exception}")
            Base.__logger.warning(error_string)
        elif exception is BadAuthenticationType:
            error_string = f"SSH Error - Unable to use provided authentication type to host - {Base.config.hostname} "
            error_string += f"- Received {type(exception).__name__}"
            Base.__logger.debug(f"Full stack trace: {exception}")
            Base.__logger.warning(error_string)
        elif exception is PasswordRequiredException:
            error_string = f"SSH Error - Must provide a password to authenticate to host - {Base.config.hostname} "
            error_string += f"- Received {type(exception).__name__}"
            Base.__logger.debug(f"Full stack trace: {exception}")
            Base.__logger.warning(error_string)
        elif exception is AuthenticationError:
            error_string = f"Windows Error - Unable to authenticate to host - {Base.config.hostname} "
            error_string += f"- Received {type(exception).__name__}"
            Base.__logger.debug(f"Full stack trace: {exception}")
            Base.__logger.warning(error_string)
        elif exception is WinRMTransportError:
            error_string = f"Windows Error - Error occurred during transport on host - {Base.config.hostname} "
            error_string += f"- Received {type(exception).__name__}"
            Base.__logger.debug(f"Full stack trace: {exception}")
            Base.__logger.warning(error_string)
        elif exception is WSManFaultError:
            error_string = f"Windows Error - Received WSManFault information from host - {Base.config.hostname} "
            error_string += f"- Received {type(exception).__name__}"
            Base.__logger.debug(f"Full stack trace: {exception}")
            Base.__logger.warning(error_string)
        elif exception is RequestException:
            error_string = f"Request Exception - Connection Error to the configured host - {Base.config.hostname} "
            error_string += f"- Received {type(exception).__name__}"
            Base.__logger.debug(f"Full stack trace: {exception}")
            Base.__logger.warning(error_string)
        else:
            error_string = f"Unknown Error - Received an unknown error from host - {Base.config.hostname} "
            error_string += f"- Received {type(exception).__name__}"
            Base.__logger.debug(f"Full stack trace: {exception}")
            Base.__logger.warning(error_string)
