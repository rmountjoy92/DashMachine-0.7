import os
from markupsafe import Markup
from typing import TypeVar
from markdown2 import markdown
from flask import render_template_string
from dashmachine.paths import user_markdown_folder, user_templates_folder

STR_OR_DICT = TypeVar("String or Dict", str, dict)


def resolve_image_option(img_option: STR_OR_DICT, default_height: str) -> dict:
    if isinstance(img_option, str):
        opt_image = {
            "type": ("image" if "static/" in img_option else "material-icon"),
            "src": img_option,
            "height": default_height,
        }
    else:
        opt_image = img_option
    return opt_image


def resolve_onpress_option(onpress_option: STR_OR_DICT) -> dict:
    if isinstance(onpress_option, str):
        opt_onpress = {"href": onpress_option, "target": "new_tab"}
    else:
        opt_onpress = onpress_option
    return opt_onpress


def html_from_markdown_file(file):
    path = os.path.join(user_markdown_folder, file)
    with open(path, "r") as md_file:
        md = md_file.read()
    html = markdown(
        md,
        extras=[
            "tables",
            "fenced-code-blocks",
            "break-on-newline",
            "header-ids",
            "code-friendly",
        ],
    )
    return Markup(html)


def html_from_template_file(file, dashboard_card):
    path = os.path.join(user_templates_folder, file)
    with open(path, "r") as template_file:
        with dashboard_card.dashboard.dm.app.app_context():
            html = render_template_string(
                template_file.read(), dashboard_card=dashboard_card
            )
    return Markup(html)
