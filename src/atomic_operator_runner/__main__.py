"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """atomic-operator-runner."""


if __name__ == "__main__":
    main(prog_name="atomic-operator-runner")  # pragma: no cover
