"""Used to run commands remotely."""
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
from typing import Dict

import paramiko
from pypsrp.client import Client

from .base import Base
from .utils.exceptions import IncorrectExecutorError
from .utils.exceptions import RemoteRunnerExecutionError


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

    def run(self, executor: str, command: str) -> Dict[str]:
        """Runs the provided command remotely using the provided executor.

        There are several executors that can be used: sh, bash, powershell and cmd

        Args:
            executor (str): The name of the executor to use.
            command (str): The command string to run.

        Raises:
            IncorrectExecutorError: Raised when the provided executor is unknown.
            RemoteRunnerExecutionError: Raised when an error occurs running command remotely.

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
        except Exception as e:
            raise RemoteRunnerExecutionError(exception=e) from e
        return return_dict
