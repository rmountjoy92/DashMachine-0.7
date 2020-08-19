import os
from dashmachine.dm.file_watcher import FileWatcher
from dashmachine.paths import dashboards_folder
from dashmachine.dm.settings import Settings
from dashmachine.dm.dashboard import Dashboard
from dashmachine.dm.data_source_handler import DataSourceHandler

DEFAULT_QUERY_PROVIDERS = [
    {"name": "Google", "prefix": "g", "url": "https://www.google.com/search?q="},
    {"name": "Duckduckgo", "prefix": "d", "url": "https://duckduckgo.com/?q="},
    {"name": "Amazon", "prefix": "a", "url": "https://www.amazon.com/s?k="},
    {
        "name": "Wikipedia",
        "prefix": "w",
        "url": "https://en.wikipedia.org/wiki/Special:Search/",
    },
    {
        "name": "Arch Wiki",
        "prefix": "aw",
        "url": "https://wiki.archlinux.org/index.php?search=",
    },
]


class DashMachine:
    def __init__(self, app):
        print(" * DashMachine started")
        self.app = app

        self.settings = {}
        self.load_settings()

        self.dashboards = {}
        self.load_dashboards()

        self.main_dashboard = self.get_dashboard_by_name("main")

        self.data_source_handler = DataSourceHandler()

        if not hasattr(self, "query_providers"):
            self.query_providers = DEFAULT_QUERY_PROVIDERS

        self.settings_file_watcher = FileWatcher(
            self.settings.toml_path, self.load_settings
        )
        self.dashboards_folder_watcher = FileWatcher(
            dashboards_folder, self.load_dashboards, event="added"
        )

    def load_settings(self):
        print(" * Settings loaded")
        self.settings = Settings()
        if self.settings.error:
            for dboard_name, dboard in self.dashboards.items():
                dboard.error = self.settings.error

    def load_dashboards(self):
        print(" * Dashboards loaded")
        self.dashboards = {}
        for file in os.listdir(dashboards_folder):
            self.dashboards[file.replace(".toml", "")] = Dashboard(file=file, dm=self)

    def get_dashboard_by_name(self, name):
        return (
            self.dashboards[name] if self.dashboards.get(name) else self.main_dashboard
        )
