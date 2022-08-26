"""Tests Processor class methods."""
import random


SAMPLE_DATA = {
    "command": "echo 'Hello World!'",
    "executor": random.choice(["sh", "bash", "powershell", "cmd"]),
    "return_code": 1 or 2,
    "output": "Sample Output",
    "errors": "Sample Errors",
}

SAMPLE_BASE_RECORD = {
    "type": "informational",
    "message_data": "Some Message data",
    "source": "localhost",
    "pid": random.randint(250, 1000),
    "native_thread_id": random.randint(250, 1000),
    "managed_thread_id": random.randint(250, 1000),
    "extra": {"key": "value"},
}


class SamplePSDataStreams:
    """Sample PSDataStreams class."""

    def __init__(self) -> None:
        """Example."""
        type_property = random.choice(["error", "debug", "information", "verbose", "warning"])

        setattr(self, type_property, [SampleErrorRecordMessage()])


class SampleErrorRecordMessage:
    """A sample ErrorRecordMessage class."""

    extra = {
        "MESSAGE_TYPE": "266245",
        "action": "None",
        "activity": "Invoke-Expression",
        "category": "17",
        "command_definition": "None",
        "command_name": "None",
        "command_type": "None",
        "command_visibility": "None",
        "details_message": "None",
        "exception": "System.Management.Automation.ParseException: At line:1 char:12\r\n+ Get-Service'\r\n+            ~\nThe string is missing the terminator: '.\r\n   at System.Management.Automation.ScriptBlock.Create(Parser parser, String fileName, String fileContents)\r\n   at System.Management.Automation.ScriptBlock.Create(ExecutionContext context, String script)\r\n   at Microsoft.PowerShell.Commands.InvokeExpressionCommand.ProcessRecord()\r\n   at System.Management.Automation.CommandProcessor.ProcessRecord()",
        "extended_info_present": "False",
        "fq_error": "TerminatorExpectedAtEndOfString,Microsoft.PowerShell.Commands.InvokeExpressionCommand",
        "invocation": "False",
        "invocation_bound_parameters": "None",
        "invocation_command_origin": "None",
        "invocation_expecting_input": "None",
        "invocation_history_id": "None",
        "invocation_info": "System.Management.Automation.InvocationInfo",
        "invocation_line": "None",
        "invocation_name": "None",
        "invocation_offset_in_line": "None",
        "invocation_pipeline_iteration_info": "None",
        "invocation_pipeline_length": "None",
        "invocation_pipeline_position": "None",
        "invocation_position_message": "None",
        "invocation_script_line_number": "None",
        "invocation_script_name": "None",
        "invocation_unbound_arguments": "None",
        "message": "ParserError: (:) [Invoke-Expression], ParseException",
        "pipeline_iteration_info": "None",
        "reason": "ParseException",
        "script_stacktrace": "None",
        "target_info": "None",
        "target_name": "",
        "target_object": "None",
        "target_type": "",
    }

    def __init__(self, type_property: str = "error") -> None:
        """Example."""
        self.type = type_property
        self.message_data = "ParserError: (:) [Invoke-Expression], ParseException"
        self.source = None
        self.time_generated = None
        self.user = None
        self.computer = None
        self.pid = None
        self.native_thread_id = None
        self.managed_thread_id = None

        for key, val in self.extra.items():
            setattr(self, key, val)


def test_processor():
    """Tests Processor class."""
    from atomic_operator_runner.models import RunnerResponse
    from atomic_operator_runner.processor import Processor

    processor = Processor(**SAMPLE_DATA)
    assert processor.response
    assert processor.response.environment is None
    assert processor.response.command == SAMPLE_DATA["command"]
    assert processor.response.executor == SAMPLE_DATA["executor"]
    assert processor.response.return_code == SAMPLE_DATA["return_code"]
    assert processor.response.output == SAMPLE_DATA["output"]
    assert processor.response.records
    assert len(processor.response.records) == 1
    assert processor.response.records[0].type == "error"
    assert processor.response.records[0].message_data == SAMPLE_DATA["errors"]
    processor.response = RunnerResponse()


def test_capture_base_records():
    """Tests cpature base records."""
    from atomic_operator_runner.models import RunnerResponse
    from atomic_operator_runner.processor import Processor

    processor = Processor(**SAMPLE_DATA)
    processor.response = RunnerResponse()

    processor._capture_base_records(data=SAMPLE_DATA["output"])
    assert processor.response.records and len(processor.response.records) == 1
    assert processor.response.records[0].message_data == SAMPLE_DATA["output"]

    processor.response = RunnerResponse()
    processor.response.records = []
    processor = Processor(**SAMPLE_DATA)
    processor._capture_base_records(data=SAMPLE_BASE_RECORD)
    for key, _val in SAMPLE_BASE_RECORD.items():
        assert hasattr(processor.response.records[0], key)


def test_parse_data_record():
    """Testing parse_data_record method."""
    from atomic_operator_runner.models import BaseRecord
    from atomic_operator_runner.processor import Processor

    processor = Processor(**SAMPLE_DATA)

    response = processor._parse_data_record(data=SampleErrorRecordMessage(), record_type="error")
    assert isinstance(response, BaseRecord)


def test_handle_windows_streams():
    """Testing handle_windows_streams method."""
    from atomic_operator_runner.processor import Processor

    processor = Processor(**SAMPLE_DATA)

    response = processor._handle_windows_streams(stream=SamplePSDataStreams())
    assert isinstance(response, list)
    assert len(response) == 1
