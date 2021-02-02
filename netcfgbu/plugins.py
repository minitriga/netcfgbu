from collections import defaultdict

from netcfgbu.cli.report import Report

_registered_plugins = defaultdict(dict)

_PLUGIN_NAME = "hooks"

def load_plugins(plugins_dir):
    # plugins_dir = config_dir.joinpath("plugins")
    if not plugins_dir.is_dir():
        return

    from importlib.machinery import FileFinder, SourceFileLoader

    finder = FileFinder(str(plugins_dir), (SourceFileLoader, [".py"]))  # noqa

    for py_file in plugins_dir.glob("*.py"):
        mod_name = py_file.stem
        finder.find_spec(mod_name).loader.load_module(mod_name)

class Plugin(object):
    name = None


    def report(report):
        pass


    def backup_success(rec: dict, res: bool):
        pass


    def backup_failed(rec: dict, exc: str):
        pass


    def git_report(success: bool, tag_name: str):
        pass

    def run_backup_failed(rec: dict, exc:str):
        tasks = _registered_plugins[_PLUGIN_NAME].get("backup") or Plugin
        if isinstance(tasks, list):
            for task in tasks:
                task.backup_failed(rec, exc)
        else:
            tasks.backup_failed(rec, exc)


    def run_backup_success(rec: dict, exc:str):
        tasks = _registered_plugins[_PLUGIN_NAME].get("backup") or Plugin
        if isinstance(tasks, list):
            for task in tasks:
                task.backup_success(rec, res)
        else:
            tasks.backup_success(rec, res)


    def run_report(task_results):
        tasks = _registered_plugins[_PLUGIN_NAME].get("backup") or Plugin
        if isinstance(tasks, list):
            for task in tasks:
                task.report(task_results)
        else:
            tasks.report(task_results)


    def run_git_report(success: bool, tag_name: str) -> None:
        tasks = _registered_plugins[_PLUGIN_NAME].get("git") or Plugin
        if isinstance(tasks, list):
            for task in tasks:
                task.git_report(success, tag_name)
        else:
            tasks.git_report(success, tag_name)


    @staticmethod
    def register(type="default", name=None):
        def decorator(cls: Plugin):
            if type in _registered_plugins[_PLUGIN_NAME]:
                _registered_plugins[_PLUGIN_NAME][type].append(cls)
            else:
                _registered_plugins[_PLUGIN_NAME][type] = []
                _registered_plugins[_PLUGIN_NAME][type].append(cls)
            return cls
        return decorator
