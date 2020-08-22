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

        self.tags = self.options.get("tags", [])
        self.onpress = resolve_onpress_option(self.options.get("onpress", {}))

        self.card = self.options.get("card", {})
        if not self.card.get("classes") and not self.card.get("css"):
            self.card["classes"] = "theme-surface-transparent"
        if self.card.get("full-width") is True:
            self.card["width"] = "calc(100vw - 2rem)"

        self.icon = Icon(self.options)
        self.title = Title(self.options)
        self.description = Description(self.options)
        self.data_sources = DataSources(self.options)
        self.list = List(self.options)
        self.actionbar = ActionBar(self.options)
        self.content = Content(self.options, self)
