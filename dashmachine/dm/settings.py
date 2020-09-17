import os
import toml
import logging
from random import choice
from dashmachine.paths import settings_toml, user_wallpapers_folder


class Settings:
    def __init__(self, read_toml=True):
        self.toml_path = settings_toml
        self.toml_dict = {}
        self.error = None

        self.window_title = "DashMachine"
        self.login_required = False
        self.public_command_bar_visible = True
        self.wallpaper = None
        self.theme = "light"

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

            if self.wallpaper == "random":
                self.randomize_wallpaper()
            logging.info("Settings loaded")

    def randomize_wallpaper(self):
        wallpapers = os.listdir(user_wallpapers_folder)
        self.wallpaper = choice(wallpapers)
