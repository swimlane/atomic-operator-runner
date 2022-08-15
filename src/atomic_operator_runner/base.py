import re

from .utils.logger import LoggingBase


class Base(metaclass=LoggingBase):

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
    hostname = None
    username = None
    password = None
    verify_ssl = False
    ssh_key_path = None
    private_key_string = None
    ssh_port = 22
    ssh_timeout = 5
    platform = None
    _run_type = None

    def clean_output(self, data):
        """Decodes data and strips CLI garbage from returned outputs and errors

        Args:
            data (str): A output or error returned from subprocess

        Returns:
            str: A cleaned string which will be displayed on the console and in logs
        """
        if data:
            # Remove Windows CLI garbage
            data = re.sub(
                r"Microsoft\ Windows\ \[version .+\]\r?\nCopyright.*(\r?\n)+[A-Z]\:.+?\>",
                "",
                data.decode("utf-8", "ignore"),
            )
            # formats strings with newline and return characters
            return re.sub(r"(\r?\n)*[A-Z]\:.+?\>", "", data)
        return data

    def print_process_output(self, command: str, return_code: int, output, errors):
        """Outputs the appropriate outputs if they exists to the console and log files

        Args:
            command (str): The command which was ran by subprocess
            return_code (int): The return code from subprocess
            output (bytes): Output from subprocess which is typically in bytes
            errors (bytes): Errors from subprocess which is typically in bytes
        """
        return_dict = {}
        if return_code == 127:
            error_string = f"\n\nCommand Not Found: {command} returned exit code {return_code}: \n"
            error_string += f"Errors: {self.clean_output(errors)}/nOutput: {output}"
            return_dict.update({
                "error": error_string
            })
            self.__logger.warning(return_dict["error"])
        if output or errors:
            if output:
                return_dict["output"] = self.clean_output(output)
                self.__logger.info("\n\nOutput: {}".format(return_dict["output"]))
            else:
                return_dict[
                    "error"
                ] = f"\n\nCommand: {command} returned exit code {return_code}: \n{self.clean_output(errors)}"
                self.__logger.warning(return_dict["error"])
        else:
            self.__logger.info("(No output)")
        return return_dict
