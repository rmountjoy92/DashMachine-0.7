from dashmachine.dm.utils import (
    resolve_image_option,
    resolve_onpress_option,
    html_from_markdown_file,
    html_from_template_file,
)


class DashboardCard:
    def __init__(self, name, options, dashboard):
        self.dashboard = dashboard
        self.name = name
        self.options = options
        self.tags = options.get("tags", [])
        self.onpress = resolve_onpress_option(options.get("onpress", {}))

        self.card = options.get("card", {})
        if not self.card.get("classes") and not self.card.get("css"):
            self.card["classes"] = "theme-surface-transparent"
        if self.card.get("full-width") is True:
            self.card["width"] = "calc(100vw - 2rem)"

        self.icon = Icon(options)
        self.title = Title(options)
        self.description = Description(options)
        self.data_sources = DataSources(options)
        self.list = List(options)
        self.actionbar = ActionBar(options)
        self.content = Content(options, self)


class Icon:
    def __init__(self, options):
        # parse string shorthand
        if isinstance(options.get("icon", None), str):
            self.image = resolve_image_option(options["icon"], default_height="64px")
        else:
            # apply user config dict
            for key, value in options.get("icon", {}).items():
                setattr(self, key, value)
            if hasattr(self, "image"):
                self.image = resolve_image_option(self.image, default_height="64px")
            if hasattr(self, "onpress"):
                self.onpress = resolve_onpress_option(self.onpress)


class Title:
    def __init__(self, options):
        # parse string shorthand
        if isinstance(options.get("title", None), str):
            self.text = options["title"]
        else:
            # apply user config dict
            for key, value in options.get("title", {}).items():
                setattr(self, key, value)

        # set defaults
        if not hasattr(self, "css") and not hasattr(self, "classes"):
            self.classes = "small-title"
        if hasattr(self, "onpress"):
            self.onpress = resolve_onpress_option(self.onpress)
        if not hasattr(self, "width"):
            self.width = "128px"


class Description:
    def __init__(self, options):
        # parse string shorthand
        if isinstance(options.get("description", None), str):
            self.text = options["description"]
        else:
            # apply user config dict
            for key, value in options.get("description", {}).items():
                setattr(self, key, value)

        # set defaults
        if not hasattr(self, "css") and not hasattr(self, "classes"):
            self.classes = "small-subtitle"
        if not hasattr(self, "width"):
            self.width = "128px"


class DataSources:
    def __init__(self, options):
        # apply user config dict
        for key, value in options.get("data_sources", {}).items():
            setattr(self, key, value)

        # set defaults
        if not hasattr(self, "collection"):
            self.collection = {"css": "width: 200px"}
        if not hasattr(self, "width"):
            self.width = "200px"


class List:
    def __init__(self, options):
        # apply user config dict
        for key, value in options.get("list", {}).items():
            setattr(self, key, value)


class ActionBar:
    def __init__(self, options):
        # apply user config dict
        for key, value in options.get("actionbar", {}).items():
            setattr(self, key, value)

        if hasattr(self, "actions"):
            for action in self.actions:
                action["icon"] = resolve_image_option(
                    action["icon"], default_height="24px"
                )
                if not action["icon"].get("classes", None):
                    action["icon"]["classes"] = "icon-btn"
                if action.get("onpress", None):
                    action["onpress"] = resolve_onpress_option(action["onpress"])


class Content:
    def __init__(self, options, dashboard_card):
        self.markdown = None
        self.html = None

        # apply user config dict
        for key, value in options.get("content", {}).items():
            setattr(self, key, value)

        if not hasattr(self, "alignment"):
            self.alignment = "left"

        if self.markdown:
            self.markdown = html_from_markdown_file(self.markdown)

        if self.html:
            self.html = html_from_template_file(
                name=self.html, dashboard_card=dashboard_card
            )
