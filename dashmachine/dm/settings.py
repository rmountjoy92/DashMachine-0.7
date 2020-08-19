import toml
from dashmachine.paths import settings_toml


class Settings:
    def __init__(self):
        self.toml_path = settings_toml
        self.error = None
        try:
            self.toml_dict = toml.load(settings_toml)
        except Exception as e:
            self.error = (
                f"DashMachine was unable to read your settings.toml file. \n"
                f"Here is error: {e}"
            )
            return

        if self.toml_dict.get("Settings"):
            for k, v in self.toml_dict["Settings"].items():
                setattr(self, k, v)

        if not hasattr(self, "window"):
            self.window = {"title": "DashMachine"}
