import os
import toml
import logging
from random import choice
from dashmachine.paths import settings_toml, user_wallpapers_folder


class Settings:
    def __init__(self, read_toml=True):
        """
        The Settings class. This is responsible for storing the data from your
        settings.toml file. It serves as a place to make app-wide changes in DashMachine
        The FileWatcher for settings.toml runs DashMachine.build()

        :param read_toml: (bool) Optionally skip the process in which the toml file
        is reloaded.

        """
        self.toml_path = settings_toml
        self.toml_dict = {}
        self.error = None

        self.window_title = "DashMachine"
        self.login_required = False
        self.public_command_bar_visible = True
        self.wallpaper = None
        self.theme = "light"
        self.editor_url = os.environ.get("EDITOR_URL", None)
        self.isotope_options = {}

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

            # isotope defaults for global scope
            if not self.isotope_options.get("itemSelector"):
                self.isotope_options["itemSelector"] = ".grid-item"
            if not self.isotope_options.get("layoutMode"):
                self.isotope_options["layoutMode"] = "packery"
                self.isotope_options["packery"] = "{gutter:10}"
            if not self.isotope_options.get("hiddenStyle"):
                self.isotope_options["hiddenStyle"] = "{opacity:0}"
            if not self.isotope_options.get("visibleStyle"):
                self.isotope_options["visibleStyle"] = "{opacity:1}"

            if self.wallpaper == "random":
                self.randomize_wallpaper()
            logging.info("Settings loaded")

    def randomize_wallpaper(self):
        wallpapers = os.listdir(user_wallpapers_folder)
        self.wallpaper = choice(wallpapers)
