"""Runs the provided command string locally or remotely."""
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
import atexit
import os
import platform
from datetime import datetime
from typing import List
from typing import Optional

from .base import Base
from .models import Host
from .models import RunnerResponse
from .models import TargetEnvironment
from .utils.exceptions import IncorrectPlatformError


class Runner(Base):
    """Runs the provided command string locally or remotely."""

    responses: List[RunnerResponse] = []

    def __init__(
        self,
        platform: str,
        hostname: Optional[str] = None,
        username: Optional[str] = None,
        password: Optional[str] = None,
        ssh_key_path: Optional[str] = None,
        private_key_string: Optional[str] = None,
        verify_ssl: bool = False,
        ssh_port: int = 22,
        ssh_timeout: int = 5,
    ) -> None:
        """Used to run commands either locally or remotely.

        The provided configuration options determine where the provided command(s) will be ran.

        Args:
            platform (str): The platform the commands will be ran against. Options are macos, linux, windows and aws.
            hostname (str, optional): The hostname to run commands remotely on. Defaults to None.
            username (str, optional): The username to connect to the remote host on. Defaults to None.
            password (str, optional): The password used to connect to the remote host. Defaults to None.
            verify_ssl (bool, optional): Whether or not to verify SSL/TLS. Defaults to False.
            ssh_key_path (str, optional): A string path to an ssh key. Defaults to None.
            private_key_string (str, optional): The private key string value for ssh connection. Defaults to None.
            ssh_port (int, optional): The port used for SSH connections. Defaults to 22.
            ssh_timeout (int, optional): The timeout for SSH connections. Defaults to 5.

        Raises:
            IncorrectPlatformError: Raised when the provided platform is not a correct option.
        """
        if platform.lower() not in ["macos", "linux", "windows", "aws"]:
            raise IncorrectPlatformError(provided_platform=platform)
        Base.config = Host(
            hostname=hostname,
            username=username,
            password=password,
            verify_ssl=verify_ssl,
            ssh_key_path=ssh_key_path,
            private_key_string=private_key_string,
            ssh_port=ssh_port,
            ssh_timeout=ssh_timeout,
            platform=platform.lower(),
            run_type="remote" if hostname else "local",
        )
        atexit.register(self._return_response)

    def _return_response(self) -> None:
        """Returns JSON of the RunnerResponse class object."""
        print(self.response.json())

    def _get_username(self) -> str:
        """Attempts to determine the current logged in user name.

        Returns:
            str: A username string.
        """
        try:
            import getpass

            return getpass.getuser()
        except Exception as e:
            self.__logger.debug(f"Unable to retrieve username from getpass.getuser method. {e}")
        try:
            return os.getlogin()
        except Exception as e:
            self.__logger.debug(f"Unable to retrieve username from os.getlogin method. {e}")
        return "Unknown"

    def run(
        self, command: str, executor: str, cwd: Optional[str] = None, elevation_required: bool = False
    ) -> List[str]:
        """Runs the provided command either locally or remotely based on the provided configuration information.

        Args:
            command (str): The command string to run.
            executor (str): The executor to use when running the provided command.
            cwd (str, optional): The current working directory. Defaults to None.
            elevation_required (bool, optional): Whether or not elevation is required. Defaults to False.

        Returns:
            List[str]: Returns a list of dictionaries of the command results, including any errors.
        """
        Base.response = RunnerResponse(
            start_timestamp=datetime.now(),
            environment=TargetEnvironment(
                platform=Base.config.platform,
                hostname=Base.config.hostname if Base.config.hostname else platform.node(),
                user=Base.config.username if Base.config.username else self._get_username(),
            ),
        )
        if elevation_required:
            command = f"{self.ELEVATION_COMMAND_MAP.get(executor)} {command}"
        Base.response.elevation_required = elevation_required
        if Base.config.run_type == "local":
            from .local import LocalRunner

            LocalRunner().run(executor=executor, command=command, cwd=cwd)
        else:
            from .remote import RemoteRunner

            RemoteRunner().run(executor=executor, command=command)
        atexit.unregister(self._return_response)
        self.responses.append(self.response)
        return [x.json() for x in self.responses]

    def copy(self) -> None:
        """Used to copy files from one system to another."""
        pass
