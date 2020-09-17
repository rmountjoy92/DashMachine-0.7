from dashmachine.dm.utils import resolve_onpress_option


class Title:
    def __init__(self, options):
        # parse string shorthand
        if isinstance(options.get("title"), str):
            self.text = options["title"]
        else:
            # apply user config dict
            for key, value in options.get("title", {}).items():
                setattr(self, key, value)

        # set defaults
        if hasattr(self, "onpress"):
            self.onpress = resolve_onpress_option(self.onpress)
