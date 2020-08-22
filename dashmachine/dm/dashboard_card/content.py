from dashmachine.dm.utils import html_from_markdown_file, html_from_template_file


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
            self.markdown = html_from_markdown_file(file=self.markdown)

        if self.html:
            self.html = html_from_template_file(
                file=self.html, dashboard_card=dashboard_card
            )
