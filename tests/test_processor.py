"""Tests Processor class methods."""
import random


SAMPLE_DATA = {
    "command": "echo 'Hello World!'",
    "executor": random.choice(["sh", "bash", "powershell", "cmd"]),
    "return_code": 1 or 2,
    "output": "Sample Output",
    "errors": "Sample Errors"
}

SAMPLE_BASE_RECORD = {
    "type": "informational",
    "message_data": "Some Message data",
    "source": "localhost",
    "pid": random.randint(250,1000),
    "native_thread_id": random.randint(250,1000),
    "managed_thread_id": random.randint(250,1000),
    "extra": {"key": "value"}
}

def test_processor(remote_configured_runner_class):
    from atomic_operator_runner.processor import Processor
    from atomic_operator_runner.models import RunnerResponse

    processor = Processor(**SAMPLE_DATA)
    assert processor.response
    assert processor.response.environment == None
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
    from atomic_operator_runner.processor import Processor
    from atomic_operator_runner.models import RunnerResponse

    processor = Processor(**SAMPLE_DATA)
    processor.response = RunnerResponse()

    processor._capture_base_records(data=SAMPLE_DATA["output"])
    assert processor.response.records and len(processor.response.records) == 1
    assert processor.response.records[0].message_data == SAMPLE_DATA["output"]

    processor.response = RunnerResponse()
    processor.response.records = []
    processor = Processor(**SAMPLE_DATA)
    processor._capture_base_records(data=SAMPLE_BASE_RECORD)
    for key,val in SAMPLE_BASE_RECORD.items():
        assert hasattr(processor.response.records[0], key)
