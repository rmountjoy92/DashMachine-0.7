import toml
from dashmachine.paths import settings_toml


class Settings:
    def __init__(self):
        self.error = None
        try:
            self.toml_dict = toml.load(settings_toml)
            for k, v in self.toml_dict["Settings"].items():
                setattr(self, k, v)

        except Exception as e:
            self.error = (
                f"DashMachine was unable to read your settings.toml file. \n"
                f"Here is error: {e}"
            )
            return

        if not hasattr(self, "window"):
            self.window = {"title": "DashMachine"}
