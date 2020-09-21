class Description:
    def __init__(self, options):
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
