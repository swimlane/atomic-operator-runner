import os
import subprocess

from .base import Base


class LocalRunner(Base):

    def run(
        self, 
        executor: str, 
        command: str, 
        timeout: int = 5, 
        shell: bool = False, 
        env = os.environ, 
        cwd: str = None
    ):
        process = subprocess.Popen(
            executor=executor,
            shell=shell,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
            cwd=cwd,
        )
        try:
            outs, errs = process.communicate(
                bytes(command, "utf-8") + b"\n",
                timeout=timeout
            )
            return self.print_process_output(
                command=command,
                return_code=process.returncode,
                output=outs,
                errors=errs
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
