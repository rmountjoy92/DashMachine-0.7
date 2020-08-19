import toml
from importlib import import_module
from dashmachine.dm import FileWatcher
from dashmachine.paths import data_sources_toml


class DataSourceHandler:
    def __init__(self):
        self.toml_dict = None
        self.error = None
        self.data_sources = []
        self.load_data_sources()
        self.file_watcher = FileWatcher(data_sources_toml, self.load_data_sources)

    def load_data_sources(self):
        try:
            self.toml_dict = toml.load(data_sources_toml)
        except toml.TomlDecodeError as e:
            self.error = {
                "error_title": "DashMachine was unable to read your data_sources.toml file.",
                "error": f"Error from toml: {e}",
            }
            return
        self.data_sources = [{key: value} for key, value in self.toml_dict.items()]
        print(" * Data Sources loaded")

    def process_data_source(self, data_source_name):
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
