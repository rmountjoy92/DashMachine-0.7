import toml
import logging
from dashmachine.paths import settings_toml


class Settings:
    def __init__(self, read_toml=True):
        self.toml_path = settings_toml
        self.toml_dict = {}
        self.error = None

        self.window = {"title": "DashMachine"}
        self.theme = {"brightness": "light", "primary": "orange", "accent": "lightBlue"}

        if read_toml:
            try:
                self.toml_dict = toml.load(settings_toml)
            except Exception as e:
                self.error = {
                    "error_title": "DashMachine was unable to read your settings.toml file. \n",
                    "error": f"Here is the error: {e}",
                }
                logging.error(self.error["error_title"], exc_info=True)
                return

            if self.toml_dict.get("Settings"):
                for k, v in self.toml_dict["Settings"].items():
                    setattr(self, k, v)
            logging.info("Settings loaded")
