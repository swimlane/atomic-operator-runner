"""Tests Base class methods."""
import platform


def test_get_local_system_platform(remote_configured_runner_class):
    """Tests get local system platform."""
    assert (
        remote_configured_runner_class.get_local_system_platform() == "macos"
        if platform.node().lower() == "darwin"
        else platform.node().lower()
    )
