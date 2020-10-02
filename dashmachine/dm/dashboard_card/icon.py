from dashmachine.dm.utils import resolve_image_option, resolve_onpress_option


class Icon:
    def __init__(self, options):
        """
        This section contains an image at the top of the card.

        :param options: (dict) the key/value pairs from this section of the
        card's config toml
        """

        # parse string shorthand
        if isinstance(options.get("icon", None), str):
            self.image = resolve_image_option(options["icon"], default_height="64px")
        else:
            # apply user config dict
            for key, value in options.get("icon", {}).items():
                setattr(self, key, value)
            if not hasattr(self, "height"):
                self.height = "64px"
            if hasattr(self, "image"):
                self.image = resolve_image_option(
                    self.image, default_height=self.height
                )
            if hasattr(self, "onpress"):
                self.onpress = resolve_onpress_option(self.onpress)
