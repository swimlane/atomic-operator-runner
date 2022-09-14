"""Runs a command on a local system."""
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
import subprocess
from typing import Dict
from typing import Optional

from .base import Base
from .processor import Processor
from .utils.exceptions import IncorrectExecutorError
from .utils.exceptions import IncorrectPlatformError


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
    ) -> None:
        """Runs the provided command string using the provided executor.

        There are several executors that can be used: sh, bash, powershell and cmd

        Args:
            executor (str): The executor to use when executing the provided command string.
            command (str): The command string to run.
            timeout (int, optional): Timeout when running a command. Defaults to 5.
            shell (bool, optional): Whether to spawn a new shell or not. Defaults to False.
            env (dict, optional): Environment to use including environmental variables.. Defaults to os.environ.
            cwd (str, optional): The current working directory. Defaults to None.

        Raises:
            IncorrectExecutorError: Raises when an incorrect executor is provided
            IncorrectPlatformError: Raised when an incorrect platform is provided
        """
        if not self.COMMAND_MAP.get(executor):
            raise IncorrectExecutorError(provided_executor=executor)
        if not self.COMMAND_MAP.get(executor).get(Base.config.platform):
            raise IncorrectPlatformError(provided_platform=Base.config.platform)
        _executor = self.COMMAND_MAP[executor][Base.config.platform]
        self.__logger.debug("Starting a subprocess on the local system.")
        process = subprocess.Popen(
            _executor,
            shell=shell,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            cwd=cwd,
        )
        try:
            self.__logger.info("Running command now.")
            outs, errs = process.communicate(bytes(command, "utf-8") + b"\n", timeout=timeout)
            # Adding details to our object response object
            Processor(
                command=command, executor=_executor, return_code=process.returncode, output=str(outs), errors=str(errs)
            )
        except subprocess.TimeoutExpired as e:
            if e.output:
                self.__logger.warning(e.output)
            if e.stdout:
                self.__logger.warning(e.stdout)
            if e.stderr:
                self.__logger.warning(e.stderr)
            self.__logger.warning("Command timed out!")

            process.kill()
