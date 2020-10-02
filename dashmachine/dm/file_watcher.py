import logging
from threading import Thread
from watchgod import watch, Change


class FileWatcher:
    def __init__(self, path, change_function, event="modified"):
        """
        The FileWatcher. Every file in the config folder must be watched for changes
        to enable a 'hot-reload' style approach to applying user's changes in the
        config directory.

        When a FileWatcher is initialized, it spawns a new thread running the
        watch_this function.

        :param path: (Path) the path location for what to watch
        :param change_function: (function) a function to run if a change is detected
        :param event: (str) Which type of event to trigger the watcher, options are
        'all', 'modified', 'added'

        """
        self.path = path
        self.change_function = change_function
        self.event = event
        self.proc = None
        self.start()

    def watch_this(self):
        """
        Watches for changes. Runs self.change_function when a change is detected.

        :return None:
        """
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
        """
        Spawns a new thread, using self.watch_this as it's function.

        :return:
        """
        self.proc = Thread(target=self.watch_this, daemon=True)
        self.proc.start()
