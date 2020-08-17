import os
from dashmachine.paths import dashboards_folder
from dashmachine.dm.settings import Settings
from dashmachine.dm.dashboard import Dashboard


class DashMachine:
    def __init__(self, app):
        self.app = app
        self.error = None

        self.settings = Settings()
        if self.settings.error:
            self.error = self.settings.error
            return

        self.dashboards = {}
        for file in os.listdir(dashboards_folder):
            self.dashboards[file.replace(".toml", "")] = Dashboard(file=file, dm=self)

        self.main_dashboard = self.get_dashboard_by_name("main")

    def get_dashboard_by_name(self, name):
        return (
            self.dashboards[name] if self.dashboards.get(name) else self.main_dashboard
        )
