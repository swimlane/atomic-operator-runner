# atomic-operator-runner

[![PyPI](https://img.shields.io/pypi/v/atomic-operator-runner.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/atomic-operator-runner.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/atomic-operator-runner)][pypi status]
[![License](https://img.shields.io/pypi/l/atomic-operator-runner)][license]

[![Tests](https://github.com/swimlane/atomic-operator-runner/workflows/Tests/badge.svg)][tests]
[![Codecov](https://codecov.io/gh/swimlane/atomic-operator-runner/branch/main/graph/badge.svg)][codecov]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]

[pypi status]: https://pypi.org/project/atomic-operator-runner/
[tests]: https://github.com/swimlane/atomic-operator-runner/actions?workflow=Tests
[codecov]: https://app.codecov.io/gh/swimlane/atomic-operator-runner
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black

## Features

- Execute a command string on a local, remote Windows, remote macOS and remote Linux systems
- Execute a command for PowerShell, command-line (cmd) and bash/sh on any of the above systems
- Can execute commands elevated on the supported systems
- Returns a standard response object, as well as displays a formatter version to the console via logging

### Response Object

Every execution of a command will return a standard object that includes details about the command execution. The full structure of this response is outlined below:

```json
{
    "environment": {
        "platform": "windows",
        "hostname": "10.x.x.x",
        "user": "user"
    },
    "command": "Get-Service\'",
    "executor": "powershell",
    "elevation_required": false,
    "start_timestamp": "2022-08-25T14:15:10.370468",
    "end_timestamp": "2022-08-25T14:15:12.165563",
    "return_code": 1,
    "output": "",
    "records": [
        {
            "type": null,
            "message_data": null,
            "source": null,
            "time_generated": null,
            "pid": null,
            "native_thread_id": null,
            "managed_thread_id": null,
            "extra": {
                "MESSAGE_TYPE": "266245",
                "action": "None",
                "activity": "Invoke-Expression",
                "category": "17",
                "command_definition": "None",
                "command_name": "None",
                "command_type": "None",
                "command_visibility": "None",
                "details_message": "None",
                "exception": "System.Management.Automation.ParseException: At line:1 char:12\\r\\n+ Get-Service\'\\r\\n+            ~\\nThe string is missing the terminator: \'.\\r\\n   at System.Management.Automation.ScriptBlock.Create(Parser parser, String fileName, String fileContents)\\r\\n   at System.Management.Automation.ScriptBlock.Create(ExecutionContext context, String script)\\r\\n   at Microsoft.PowerShell.Commands.InvokeExpressionCommand.ProcessRecord()\\r\\n   at System.Management.Automation.CommandProcessor.ProcessRecord()",
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
                "target_type": ""
            }
        }
    ]
}
```

## Installation

You can install _atomic-operator-runner_ via [pip] from [PyPI]:

```console
$ pip install atomic-operator-runner
```

## Usage

Please see the [Command-line Reference] for details.

```bash
Usage: atomic-operator-runner [OPTIONS] COMMAND EXECUTOR

  atomic-operator-runner executes powershell, cmd or bash/sh commands both
  locally or remotely using SSH or WinRM.

Options:
  --version                       Show the version and exit.
  --platform [windows|macos|linux]
                                  Platform to run commands on.  [required]
  --hostname TEXT                 Remote hostname to run commands on.
  --username TEXT                 Username to authenticate to remote host.
  --password TEXT                 Password to authenticate to remote host.
  --ssh_key_path PATH             Path to an SSH Key to authenticate to remote
                                  host.
  --private_key_string TEXT       Private SSH Key string used to authenticate
                                  to remote host.
  --verify_ssl BOOLEAN            Whether or not to verify SSL when
                                  authenticating.
  --ssh_port INTEGER              Port used for SSH connections.
  --ssh_timeout INTEGER           Timeout used for SSH connections.
  --elevated BOOLEAN              Whether or not to run the command elevated.
  --help                          Show this message and exit.
```

## Contributing

Contributions are very welcome.

To learn more, see the [Contributor Guide](CONTRIBUTING.md).

## License

Distributed under the terms of the [MIT license](LICENSE).

_atomic-operator-runner_ is free and open source software.

## Security

Security concerns are a top priority for us, please review our [Security Policy](SECURITY.md).

<!-- github-only -->

[license]: https://github.com/swimlane/atomic-operator-runner/blob/main/LICENSE
[contributor guide]: https://github.com/swimlane/atomic-operator-runner/blob/main/CONTRIBUTING.md
