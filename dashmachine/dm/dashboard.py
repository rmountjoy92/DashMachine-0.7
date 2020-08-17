import toml
import os
from dashmachine.paths import dashboards_folder
from dashmachine.dm.data_source_handler import DataSourceHandler
from dashmachine.dm.dashboard_card import DashboardCard


class Dashboard:
    def __init__(self, file, dm):
        self.dm = dm
        self.settings = dm.settings
        self.toml_path = os.path.join(dashboards_folder, file)
        self.error = None
        self.toml_dict = None
        self.cards = None
        self.load_cards()
        self.data_source_handler = DataSourceHandler()

    def load_cards(self):
        try:
            self.toml_dict = toml.load(self.toml_path)
        except toml.TomlDecodeError as e:
            self.error = {
                "error_title": "DashMachine was unable to read your dashboard.toml file.",
                "error": f"Error from toml: {e}",
            }
            return
        self.cards = [
            DashboardCard(name=key, options=value, dashboard=self)
            for key, value in self.toml_dict.items()
        ]
