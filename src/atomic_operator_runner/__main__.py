"""Main command line entry point."""
# Copyright: (c) 2022, Swimlane <info@swimlane.com>
# MIT License (see LICENSE or https://opensource.org/licenses/MIT)
import click

from atomic_operator_runner import Runner


@click.command()
@click.version_option()
@click.option(
    "--platform",
    required=True,
    type=click.Choice(["windows", "macos", "linux"], case_sensitive=False),
    help="Platform to run commands on.",
)
@click.option("--hostname", help="Remote hostname to run commands on.")
@click.option("--username", help="Username to authenticate to remote host.")
@click.option("--password", help="Password to authenticate to remote host.")
@click.option("--ssh_key_path", type=click.Path(exists=True), help="Path to an SSH Key to authenticate to remote host.")
@click.option("--private_key_string", help="Private SSH Key string used to authenticate to remote host.")
@click.option("--verify_ssl", default=False, help="Whether or not to verify SSL when authenticating.")
@click.option("--ssh_port", default=22, help="Port used for SSH connections.")
@click.option("--ssh_timeout", default=5, help="Timeout used for SSH connections.")
@click.argument("command")
@click.argument("executor")
@click.option("--elevated", default=False, help="Whether or not to run the command elevated.")
def main(
    platform,
    hostname,
    username,
    password,
    ssh_key_path,
    private_key_string,
    verify_ssl,
    ssh_port,
    ssh_timeout,
    command,
    executor,
    elevated,
) -> None:
    """atomic-operator-runner executes powershell, cmd or bash/sh commands both locally or remotely using SSH or WinRM."""
    return Runner(
        platform=platform,
        hostname=hostname,
        username=username,
        password=password,
        ssh_key_path=ssh_key_path,
        private_key_string=private_key_string,
        verify_ssl=verify_ssl,
        ssh_port=ssh_port,
        ssh_timeout=ssh_timeout,
    ).run(command=command, executor=executor, elevation_required=elevated)


if __name__ == "__main__":
    main(prog_name="atomic-operator-runner")  # pragma: no cover
