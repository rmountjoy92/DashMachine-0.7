import logging
from threading import Thread
from watchgod import watch, Change


class FileWatcher:
    def __init__(self, path, change_function, event="modified"):
        self.path = path
        self.change_function = change_function
        self.event = event
        self.proc = None
        self.start()

    def watch_this(self):
        logging.info(f"Watching {self.path} for file {self.event}")
        for changes in watch(self.path):
            for change in changes:
                if (
                    (self.event == "all")
                    or (self.event == "modified" and change[0] == Change.modified)
                    or (self.event == "added" and change[0] == Change.added)
                ):
                    logging.info(f"Detected file {self.event} in {self.path}")
                    self.change_function()

    def start(self):
        self.proc = Thread(target=self.watch_this, daemon=True)
        self.proc.start()
