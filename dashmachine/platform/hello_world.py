class Platform:
    def __init__(self, options):

        # parse the user's options from the config entries
        for key, value in options.items():
            setattr(self, key, value)

    def process(self):
        return (
            f"Stat: 500mb/s <br>"
            f"Stat: 500mb/s <br>"
            f"Stat: 500mb/s <br>"
            f"Stat: 500mb/s <br>"
        )
