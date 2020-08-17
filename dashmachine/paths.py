import os
from pathlib import Path


# root path of the application
def get_root_folder():
    curr_folder = os.path.dirname(__file__)
    rfolder = Path(curr_folder).parent
    return rfolder


root_folder = get_root_folder()

project_folder = os.path.join(root_folder, "dashmachine")

documentation_folder = os.path.join(root_folder, "documentation")

vs_folder = os.path.join(root_folder, "vscode_integration")

static_folder = os.path.join(project_folder, "static")

# set up the config folder
config_folder = os.path.join(root_folder, "config")
if not os.path.isdir(config_folder):
    os.mkdir(config_folder)

dashboards_folder = os.path.join(config_folder, "dashboards")
if not os.path.isdir(dashboards_folder):
    os.mkdir(dashboards_folder)


def make_toml_file(path):
    if not os.path.isfile(path):
        with open(path, "w") as new_file:
            new_file.write("")


main_dashboard = os.path.join(dashboards_folder, "main.toml")
make_toml_file(main_dashboard)

access_toml = os.path.join(config_folder, "access.toml")
make_toml_file(access_toml)

data_sources_toml = os.path.join(config_folder, "data_sources.toml")
make_toml_file(data_sources_toml)

settings_toml = os.path.join(config_folder, "settings.toml")
make_toml_file(settings_toml)

users_toml = os.path.join(config_folder, "users.toml")
make_toml_file(users_toml)

user_assets_folder = os.path.join(config_folder, "assets")
if not os.path.isdir(user_assets_folder):
    os.mkdir(user_assets_folder)

user_markdown_folder = os.path.join(user_assets_folder, "markdown")
if not os.path.isdir(user_markdown_folder):
    os.mkdir(user_markdown_folder)


user_templates_folder = os.path.join(user_assets_folder, "templates")
if not os.path.isdir(user_templates_folder):
    os.mkdir(user_templates_folder)
