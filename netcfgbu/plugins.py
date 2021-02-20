from collections import defaultdict

_registered_plugins = defaultdict(dict)

_PLUGIN_NAME = "hooks"


def load_plugins(plugins_dir):
    if not plugins_dir.is_dir():
        return

    from importlib.machinery import FileFinder, SourceFileLoader

    finder = FileFinder(str(plugins_dir), (SourceFileLoader, [".py"]))  # noqa

    for py_file in plugins_dir.glob("*.py"):
        mod_name = py_file.stem
        finder.find_spec(mod_name).loader.load_module(mod_name)

    _registered_plugins[_PLUGIN_NAME] = []
    for subclass in Plugin.__subclasses__():
        _registered_plugins[_PLUGIN_NAME].append(subclass)


class Plugin(object):
    """base plugin class to use for subclassed plugins to enable custom methods to be run"""

    name = None

    def report(report):
        """returns a report specific plugin once the netcfgbu backup process has completed"""
        pass

    def backup_success(rec: dict, res: bool):
        """returns a backup success specific plugin once the netcfgbu backup process has completed"""
        pass

    def backup_failed(rec: dict, exc: str):
        """returns a backup failed specific plugin once the netcfgbu backup process has completed"""
        pass

    def git_report(success: bool, tag_name: str):
        """returns a git report specific plugin once the netcfgbu vcs save process has completed"""
        pass

    def run_backup_failed(rec: dict, exc: str):
        """execute plugins submodules for backup failed plugins"""

        tasks = _registered_plugins[_PLUGIN_NAME] or Plugin
        if isinstance(tasks, list):
            for task in tasks:
                task.backup_failed(rec, exc)
        else:
            tasks.backup_failed(rec, exc)

    def run_backup_success(rec: dict, res: str):
        """execute plugins submodules for backup success plugins"""

        tasks = _registered_plugins[_PLUGIN_NAME] or Plugin
        if isinstance(tasks, list):
            for task in tasks:
                task.backup_success(rec, res)
        else:
            tasks.backup_success(rec, res)

    def run_report(task_results):
        """execute plugins submodules for report plugins"""

        tasks = _registered_plugins[_PLUGIN_NAME] or Plugin
        if isinstance(tasks, list):
            for task in tasks:
                task.report(task_results)
        else:
            tasks.report(task_results)

    def run_git_report(success: bool, tag_name: str) -> None:
        """execute plugins submodules for vcs save plugins"""

        tasks = _registered_plugins[_PLUGIN_NAME] or Plugin
        if isinstance(tasks, list):
            for task in tasks:
                task.git_report(success, tag_name)
        else:
            tasks.git_report(success, tag_name)
