# NETCFGBU Plugins

This page shows how to hook into key `netcfgbu` lifecycle events to enable users to write arbitrary Python code to be executed when different `netcfgbu` commands are executed.

An example of this in use could be to notify a slack channel of the status of device backups. This could also be used to kick off an Ansible workflow to validate the backed up configurations using [Batfish](https://github.com/batfish/batfish).

## Lifecycle Hooks
The following table describes the possible lifecycle hooks:

| Name | Method | Description | Arguments |
| --- | --- | --- | --- |
| Backup Success | `backup_success` | `backup_success` is executed for every device that has successfully backed up. | `record`, `result` |
| Backup Failed | `backup_failed` | `backup_failed` is executed for every device that has failed to backup. | `record`, `result` |
| Report | `report` | `report` is executed at the end of `netcfgbu backup` command. | `report` |
| Git Report | `git_report` | `git_report` is executed at the end of `netcfgbu vcs save`. | `success`, `tag_name` |


## Implementing Plugins
Firstly to use `netcfgbu` a `plugins` directory needs to be identified within the `netcfgbu` configuration file or by using the environment variables. Please see [environment_variables](environment_variables.md) and [configuration-file](configuration-file.md) for the specifics.

Within the `plugins` directory Python files can be created which subclass the `netcfgbu` Plugin class like so...

```python
from netcfgbu import Plugin

class ScienceLogic(Plugin):
    name = "ScienceLogic"

    def backup_success(rec: dict, res: bool):
        print("Backup Successful")

    def backup_failed(rec: dict, exc: str):
        print("Backup Failed")

    def report(report):
        print("Backup Report")
```

Any number of Python files and classes can be created and they will all be executed within `netcfbu`. Please see the [table](#lifecycle-hooks) for the number of hooks that are available.

## Example Output
The following is an example of the above plugin in action.

```bash
(venv) $ netcfgbu backup -C netcfgbu.toml
Backup Successful
# ------------------------------------------------------------------------------
Summary: TOTAL=1, OK=1, FAIL=0
         START=2021-Feb-20 01:29:47 AM, STOP=2021-Feb-20 01:29:55 AM
         DURATION=7.829s
# ------------------------------------------------------------------------------
Backup Report
```

