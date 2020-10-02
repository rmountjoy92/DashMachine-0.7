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

        try:
            spec = importlib_util.spec_from_file_location(
                f"{ds_options['platform']}",
                os.path.join(user_platform, f"{ds_options['platform']}.py"),
            )
            module = importlib_util.module_from_spec(spec)
            spec.loader.exec_module(module)
        except Exception:
            try:
                module = import_module(f"dashmachine.platform.{ds_options['platform']}")
            except Exception as e:
                error = error_msg + (
                    f"Issue importing the requested platform! Maybe it doesn't exist?"
                    f" Check your data_sources.toml. <br> Got this error: <br> {e}</div>"
                )
                return error

        try:
            platform = module.Platform(ds_options)
        except Exception as e:
            error = error_msg + (
                f"Issue initializing the requested platform!"
                f" Check your data_sources.toml. <br> Got this error: <br> {e}</div>"
            )
            return error

        try:
            html = platform.process()
        except Exception as e:
            error = error_msg + (
                f"The platform's process method failed! "
                f" Check your data_sources.toml. <br> Got this error: <br> {e}</div>"
            )
            return error

        return html
