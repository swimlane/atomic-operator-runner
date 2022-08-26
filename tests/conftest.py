"""Configuration for the pytest test suite."""
import random

import pytest
from click.testing import CliRunner

from atomic_operator_runner import Runner


CONFIG = {
    "platform": random.choice(["macos", "linux", "windows"]),
    "hostname": "my-local-host",
    "username": "username",
    "password": "password",
    "verify_ssl": random.choice([True, False]),
    "ssh_key_path": "~/temp",
    "private_key_string": "private key",
    "ssh_port": random.randint(1, 30),
    "ssh_timeout": random.randint(1, 10),
}


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


@pytest.fixture
def main_runner_class() -> Runner:
    """Returns main Runner class."""
    return Runner


@pytest.fixture
def remote_configured_runner_class() -> Runner:
    """Returns a remote configured Runner class object."""
    return Runner(**CONFIG)
