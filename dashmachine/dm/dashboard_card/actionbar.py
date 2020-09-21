from dashmachine.dm.utils import resolve_image_option, resolve_onpress_option


class ActionBar:
    def __init__(self, options):
        # apply user config dict
        for key, value in options.get("actionbar", {}).items():
            setattr(self, key, value)

        if hasattr(self, "actions"):
            for action in self.actions:
                action["icon"] = resolve_image_option(
                    action["icon"], default_height="24px"
                )
                if action.get("onpress", None):
                    action["onpress"] = resolve_onpress_option(action["onpress"])
