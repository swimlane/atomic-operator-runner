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

    def _parse_data_record(self, data, type):
        """Parses the InformationRecord data out of the response stream."""
        extra_dict = {}
        for i in dir(data):
            if not i.startswith('_'):
                extra_dict[i] = str(getattr(data, i))
        if hasattr(data, "message_data"):
            message = data.message_data
        else:
            message = data.message
        data_dict = {
            "type": type,
            "message-data": message,
            "source": data.source if hasattr(data, "source") else None,
            "time_generated": data.time_generated if hasattr(data, "time_generated") else None,
            "user": data.user if hasattr(data, "user") else None,
            "computer": data.computer if hasattr(data, "computer") else None,
            "pid": data.pid if hasattr(data, "pid") else None,
            "native_thread_id": data.native_thread_id if hasattr(data, "native_thread_id") else None,
            "managed_thread_id": data.managed_thread_id if hasattr(data, "managed_thread_id") else None,
            "extra": extra_dict,
        }
        if not self.response.records:
            self.response.records = [BaseRecord(**data_dict)]
        else:
            self.response.records.append(BaseRecord(**data_dict))
        return data_dict

    def __handle_windows_streams(self, stream):
        """Handles processing of all types of message strings from windows systems."""
        return_list = []
        for item in stream.error:
            if item is not None:
                return_list.append({
                    'type': 'error',
                    'value': self._parse_data_record(item)
                })
        for item in stream.debug:
            if item is not None:
                return_list.append({
                    'type': 'debug',
                    'value': self._parse_data_record(item)
                })
        for item in stream.information:
            if item is not None:
                return_list.append({
                    'type': 'information',
                    'value': self._parse_data_record(item)
                })
        for item in stream.verbose:
            if item is not None:
                return_list.append({
                    'type': 'verbose',
                    'value': self._parse_data_record(item)
                })
        for item in stream.warning:
            if item is not None:
                return_list.append({
                    'type': 'warning',
                    'value': self._parse_data_record(item)
                })
        return return_list

    def _create_client(self) -> None:
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

    def run(self, executor: str, command: str) -> Dict[str, object]:
        """Runs the provided command remotely using the provided executor.

        There are several executors that can be used: sh, bash, powershell and cmd

        Args:
            executor (str): The name of the executor to use.
            command (str): The command string to run.

        Raises:
            IncorrectExecutorError: Raised when the provided executor is unknown.
            RemoteRunnerExecutionError: Raised when an error occurs running command remotely.

        Returns:
            Dict: Returns a dictionary of output and error keys.
        """
        return_dict = {}
        self._create_client()
        try:
            if executor == "powershell":
                output, streams, had_errors = self._client.execute_ps(command)
                return self.print_process_output(
                    command=command, 
                    return_code=0 if had_errors is False else had_errors,
                    output=output, 
                    errors=self.__handle_windows_streams(stream=streams)
                )
            elif executor == "cmd":
                stdout, stderr, rc = self._client.execute_cmd(command)
                return self.print_process_output(command=command, return_code=rc, output=stdout, errors=stderr)
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
