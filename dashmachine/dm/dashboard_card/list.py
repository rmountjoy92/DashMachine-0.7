from dashmachine.dm.utils import resolve_onpress_option, resolve_image_option


class List:
    def __init__(self, options):
        self.items = []
        # apply user config dict
        for key, value in options.get("list", {}).items():
            setattr(self, key, value)

        if not hasattr(self, "alignment"):
            self.alignment = "left"

        for item in self.items:
            if item.get("icon"):
                item["icon"] = resolve_image_option(item["icon"], default_height="24px")
            if item.get("onpress"):
                item["onpress"] = resolve_onpress_option(item["onpress"])
