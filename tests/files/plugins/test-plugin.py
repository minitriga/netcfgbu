from netcfgbu.plugins import Plugin


class TestPlugin(Plugin):
    def backup_success(rec: dict, res: bool):
        return (rec, res)

    def backup_failed(rec: dict, res: bool):
        return (rec, res)
