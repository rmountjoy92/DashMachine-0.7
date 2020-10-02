from dashmachine.dm.utils import html_from_markdown_file, html_from_template_file


class Content:
    def __init__(self, options, dashboard_card):
        """

        :param options: (dict) the key/value pairs from this section of the
        card's config toml
        :param dashboard_card: (Card Object) the parent card object.
        """
        self.markdown = None
        self.html = None

        # apply user config dict
        for key, value in options.get("content", {}).items():
            setattr(self, key, value)

        if not hasattr(self, "alignment"):
            self.alignment = "left"

        if self.markdown:
            try:
                self.markdown = html_from_markdown_file(file=self.markdown)
            except Exception as e:
                dashboard_card.dashboard.error = {
                    "error_title": f"DashMachine was unable to read {self.markdown}",
                    "error": f"Here's the error: {e}",
                }

        if self.html:
            try:
                self.html = html_from_template_file(
                    file=self.html, dashboard_card=dashboard_card
                )
            except Exception as e:
                dashboard_card.dashboard.error = {
                    "error_title": f"DashMachine was unable to read {self.html}",
                    "error": f"Here's the error: {e}",
                }
