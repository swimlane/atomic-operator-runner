"""Used to run commands remotely."""
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
import atexit

from paramiko.client import AutoAddPolicy
from paramiko.client import SSHClient
from paramiko.pkey import PKey
from pypsrp.client import Client

from .base import Base
from .processor import Processor
from .utils.exceptions import IncorrectExecutorError
from .utils.exceptions import RemoteRunnerExecutionError


class RemoteRunner(Base):
    """Used to run command remotely."""

    def _get_paramiko_client(self) -> SSHClient:
        """Creates a paramiko client object."""
        _client = SSHClient()
        _client.set_missing_host_key_policy(AutoAddPolicy())
        if Base.config.ssh_key_path:
            _client.connect(
                Base.config.hostname,
                port=Base.config.ssh_port,
                username=Base.config.username,
                key_filename=Base.config.ssh_key_path,
                timeout=Base.config.ssh_timeout,
            )
        elif Base.config.private_key_string:
            _client.connect(
                Base.config.hostname,
                port=Base.config.ssh_port,
                username=Base.config.username,
                pkey=PKey(data=Base.config.private_key_string),
                timeout=Base.config.ssh_timeout,
            )
        elif Base.config.password:
            _client.connect(
                Base.config.hostname,
                port=Base.config.ssh_port,
                username=Base.config.username,
                password=Base.config.password,
                timeout=Base.config.ssh_timeout,
            )
        return _client

    def _get_pypsrp_client(self) -> Client:
        """Creates a client for the defined platform operating system."""
        return Client(
            Base.config.hostname,
            username=Base.config.username,
            password=Base.config.password,
            ssl=Base.config.verify_ssl,
        )

    def run(self, executor: str, command: str) -> None:
        """Runs the provided command remotely using the provided executor.

        There are several executors that can be used: sh, bash, powershell and cmd

        Args:
            executor (str): The name of the executor to use.
            command (str): The command string to run.

        Raises:
            IncorrectExecutorError: Raised when the provided executor is unknown.
            RemoteRunnerExecutionError: Raised when an error occurs running command remotely.
        """
        try:
            if executor == "powershell":
                # Creating a pypsrp client and executing powershell command remotely.
                output, streams, had_errors = self._get_pypsrp_client().execute_ps(command)
                # saving the output from the execution to our RunnerResponse object
                if isinstance(had_errors, bool):
                    had_errors = 0 if had_errors is False else 1
                Processor(command=command, executor=executor, return_code=had_errors, output=output, errors=streams)
            elif executor == "cmd":
                stdout, stderr, rc = self._get_pypsrp_client().execute_cmd(command)
                Processor(command=command, executor=executor, return_code=rc, output=stdout, errors=stderr)
            elif executor == "sh" or executor == "bash":
                atexit.register(self._close_paramiko_client)
                client = self._get_paramiko_client()
                stdin, stdout, stderr = client.exec_command(command=command)
                Processor(
                    command=command,
                    executor=executor,
                    return_code=stdout.channel.recv_exit_status(),
                    output=stdout.read(),
                    errors=stderr.read(),
                )
                stdin.flush()
                self._close_paramiko_client(client=client)
            else:
                raise IncorrectExecutorError(
                    f"The provided executor of '{executor}' is not one of sh, bash, powershell or cmd"
                )
        except Exception as e:
            raise RemoteRunnerExecutionError(exception=e) from e

    def _close_paramiko_client(self, client: SSHClient) -> None:
        """Closes the paramiko client."""
        client.close()
        atexit.unregister(self._close_paramiko_client)
