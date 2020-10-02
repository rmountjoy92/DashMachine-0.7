class Description:
    def __init__(self, options):
        """
        This section contains gray text that is below the title
        (if present) on the card.

        :param options: (dict) the key/value pairs from this section of the
        card's config toml
        """

        # parse string shorthand
        if isinstance(options.get("description", None), str):
            self.text = options["description"]
        else:
            # apply user config dict
            for key, value in options.get("description", {}).items():
                setattr(self, key, value)

        # set defaults
        if not hasattr(self, "width"):
            self.width = "220px"
