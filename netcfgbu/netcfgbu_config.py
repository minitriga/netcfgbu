from os.path import expandvars
from pathlib import Path
import toml

from .logger import setup_logging


def load(*, filepath=None, fileio=None):

    if filepath:
        app_cfg_file = Path(filepath)
        fileio = app_cfg_file.open()

    app_cfg = toml.load(fileio)

    app_defaults = app_cfg["defaults"]
    for var_name, var_value in app_defaults.items():
        app_defaults[var_name] = expandvars(var_value)

    credentials = app_cfg["credentials"]
    for cred in credentials:
        for var_name, var_value in cred.items():
            cred[var_name] = expandvars(var_value)

    configs_dir = Path(app_defaults["configs_dir"])
    if not configs_dir.is_dir():
        configs_dir.mkdir()

    setup_logging(app_cfg)

    return app_cfg
