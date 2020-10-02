import logging
from dashmachine.dm.utils import resolve_onpress_option
from dashmachine.dm.dashboard_card.actionbar import ActionBar
from dashmachine.dm.dashboard_card.content import Content
from dashmachine.dm.dashboard_card.data_sources import DataSources
from dashmachine.dm.dashboard_card.description import Description
from dashmachine.dm.dashboard_card.icon import Icon
from dashmachine.dm.dashboard_card.list import List
from dashmachine.dm.dashboard_card.title import Title


class DashboardCard:
    def __init__(self, name, options, dashboard):
        """
        The Card class. This class is responsible for storing the data from the parent
        dashboard's toml file. These configurations are applied in the html template
        rendered when the parent dashboard is sent to the ui.

        The ways in which these configurations effect the card's appearance can be found
        in /dashmachine/templates/main/dashboard-card.html

        :param name: (str) the searchable (not displayed) name of the card
        :param options: (dict) the key/value pairs of the card's options from the toml
        :param dashboard: (Dashboard Object) the parent Dashboard object.
        """
        self.dashboard = dashboard
        self.name = name
        self.options = options

        if self.options.get("shared_card"):
            try:
                self.options = self.dashboard.dm.shared_cards[options["shared_card"]]
            except KeyError:
                logging.error(
                    f'Shared card {options["shared_card"]} not found, using defaults..'
                )

        # SET CARD DEFAULTS
        self.tags = self.options.get("tags", [])
        self.onpress = resolve_onpress_option(self.options.get("onpress", {}))

        self.card = self.options.get("card", {})
        if not self.card.get("width"):
            self.card["width"] = "auto"
        if not self.card.get("alignment"):
            self.card["alignment"] = "center"
        if self.card.get("full-width") is True:
            self.card["width"] = "calc(100vw - 2rem)"

        # INITIALIZE CHILD CLASSES (CARD BUILDING BLOCKS) USING CARD'S OPTIONS
        self.icon = Icon(self.options)
        self.title = Title(self.options)
        self.description = Description(self.options)
        self.data_sources = DataSources(self.options)
        self.list = List(self.options)
        self.actionbar = ActionBar(self.options)
        self.content = Content(self.options, self)
