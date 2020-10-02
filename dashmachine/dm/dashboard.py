import toml
import os
import logging
from dashmachine.paths import dashboards_folder
from dashmachine.dm.dashboard_card import DashboardCard


class Dashboard:
    def __init__(self, file, dm):
        """
        The Dashboard class. For each file in your config/dashboards DashMachine will
        create an instance of this class using the configuration options from the toml
        file. This class holds all of the card objects which are configured by the
        entries in the toml file this dashboard is using.

        Dashboards can define which users and roles can access this dashboard by a
        [DASHBOARD_OPTIONS] entry in the dashboard's toml file

        This is also where DashMachine will pass any errors from it's build
        process. If there are any errors passed to this object, when the dashboard
        is access from the interface, it will display the errors and not allow the
        user to see the requested Dashboard.

        The FileWatcher for this dashboard's toml file runs Dashboard.load_cards()

        :param file: (str) the toml file name, e.g. 'main.toml'
        :param dm: (DashMachine Object) the DashMachine parent class.
        """
        self.dm = dm
        self.file = file
        self.toml_path = os.path.join(dashboards_folder, file)
        self.error = None
        self.toml_dict = None
        self.cards = None
        self.tags = []
        self.users_can_access = ["all"]
        self.roles_can_access = ["all"]
        self.load_cards()

    def load_cards(self):
        """
        Reads the toml file for the Dashboard, loads all card entries in self.card
        as Card objects. Gets all possible tags on the Dashboard and stores them
        in self.tags

        This is the function that is called by the Dashboard's FileWatcher when a
        change is detected in the Dashboard's toml file.

        :return None:
        """
        self.error = None
        try:
            self.toml_dict = toml.load(self.toml_path)
        except toml.TomlDecodeError as e:
            self.error = {
                "error_title": f"DashMachine was unable to read {self.file}",
                "error": f"Error from toml: {e}",
            }
            logging.error(self.error["error_title"], exc_info=True)
            return

        if self.toml_dict.get("DASHBOARD_OPTIONS"):
            self.users_can_access = self.toml_dict["DASHBOARD_OPTIONS"].get(
                "users_can_access", ["all"]
            )
            self.roles_can_access = self.toml_dict["DASHBOARD_OPTIONS"].get(
                "roles_can_access", ["all"]
            )
            del self.toml_dict["DASHBOARD_OPTIONS"]

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
