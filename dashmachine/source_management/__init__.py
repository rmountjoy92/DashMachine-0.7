import os
from jsmin import jsmin
from markupsafe import Markup
from dashmachine.paths import static_folder
from dashmachine.source_management.cssmin import cssmin

"""This file establishes bundles of js and css sources, minifies them using jsmin and
a module named cssmin, adds script or style tag, uses a flask
context processor to make the process functions available to every jinja template.
Load orders in bundles are respected here"""

"""You can disable minification for debug purposes here (set to True) """
debug_js = False
debug_css = False


# these are all of the local js files that will be minified when served
js_local_bundle = [
    "vendors/popper.min.js",
    "vendors/bootstrap.min.js",
    "vendors/isotope.min.js",
    "vendors/isotope-packery.min.js",
]

# these are all of the local css files that will be minified when served
css_local_bundle = [
    "vendors/material-icons.css",
    "vendors/bootstrap.min.css",
    "global/utils.css",
]


def process_local_js_sources(process_bundle=None, src=None, global_bundle=False):
    if src:
        process_bundle = [src]

    elif global_bundle is True:
        process_bundle = js_local_bundle

    html = ""
    if debug_js is True:
        for source in process_bundle:
            html += f'<script src="static/js/{source}"></script>'
        return html
    for source in process_bundle:
        source_path = os.path.join(static_folder, "js", source)
        with open(source_path) as js_file:
            if ".min." not in source:
                minified = jsmin(js_file.read(), quote_chars="'\"`")
                html += f"<script>{minified}</script>"
            else:
                html += f"<script>{js_file.read()}</script>"

    return Markup(html)


def process_local_css_sources(process_bundle=None, src=None, global_bundle=False):
    if src:
        process_bundle = [src]

    elif global_bundle is True:
        process_bundle = css_local_bundle

    html = ""
    if debug_css is True:
        for source in process_bundle:
            html += (
                f'<link rel="stylesheet" type="text/css" '
                f'href="static/css/{source}">'
            )
        return html
    else:
        for source in process_bundle:
            source_path = os.path.join(static_folder, "css", source)
            if ".min." not in source:
                minified = cssmin(source_path)
                html += f"<style>{minified}</style>"
            else:
                with open(source_path, "r") as css_file:
                    html += f"<style>{css_file.read()}</style>"

    return Markup(html)
