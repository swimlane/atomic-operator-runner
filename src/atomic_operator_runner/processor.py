"""Processes output and save response objects for an execution."""
import re
from datetime import datetime
from typing import Any
from typing import List
from typing import Union

from pypsrp.powershell import PSDataStreams

from .base import Base
from .models import BaseRecord


class Processor(Base):
    """Process the provided data and displays information as needed."""

    def __init__(self, command: str, executor: str, return_code: int, output: str, errors: Any) -> None:
        """Processes and displays output from a command execution.

        Args:
            command (str): The command ran during the execution.
            executor (str): The executor used.
            return_code (int): The return code (if available).
            output (str): The output string.
            errors (Any): Errors that may have occurred. Can be a string or dict or PSDataStreams type.
        """
        self.response.command = command
        self.response.executor = executor
        self.response.end_timestamp = datetime.now()
        self.response.output = output
        self.response.return_code = return_code

        if isinstance(errors, bytes):
            errors = errors.decode("utf-8", "ignore")

        self._capture_base_records(data=errors)
        self._print()

    def _capture_base_records(self, data: Any) -> None:
        """Builds and captures a BaseRecord object and returns it.

        Args:
            data (Any): Data to build a BaseRecord from.
        """
        record: Union[BaseRecord, List[BaseRecord]]
        if isinstance(data, dict):
            try:
                record = BaseRecord(**data)
            except Exception as e:
                self.__logger.warning("Unable to save error data as BaseRecord object. Will manually create it.")
                record = BaseRecord()
                record.extra = data
                self.__logger.debug(e)
        elif isinstance(data, str) and data:
            record = BaseRecord()
            record.type = "error"
            record.message_data = data
        elif isinstance(data, PSDataStreams):
            record = self._handle_windows_streams(stream=data)

        if not isinstance(record, list):
            record = [record]
        if not self.response.records:
            self.response.records = record
        else:
            self.response.records.extend(record)

    def _parse_data_record(self, data: Any, record_type: str) -> BaseRecord:
        """Parses the InformationRecord data out of the response stream."""
        extra_dict = {}
        for i in dir(data):
            if not i.startswith("_"):
                extra_dict[i] = str(getattr(data, i))
        if hasattr(data, "message_data"):
            message = data.message_data
        else:
            message = data.message
        data_dict = {
            "type": record_type,
            "message-data": message,
            "source": data.source if hasattr(data, "source") else None,
            "time_generated": data.time_generated if hasattr(data, "time_generated") else None,
            "user": data.user if hasattr(data, "user") else None,
            "computer": data.computer if hasattr(data, "computer") else None,
            "pid": data.pid if hasattr(data, "pid") else None,
            "native_thread_id": data.native_thread_id if hasattr(data, "native_thread_id") else None,
            "managed_thread_id": data.managed_thread_id if hasattr(data, "managed_thread_id") else None,
            "extra": extra_dict,
        }
        return BaseRecord(**data_dict)

    def _handle_windows_streams(self, stream: PSDataStreams) -> List[BaseRecord]:
        """Handles processing of all types of message strings from windows systems."""
        return_list = []
        for item in ["error", "debug", "information", "verbose", "warning"]:
            if hasattr(stream, item) and getattr(stream, item):
                for i in getattr(stream, item):
                    if i and i is not None:
                        return_list.append(self._parse_data_record(i, item))
        return return_list

    def _clean_output(self, data: Union[str, bytes]) -> str:
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
        return str(return_data)

    def _print(self) -> None:
        """Displays and logs data regarding the results of the execution."""
        self.__logger.debug("Processing command output.")
        if self.response.output:
            self.__logger.info(f"\n\nOutput: {self._clean_output(self.response.output)}")
        elif self.response.records:
            self.__logger.warning(
                f"\n\nCommand: {self.response.command} returned exit code {self.response.return_code}"
            )
            for item in self.response.records:
                if item.extra and item.extra.get("exception"):
                    self.__logger.warning(f"\n{self._clean_output(item.extra['exception'])}")
                elif item.message_data:
                    self.__logger.warning(f"\n{self._clean_output(item.message_data)}")
                else:
                    self.__logger.warning(
                        "\nAn error occurred but we are unable to display it correctly. "
                        "Please see the full response output for more details."
                    )
        else:
            self.__logger.info("(No output found)")
