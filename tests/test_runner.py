"""Runner class tests."""
import random


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


def test_setting_of_config(main_runner_class):
    """Tests setting of config."""
    runner = main_runner_class(platform="macos")
    assert runner.config.platform == "macos"


def test_setting_remote_config(main_runner_class):
    """Tests setting of remote config."""
    config = CONFIG
    runner = main_runner_class(**config)
    for key, val in config.items():
        assert getattr(runner.config, key) == val
    assert runner.config.run_type == "remote"


def test_response_is_runner_response(main_runner_class):
    """Tests Runner Response object."""
    from atomic_operator_runner.models import RunnerResponse

    runner = main_runner_class(**CONFIG)
    assert isinstance(runner.response, RunnerResponse)
