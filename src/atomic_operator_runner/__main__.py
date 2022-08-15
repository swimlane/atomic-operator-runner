"""Main command line entry point."""
# -*- coding: utf-8 -*-
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
import click


@click.command()
@click.version_option()
def main() -> None:
    """atomic-operator-runner."""


if __name__ == "__main__":
    main(prog_name="atomic-operator-runner")  # pragma: no cover
