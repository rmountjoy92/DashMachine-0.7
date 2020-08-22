from dashmachine.dm.utils import resolve_onpress_option


class Title:
    def __init__(self, options):
        # parse string shorthand
        if isinstance(options.get("title", None), str):
            self.text = options["title"]
        else:
            # apply user config dict
            for key, value in options.get("title", {}).items():
                setattr(self, key, value)

        # set defaults
        if not hasattr(self, "css") and not hasattr(self, "classes"):
            self.classes = "small-title"
        if hasattr(self, "onpress"):
            self.onpress = resolve_onpress_option(self.onpress)
        if not hasattr(self, "width"):
            self.width = "128px"
