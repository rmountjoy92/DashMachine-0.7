import os
from pathlib import Path


# root path of the application
def get_root_folder():
    curr_folder = os.path.dirname(__file__)
    rfolder = Path(curr_folder).parent
    return rfolder


def make_file(path):
    if not os.path.isfile(path):
        with open(path, "w") as new_file:
            new_file.write("")


def make_dir(path):
    if not os.path.isdir(path):
        os.mkdir(path)


root_folder = get_root_folder()

project_folder = os.path.join(root_folder, "dashmachine")

documentation_folder = os.path.join(root_folder, "documentation")

vs_folder = os.path.join(root_folder, "vscode_integration")

static_folder = os.path.join(project_folder, "static")

# set up the config directories
config_folder = os.path.join(root_folder, "config")
make_dir(config_folder)

dashboards_folder = os.path.join(config_folder, "dashboards")
make_dir(config_folder)

user_assets_folder = os.path.join(config_folder, "assets")
make_dir(user_assets_folder)

user_wallpapers_folder = os.path.join(user_assets_folder, "wallpapers")
make_dir(user_wallpapers_folder)

user_images_folder = os.path.join(user_assets_folder, "images")
make_dir(user_images_folder)

user_markdown_folder = os.path.join(user_assets_folder, "markdown")
make_dir(user_markdown_folder)

user_templates_folder = os.path.join(user_assets_folder, "templates")
make_dir(user_templates_folder)

user_css_folder = os.path.join(user_assets_folder, "css")
make_dir(user_css_folder)

user_js_folder = os.path.join(user_assets_folder, "js")
make_dir(user_js_folder)


# make the default files
main_dashboard = os.path.join(dashboards_folder, "main.toml")
make_file(main_dashboard)

access_toml = os.path.join(config_folder, "access.toml")
make_file(access_toml)

data_sources_toml = os.path.join(config_folder, "data_sources.toml")
make_file(data_sources_toml)

settings_toml = os.path.join(config_folder, "settings.toml")
make_file(settings_toml)

users_toml = os.path.join(config_folder, "users.toml")
make_file(users_toml)

shared_cards_toml = os.path.join(config_folder, "shared_cards.toml")
make_file(shared_cards_toml)

user_custom_css = os.path.join(user_css_folder, "global.css")
make_file(user_custom_css)

user_custom_js = os.path.join(user_js_folder, "global.js")
make_file(user_custom_js)
