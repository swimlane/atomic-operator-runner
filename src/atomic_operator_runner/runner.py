"""Runs the provided command string locally or remotely."""
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
from typing import Dict, NoReturn

from .base import Base


class Runner(Base):
    """Runs the provided command string locally or remotely."""

    def __init__(
        self,
        platform: str,
        hostname: str = None,
        username: str = None,
        password: str = None,
        verify_ssl: bool = False,
        ssh_key_path: str = None,
        private_key_string: str = None,
        ssh_port: int = 22,
        ssh_timeout: int = 5,
    ) -> NoReturn:
        if platform.lower() not in ["macos", "linux", "windows", "aws"]:
            raise Exception()
        Base.platform = platform.lower()
        Base._run_type = "remote" if hostname else "local"
        Base.hostname = hostname
        Base.username = username
        Base.password = password
        Base.verify_ssl = verify_ssl
        Base.ssh_key_path = ssh_key_path
        Base.private_key_string = private_key_string
        Base.ssh_port = ssh_port
        Base.ssh_timeout = ssh_timeout

    def run(self, command: str, executor: str, cwd: str = None, elevation_required: bool = False) -> Dict[str]:
        """Runs the provided command either locally or remotely based on the provided configuration information.

        Args:
            command (str): The command string to run.
            executor (str): The executor to use when running the provided command.
            cwd (str, optional): The current working directory. Defaults to None.
            elevation_required (bool, optional): Whether or not elevation is required. Defaults to False.

        Returns:
            Dict[str]: Returns a dictionary of the command results, including any errors.
        """
        if elevation_required:
            command = f"{self.ELEVATION_COMMAND_MAP.get(executor)} {command}"
        if Base._run_type == "local":
            from .local import LocalRunner

            return LocalRunner().run(executor=executor, command=command)
        else:
            from .remote import RemoteRunner

            return RemoteRunner().run(executor=executor, command=command)

    def copy(self):
        pass
