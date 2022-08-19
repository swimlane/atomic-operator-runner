"""Runs a command on a local system."""
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
import subprocess
from typing import Dict
from typing import Optional

from .base import Base


class LocalRunner(Base):
    """Used to run commands on a local system."""

    def run(
        self,
        executor: str,
        command: str,
        timeout: int = 5,
        shell: bool = False,
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[str] = None,
    ) -> Dict[str, str]:
        """Runs the provided command string using the provided executor.

        There are several executors that can be used: sh, bash, powershell and cmd

        Args:
            executor (str): The executor to use when executing the provided command string.
            command (str): The command string to run.
            timeout (int, optional): Timeout when running a command. Defaults to 5.
            shell (bool, optional): Whether to spawn a new shell or not. Defaults to False.
            env (dict, optional): Environment to use including environmental variables.. Defaults to os.environ.
            cwd (str, optional): The current working directory. Defaults to None.

        Returns:
            Dict[str]: Returns a dictionary of results from running the provided command.
        """
        self.__logger.debug("Starting a subprocess on the local system.")
        process = subprocess.Popen(
            executor,
            shell=shell,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            cwd=cwd,
        )
        try:
            self.__logger.info(f"Running command now.")
            outs, errs = process.communicate(bytes(command, "utf-8") + b"\n", timeout=timeout)
            # Adding details to our object response object
            self.response.return_code = process.returncode
            self.response.output = outs
            self.response.errors = errs
            return self.print_process_output(command=command, return_code=process.returncode, output=outs, errors=errs)
        except subprocess.TimeoutExpired as e:
            if e.output:
                self.__logger.warning(e.output)
            if e.stdout:
                self.__logger.warning(e.stdout)
            if e.stderr:
                self.__logger.warning(e.stderr)
            self.__logger.warning("Command timed out!")

            process.kill()
            return {}
