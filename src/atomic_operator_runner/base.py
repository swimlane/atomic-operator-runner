"""Base class for all classes in this project."""
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
import inspect
import platform
from typing import Dict

from .models import Host
from .models import RunnerResponse
from .utils.logger import LoggingBase


class Base(metaclass=LoggingBase):
    """Base class to all other classes within this project."""

    COMMAND_MAP: Dict[str, Dict[str, str]] = {
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
    ELEVATION_COMMAND_MAP: Dict[str, str] = {
        "powershell": "Start-Process PowerShell -Verb RunAs;",
        "cmd": "cmd.exe /c",
        "command_prompt": "cmd.exe /c",
        "sh": "sudo",
        "bash": "sudo",
        "ssh": "sudo",
    }

    config: Host
    response: RunnerResponse = RunnerResponse()

    def get_local_system_platform(self) -> str:
        """Identifies the local systems operating system platform.

        Returns:
            str: The current/local systems operating system platform
        """
        os_name = platform.system().lower()
        if os_name == "darwin":
            return "macos"
        return os_name

    def log(self, val, level="info") -> None:
        """Used to centralize logging across components.

        We identify the source of the logging class by inspecting the calling stack.

        Args:
            val (str): The log value string to output.
            level (str, optional): The log level. Defaults to "info".
        """
        component = None
        parent = inspect.stack()[1][0].f_locals.get("self", None)
        component = parent.__class__.__name__
        try:
            getattr(getattr(parent, f"_{component}__logger"), level)(val)
        except AttributeError as ae:
            getattr(self.__logger, level)(val + ae)
