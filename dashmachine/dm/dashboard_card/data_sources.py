class DataSources:
    def __init__(self, options):
        # apply user config dict
        for key, value in options.get("data_sources", {}).items():
            setattr(self, key, value)

        # set defaults
        if not hasattr(self, "width"):
            self.width = "100%"

        if not hasattr(self, "collection"):
            self.collection = {"css": f"width: {self.width};"}
