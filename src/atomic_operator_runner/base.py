"""Base class for all classes in this project."""
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
import platform
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

    def get_local_system_platform(self) -> str:
        """Identifies the local systems operating system platform.

        Returns:
            str: The current/local systems operating system platform
        """
        os_name = platform.system().lower()
        if os_name == "darwin":
            return "macos"
        return os_name
