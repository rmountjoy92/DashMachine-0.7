import os
from shutil import copy2
from dashmachine.paths import vs_folder, config_folder


def install():
    vs_config_folder = os.path.join(vs_folder, "config")
    if not os.path.isdir(vs_config_folder):
        return "No vscode config folder volume provided"

    # link dm config to workspace
    os.symlink(
        config_folder,
        os.path.join(vs_config_folder, "workspace", "DashMachine"),
        target_is_directory=True,
    )

    # install DM extension
    copy2(
        os.path.join(vs_folder, "ext"),
        os.path.join(vs_config_folder, "extensions", "rmountjoy.dashmachine"),
    )
