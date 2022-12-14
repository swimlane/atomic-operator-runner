"""Test cases for the __main__ module."""
from __future__ import annotations

from typing import TYPE_CHECKING

from atomic_operator_runner import __main__


if TYPE_CHECKING:
    from click.testing import CliRunner


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    runner.invoke(__main__.main)
