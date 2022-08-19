"""Base class for all classes in this project."""
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
import platform
import re
from typing import Dict
from typing import Optional

from .models import RunnerResponse
from .utils.logger import LoggingBase


class Base(metaclass=LoggingBase):
    """Base class to all other classes within this project."""

    COMMAND_MAP = {
        "command_prompt": {
            "windows": "C:\\Windows\\System32\\cmd.exe",
            "linux": "/bin/sh",
            "macos": "/bin/sh",
            "default": "/bin/sh",
        },
        "powershell": {"windows": "C:\\Windows\\System32\\WindowsPowerShell\\v1.0\\powershell.exe"},
        "sh": {"linux": "/bin/sh", "macos": "/bin/sh"},
        "bash": {"linux": "/bin/bash", "macos": "/bin/bash"},
    }
    ELEVATION_COMMAND_MAP = {
        "powershell": "Start-Process PowerShell -Verb RunAs;",
        "cmd": "cmd.exe /c",
        "command_prompt": "cmd.exe /c",
        "sh": "sudo",
        "bash": "sudo",
        "ssh": "sudo",
    }

    # properties used throughout the project
    hostname: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None
    verify_ssl: Optional[bool] = False
    ssh_key_path: Optional[str] = None
    private_key_string: Optional[str] = None
    ssh_port: Optional[int] = 22
    ssh_timeout: Optional[int] = 5
    platform: Optional[str] = None
    _run_type: Optional[str] = None
    response = RunnerResponse()

    def clean_output(self, data: bytes) -> str:
        """Decodes data and strips CLI garbage from returned outputs and errors.

        Args:
            data (bytes): A output or error returned from subprocess

        Returns:
            str: A cleaned string which will be displayed on the console and in logs
        """
        return_data = data.decode("utf-8", "ignore") if isinstance(data, bytes) else data
        # Remove Windows CLI garbage
        return_data = re.sub(
            r"Microsoft\ Windows\ \[version .+\]\r?\nCopyright.*(\r?\n)+[A-Z]\:.+?\>", "", str(return_data)
        )
        # formats strings with newline and return characters
        return_data = re.sub(r"(\r?\n)*[A-Z]\:.+?\>", "", str(return_data))
        return return_data

    def print_process_output(self, command: str, return_code: int, output: bytes, errors: bytes) -> Dict[str, str]:
        """Outputs the appropriate outputs if they exists to the console and log files.

        Args:
            command (str): The command which was ran by subprocess
            return_code (int): The return code from subprocess
            output (bytes): Output from subprocess which is typically in bytes
            errors (bytes, optional): Errors from subprocess which is typically in bytes

        Returns:
            dict: A dictionary containing the output and any errors.
        """
        self.__logger.debug("Processing command output.")
        return_dict = {
            "output": None,
            "error": None,
        }
        if errors:
            cleaned_errors = self.clean_output(errors)
        else:
            cleaned_errors = ""
        if return_code == 127:
            error_string = f"\n\nCommand Not Found: {command} returned exit code {return_code}: \n"
            error_string += f"Errors: {cleaned_errors}/nOutput: {output}"
            return_dict.update({"error": error_string})
            self.__logger.warning(return_dict["error"])
        if output or errors:
            if output:
                return_dict["output"] = self.clean_output(output)
                self.__logger.info("\n\nOutput: {}".format(return_dict["output"]))
            else:
                return_dict[
                    "error"
                ] = f"\n\nCommand: {command} returned exit code {return_code}: \n{self.clean_output(cleaned_errors)}"
                self.__logger.warning(return_dict["error"])
        else:
            self.__logger.info("(No output)")
        return return_dict

    def get_local_system_platform(self) -> str:
        """Identifies the local systems operating system platform.

        Returns:
            str: The current/local systems operating system platform
        """
        os_name = platform.system().lower()
        if os_name == "darwin":
            return "macos"
        return os_name
