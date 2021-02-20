import pytest
from netcfgbu.config import load
from netcfgbu.plugins import Plugin, _registered_plugins, load_plugins


@pytest.fixture()
def pytest_load_plugins(request, monkeypatch, netcfgbu_envars):
    plugins_dir = f"{request.fspath.dirname}/files/plugins"
    monkeypatch.setenv("NETCFGBU_PLUGINSDIR", str(plugins_dir))
    app_cfg = load()

    load_plugins(app_cfg.defaults.plugins_dir)


def test_loading_plugins(pytest_load_plugins):
    assert issubclass(_registered_plugins["hooks"][0], Plugin)


def test_plugin_backup_success(pytest_load_plugins):
    rec = {"host": "switch1", "os_name": "junos"}
    res = True

    result = _registered_plugins["hooks"][0].backup_success(rec, res)

    assert result[0] == rec
    assert result[1] == res


def test_plugin_backup_failed(pytest_load_plugins):
    rec = {"host": "switch1", "os_name": "junos"}
    res = False

    result = _registered_plugins["hooks"][0].backup_failed(rec, res)

    assert result[0] == rec
    assert result[1] == res
