"""Runs a command on a local system."""
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
import subprocess
from typing import Dict
from typing import Optional

from .base import Base
from .processor import Processor


class AWSRunner(Base):
    """Used to run commands on a Amazon Web Services system."""

    def _run(
        self,
        executor: str,
        command: str,
        timeout: int = 5,
        shell: bool = False,
        env: Optional[Dict[str, str]] = None,
        cwd: Optional[str] = None,
    ) -> Dict[str, str]:
        """Runs the provided command string using the provided executor.

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
            self.__logger.info("Running command now.")
            outs, errs = process.communicate(bytes(command, "utf-8") + b"\n", timeout=timeout)
            Processor(
                command=command, executor=executor, return_code=process.returncode, output=str(outs), errors=str(errs)
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
            return {}

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
        self.__logger.info("Checking for AWS CLI tools...")
        response = self._run(executor=executor, command="aws --version", timeout=timeout, shell=shell, env=env, cwd=cwd)
        if response and response.get("error"):
            self.__logger.warning(response.get("error"))
            return response
        self.__logger.info("AWS CLI tools found. Starting to run command...")
        return self._run(executor=executor, command=command, timeout=timeout, shell=shell, env=env, cwd=cwd)
