import os
import toml
import logging
from dashmachine.paths import config_folder


class ConfigModifier:
    def __init__(self):
        self.config_folder = config_folder
        self.error = None

    def modify_toml(self, commands):
        # parse user command string
        commands = commands.replace("'", '"')
        toml_file = commands[: commands.find(" ")]
        toml_file_end = len(toml_file) + 1
        table = commands[toml_file_end : commands.find(" ", toml_file_end)]
        if '"' in table:
            table = commands[
                toml_file_end : commands.find('"', commands.find('"') + 1) + 1
            ]
        table_name_end = toml_file_end + len(table) + 1
        table = table.replace('"', "")
        key = commands[table_name_end : commands.find(" ", table_name_end + 1)]
        key_end = table_name_end + len(key) + 1
        value = commands[key_end:]

        toml_file = os.path.join(self.config_folder, toml_file)
        try:
            toml_dict = toml.load(toml_file)
        except toml.TomlDecodeError as e:
            self.error = {
                "error_title": f"DashMachine was unable to read {toml_file}",
                "error": f"Error from toml: {e}",
            }
            logging.error(self.error["error_title"], exc_info=True)
            return

        try:
            toml_dict[table]
        except KeyError:
            self.error = {
                "error_title": f"Table: {table}, not found!",
                "error": f"That table doesn't exist in {toml_file}.",
            }
            logging.error(self.error["error_title"], exc_info=True)
            return

        if "." in key:
            toml_dict[table][key.split(".")[0]] = {}
            toml_dict[table][key.split(".")[0]][key.split(".")[1]] = value
        else:
            toml_dict[table][key] = value

        try:
            with open(toml_file, "w") as new_toml:
                toml.dump(toml_dict, new_toml)
        except Exception as e:
            self.error = {
                "error_title": f"Unable to set toml key: {key} in table: {table}",
                "error": f"Error from toml: {e}",
            }
            logging.error(self.error["error_title"], exc_info=True)
            return
