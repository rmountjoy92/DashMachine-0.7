import toml
import os
import logging
from dashmachine.paths import dashboards_folder
from dashmachine.dm.dashboard_card import DashboardCard


class Dashboard:
    def __init__(self, file, dm):
        self.dm = dm
        self.settings = dm.settings
        self.file = file
        self.toml_path = os.path.join(dashboards_folder, file)
        self.error = None
        self.toml_dict = None
        self.cards = None
        self.tags = []
        self.load_cards()

    def load_cards(self):
        try:
            self.toml_dict = toml.load(self.toml_path)
        except toml.TomlDecodeError as e:
            self.error = {
                "error_title": "DashMachine was unable to read your dashboard.toml file.",
                "error": f"Error from toml: {e}",
            }
            logging.error(self.error["error_title"], exc_info=True)
            return
        self.cards = [
            DashboardCard(name=key, options=value, dashboard=self)
            for key, value in self.toml_dict.items()
        ]
        for card in self.cards:
            if hasattr(card, "tags"):
                for tag in card.tags:
                    if tag not in self.tags:
                        self.tags.append(tag)
        logging.info(f"Cards for {self.file} were loaded")
