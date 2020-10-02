class DataSources:
    def __init__(self, options):
        """
        This section is an area below the list (if present) on the card for loading
        in information from data sources configured in your data-sources.toml file

        :param options: (dict) the key/value pairs from this section of the
        card's config toml
        """
        # apply user config dict
        for key, value in options.get("data_sources", {}).items():
            setattr(self, key, value)

        # set defaults
        if not hasattr(self, "width"):
            self.width = "100%"

        if not hasattr(self, "collection"):
            self.collection = {"css": f"width: {self.width};"}
