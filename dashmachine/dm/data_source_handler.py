import os
import logging
import toml
from importlib import import_module, util as importlib_util
from dashmachine.paths import data_sources_toml, user_platform


class DataSourceHandler:
    """
    The DataSourceHandler class. This class is responsible for loading all of the
    configured data_sources in the data_source.toml file. A data_source is simply a
    configuration for how a Platform will run when it's called.

    This class is also responsible for calling Platforms, using the data_source config
    entries to do whatever it is the Platform is designed to do e.g. returning html for
    data_sources block on the Card.

    The FileWatcher for data_sources.toml runs DashMachine.build()

    """

    def __init__(self):
        self.toml_dict = None
        self.error = None
        self.data_sources = []
        self.load_data_sources()

    def load_data_sources(self):
        """
        Load all data_source configurations from data_sources.toml

        :return:
        """
        try:
            self.toml_dict = toml.load(data_sources_toml)
        except toml.TomlDecodeError as e:
            self.error = {
                "error_title": "DashMachine was unable to read your data_sources.toml file.",
                "error": f"Error from toml: {e}",
            }
            logging.error(self.error["error_title"], exc_info=True)
            return
        self.data_sources = [{key: value} for key, value in self.toml_dict.items()]
        logging.info("Data Sources loaded")

    def process_data_source(self, data_source_name):
        """
        Call the configured platform's process method using the configuration entry from
        data_sources.toml.

        When the platform is loaded for processing, it will first look in
        /config/platform, and if it's not there, it will use DM's included platforms
        from dashmachine/platform.

        :param data_source_name: (str) name of the data_source config entry
        from data_sources.toml

        :return return_value_from_platform: (Any) return value provided the platform
        being called. If there is an error in the process, it will return an error
        message as html.
        """
        error_msg = (
            f'<div style="background: red; color: white; '
            f'font-weight: bold; padding: 1rem; border-radius: 12px">'
        )
        try:
            ds_options = [
                option[data_source_name]
                for option in self.data_sources
                if option.get(data_source_name, None)
            ][0]
        except Exception as e:
            error = error_msg + (
                f"Issue matching data source on this card to a configured data source"
                f" in data_sources.toml! <br> Got this error: <br> {e}</div>"
            )
            return error

        return_val = self.execute_platform_method(
            ds_options["platform"], "process", ds_options
        )
        if isinstance(return_val, tuple):
            return error_msg + (
                f"{return_val[0]}"
                f" Check your data_sources.toml. <br> Got this error: "
                f"<br> {return_val[1]}</div>"
            )
        return return_val

    def on_dm_startup(self):
        for platform in os.listdir(user_platform):
            if platform not in ["__init__.py", "__pycache__"]:
                resp = self.execute_platform_method(
                    platform.replace(".py", ""),
                    "on_startup",
                    ignore_missing_methods=True,
                )
                if isinstance(resp, tuple):
                    logging.error(
                        f"{platform}'s startup method failed! "
                        f"Here's the error: {resp[0]} - {resp[1]}"
                    )

    @staticmethod
    def execute_platform_method(
        platform_name, method_name, ds_options={}, ignore_missing_methods=False
    ):
        # import the module
        try:
            spec = importlib_util.spec_from_file_location(
                f"{platform_name}",
                os.path.join(user_platform, f"{platform_name}.py"),
            )
            module = importlib_util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception:
            try:
                module = import_module(f"dashmachine.platform.{platform_name}")
            except Exception as e:
                error = (
                    "Issue importing the requested platform! Maybe it doesn't exist?",
                    e,
                )
                return error

        # initialize the platform's process method
        try:
            platform = module.Platform(ds_options)
        except Exception as e:
            error = (
                "Issue initializing the requested platform!",
                e,
            )
            return error

        # get the method
        try:
            method = getattr(platform, method_name)
        except Exception as e:
            if ignore_missing_methods:
                return None
            error = (
                f"Issue getting the platform's {method_name} method.",
                e,
            )
            return error

        # execute the method
        try:
            return_val = method()
        except Exception as e:
            error = (
                f"Issue getting the platform's {method_name} method.",
                e,
            )
            return error

        return return_val
