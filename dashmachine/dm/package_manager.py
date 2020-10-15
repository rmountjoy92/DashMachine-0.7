import os
import toml
import logging
import requests
from shutil import rmtree, copy2
from zipfile import ZipFile
from dashmachine.paths import (
    static_folder,
    config_folder,
    dashboards_folder,
    user_platform,
    data_sources_toml,
    custom_themes_folder,
    user_templates_folder,
    user_markdown_folder,
    user_custom_css,
    user_custom_js,
    user_images_folder,
    user_wallpapers_folder,
)


class PackageManager:
    def __init__(self):
        self.temp_folder = os.path.join(static_folder, "packages_temp")
        self.zip_file = os.path.join(self.temp_folder, "temp.zip")
        self.package_toml_file = os.path.join(self.temp_folder, "package.toml")
        self.package_toml = None
        self.error = None

    def reset_temp_folder(self):
        if os.path.isdir(self.temp_folder):
            rmtree(self.temp_folder)
        os.mkdir(self.temp_folder)

    def make_error(self, error_text):
        logging.error(f"INSTALLER ERROR: {error_text}")
        self.error = error_text
        self.package_toml = None
        self.reset_temp_folder()

    def read_package_file(self, file_name):
        try:
            with open(os.path.join(self.temp_folder, file_name), "r") as pkg_file:
                return pkg_file.read()
        except Exception:
            return None

    def validate_package(self):
        if not self.package_toml["package"].get("name"):
            self.make_error("Package has no name")
            return

        if not self.package_toml["package"].get("version"):
            self.make_error("Package has no version")
            return

        if not self.package_toml["package"].get("author"):
            self.make_error("Package has no author")
            return

        package_sections = [
            {"name": "provides_dashboards", "type": ".toml"},
            {"name": "provides_cards", "type": ".toml"},
            {"name": "provides_platforms", "type": ".py"},
            {"name": "provides_data_sources", "type": ".toml"},
            {"name": "provides_themes", "type": ".scss"},
            {"name": "provides_images", "type": "image"},
            {"name": "provides_wallpapers", "type": "image"},
            {"name": "provides_css", "type": ".css"},
            {"name": "provides_js", "type": ".js"},
            {"name": "provides_templates", "type": ".html"},
            {"name": "provides_markdown", "type": ".md"},
        ]
        for section in package_sections:
            if self.package_toml["package"].get(section["name"]):
                for file in self.package_toml["package"][section["name"]]:
                    ext = os.path.splitext(file)[1]
                    if os.path.isfile(os.path.join(self.temp_folder, file)):
                        if ext == section["type"] or section["type"] == "image":
                            continue
                        else:
                            self.make_error(
                                f"{file} needs to be of type {section['type']}"
                            )
                            return
                    else:
                        self.make_error(f"Could not find {file}")
                        return

    def handle_file_upload(self, request):
        self.reset_temp_folder()
        file = request.files.get("zip_file")
        if not file:
            self.make_error("No file provided")
            return

        if os.path.splitext(file.filename)[1] != ".zip":
            self.make_error("File is not of type .zip")
            return

        file.save(self.zip_file)
        self.load_package()

    def load_by_url(self, url):
        self.reset_temp_folder()
        downloaded_file = requests.get(url)
        with open(self.zip_file, "wb") as zip_file:
            zip_file.write(downloaded_file.content)

        self.load_package()

    def load_package(self):
        try:
            with ZipFile(self.zip_file, "r") as zf:
                zf.extractall(path=self.temp_folder)
        except Exception as e:
            self.make_error(f"Could not unzip your package. Error: {e}")
            return

        os.remove(self.zip_file)

        try:
            self.package_toml = toml.load(self.package_toml_file)
        except Exception as e:
            self.make_error(f"Could not load your package.toml. Error: {e}")
            return

        if not self.package_toml.get("package"):
            self.make_error("[packages] table not found in package.toml")
            return

        self.validate_package()

    def install_package(self, form):
        try:
            # install dashboards
            files = self.package_toml["package"].get("provides_dashboards", [])
            for file in files:
                temp_path = os.path.join(self.temp_folder, file)
                custom_name = form.get(f"dashboards-{file}-name")
                if custom_name:
                    file = custom_name
                copy2(temp_path, os.path.join(dashboards_folder, file))

            # install cards
            files = self.package_toml["package"].get("provides_cards", [])
            for file in files:
                dashboard_file = form.get(f"card-{file}-dashboard", "main") + ".toml"
                if dashboard_file == "shared_cards.toml":
                    dashboard_fp = os.path.join(config_folder, "shared_cards.toml")
                else:
                    dashboard_fp = os.path.join(dashboards_folder, dashboard_file)
                card_toml = (
                    f"\n# Installed by package: {self.package_toml['package']['name']}\n"
                    f"{form.get(f'card-{file}-toml')}"
                )
                with open(dashboard_fp, "a") as f:
                    f.write(card_toml)

            # install platforms
            files = self.package_toml["package"].get("provides_platforms", [])
            for file in files:
                temp_path = os.path.join(self.temp_folder, file)
                custom_name = form.get(f"platforms-{file}-name")
                if custom_name:
                    file = custom_name
                copy2(temp_path, os.path.join(user_platform, file))

            # install data sources
            files = self.package_toml["package"].get("provides_data_sources", [])
            for file in files:
                ds_toml = (
                    f"\n# Installed by package: {self.package_toml['package']['name']}\n"
                    f"{form.get(f'ds-{file}-toml')}"
                )
                with open(data_sources_toml, "a") as f:
                    f.write(ds_toml)

            # install themes
            files = self.package_toml["package"].get("provides_themes", [])
            for file in files:
                temp_path = os.path.join(self.temp_folder, file)
                custom_name = form.get(f"theme-{file}-name")
                if custom_name:
                    file = custom_name
                copy2(temp_path, os.path.join(custom_themes_folder, file))

            # install images
            files = self.package_toml["package"].get("provides_images", [])
            for file in files:
                temp_path = os.path.join(self.temp_folder, file)
                custom_name = form.get(f"image-{file}-name")
                if custom_name:
                    file = custom_name
                copy2(temp_path, os.path.join(user_images_folder, file))

            # install wallpapers
            files = self.package_toml["package"].get("provides_wallpapers", [])
            for file in files:
                temp_path = os.path.join(self.temp_folder, file)
                custom_name = form.get(f"wallpaper-{file}-name")
                if custom_name:
                    file = custom_name
                copy2(temp_path, os.path.join(user_wallpapers_folder, file))

            # install css
            files = self.package_toml["package"].get("provides_css", [])
            for file in files:
                css = (
                    f"\n/* Installed by {self.package_toml['package']['name']} */\n"
                    f"{self.read_package_file(file)}"
                )
                with open(user_custom_css, "a") as f:
                    f.write(css)

            # install js
            files = self.package_toml["package"].get("provides_js", [])
            for file in files:
                css = (
                    f"\n// Installed by {self.package_toml['package']['name']} \n"
                    f"{self.read_package_file(file)}"
                )
                with open(user_custom_js, "a") as f:
                    f.write(css)

            # install templates
            files = self.package_toml["package"].get("provides_templates", [])
            for file in files:
                temp_path = os.path.join(self.temp_folder, file)
                custom_name = form.get(f"template-{file}-name")
                if custom_name:
                    file = custom_name
                copy2(temp_path, os.path.join(user_templates_folder, file))

            # install markdown
            files = self.package_toml["package"].get("provides_markdown", [])
            for file in files:
                temp_path = os.path.join(self.temp_folder, file)
                custom_name = form.get(f"markdown-{file}-name")
                if custom_name:
                    file = custom_name
                copy2(temp_path, os.path.join(user_markdown_folder, file))

        except Exception as e:
            self.make_error(f"Could not install package! I got this error: {e}")
            return

        self.cleanup_install()

    def cleanup_install(self):
        self.package_toml = None
        self.reset_temp_folder()
