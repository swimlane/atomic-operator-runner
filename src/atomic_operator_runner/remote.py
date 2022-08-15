"""Used to run commands remotely."""
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
from typing import Dict

import paramiko
from paramiko.ssh_exception import (
    BadAuthenticationType,
    NoValidConnectionsError,
    AuthenticationException,
    PasswordRequiredException,
)
from pypsrp.client import Client
from pypsrp.exceptions import AuthenticationError, WinRMTransportError, WSManFaultError

from requests.exceptions import RequestException

from .base import Base
from .utils.exceptions import IncorrectExecutorError


class RemoteRunner(Base):
    """Used to run command remotely."""

    def _create_client(self):
        """Creates a client for the defined platform operating system."""
        if Base.platform == "windows":
            self._client = Client(
                Base.hostname,
                username=Base.username,
                password=Base.password,
                ssl=Base.verify_ssl,
            )
        else:
            self._client = paramiko.SSHClient()
            self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            if Base.ssh_key_path:
                self._client.connect(
                    Base.hostname,
                    port=Base.ssh_port,
                    username=Base.username,
                    key_filename=Base.ssh_key_path,
                    timeout=Base.ssh_timeout,
                )
            elif Base.private_key_string:
                self._client.connect(
                    Base.hostname,
                    port=Base.ssh_port,
                    username=Base.username,
                    pkey=Base.private_key_string,
                    timeout=Base.ssh_timeout,
                )
            elif Base.password:
                self._client.connect(
                    Base.hostname,
                    port=Base.ssh_port,
                    username=Base.username,
                    password=Base.password,
                    timeout=Base.ssh_timeout,
                )

    def run(
        self,
        executor: str,
        command: str,
    ) -> Dict[str]:
        """Runs the provided command remotely using the provided executor.

        There are several executors that can be used: sh, bash, powershell and cmd

        Args:
            executor (str): The name of the executor to use.
            command (str): The command string to run.

        Raises:
            IncorrectExecutorError: Raised when the provided executor is unknown.

        Returns:
            Dict[str]: Returns a dictionary of output and error keys.
        """
        return_dict = {}
        self._create_client()
        try:
            if executor == "powershell":
                output, streams, had_errors = self._client.execute_ps(command)
                return_dict.update(
                    {
                        "output": output,
                        "error": streams,
                    }
                )
            elif executor == "cmd":
                stdout, stderr, rc = self._client.execute_cmd(command)
                return_dict.update(
                    {
                        "output": stdout,
                        "error": stderr,
                    }
                )
            elif executor == "ssh":
                stdin, stdout, stderr = self._client.exec_command(command=command)
                return_dict.update(
                    {
                        "output": stdout,
                        "error": stderr,
                    }
                )
            else:
                raise IncorrectExecutorError(
                    f"The provided executor of '{executor}' is not one of sh, bash, powershell or cmd"
                )
        except NoValidConnectionsError as ec:
            error_string = f"SSH Error - Unable to connect to {Base.hostname} - Received {type(ec).__name__}"
            self.__logger.debug(f"Full stack trace: {ec}")
            self.__logger.warning(error_string)
            return {"error": error_string}
        except AuthenticationException as ea:
            error_string = f"SSH Error - Unable to authenticate to host - {Base.hostname} "
            error_string += f"- Received {type(ea).__name__}"
            self.__logger.debug(f"Full stack trace: {ea}")
            self.__logger.warning(error_string)
            return {"error": error_string}
        except BadAuthenticationType as eb:
            error_string = f"SSH Error - Unable to use provided authentication type to host - {Base.hostname} "
            error_string += f"- Received {type(eb).__name__}"
            self.__logger.debug(f"Full stack trace: {eb}")
            self.__logger.warning(error_string)
            return {"error": error_string}
        except PasswordRequiredException as ep:
            error_string = f"SSH Error - Must provide a password to authenticate to host - {Base.hostname} "
            error_string += f"- Received {type(ep).__name__}"
            self.__logger.debug(f"Full stack trace: {ep}")
            self.__logger.warning(error_string)
            return {"error": error_string}
        except AuthenticationError as ewa:
            error_string = (
                f"Windows Error - Unable to authenticate to host - {Base.hostname} - Received {type(ewa).__name__}"
            )
            self.__logger.debug(f"Full stack trace: {ewa}")
            self.__logger.warning(error_string)
            return {"error": error_string}
        except WinRMTransportError as ewt:
            error_string = f"Windows Error - Error occurred during transport on host - {Base.hostname} "
            error_string += f"- Received {type(ewt).__name__}"
            self.__logger.debug(f"Full stack trace: {ewt}")
            self.__logger.warning(error_string)
            return {"error": error_string}
        except WSManFaultError as ewf:
            error_string = f"Windows Error - Received WSManFault information from host - {Base.hostname} "
            error_string += f"- Received {type(ewf).__name__}"
            self.__logger.debug(f"Full stack trace: {ewf}")
            self.__logger.warning(error_string)
            return {"error": error_string}
        except RequestException as re:
            error_string = f"Request Exception - Connection Error to the configured host - {Base.hostname} "
            error_string += f"- Received {type(re).__name__}"
            self.__logger.debug(f"Full stack trace: {re}")
            self.__logger.warning(error_string)
            return {"error": error_string}
        except Exception as ex:
            error_string = f"Unknown Error - Received an unknown error from host - {Base.hostname} "
            error_string += f"- Received {type(ex).__name__}"
            self.__logger.debug(f"Full stack trace: {ex}")
            self.__logger.warning(error_string)
            return {"error": error_string}
        return return_dict
