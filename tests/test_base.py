"""Tests Base class methods."""

def test_get_local_system_platform(remote_configured_runner_class):
    assert remote_configured_runner_class.get_local_system_platform() == "macos"
