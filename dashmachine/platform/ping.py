"""

##### ping
Check if a service is online.
```ini
[variable_name]
platform = 'ping'
resource = '192.168.1.1'
```
> **Returns:** a right-aligned colored bullet point on the app card.

| Variable        | Required | Description                                                     | Options           |
|-----------------|----------|-----------------------------------------------------------------|-------------------|
| [variable_name] | Yes      | Name for the data source.                                       | [variable_name]   |
| platform        | Yes      | Name of the platform.                                           | rest              |
| resource        | Yes      | Url of whatever you want to ping                                | url               |

> **Working example:**
>```config/data_sources.toml
>[ping_ds]
>platform = 'ping'
>resource = '192.168.1.1'
```


```
>Dashboard.toml
>[custom_card_name]
>title = 'ping test'
>data_sources = 'ping_ds'
>```


"""

import platform
import subprocess


class Platform:
    def __init__(self, options):
        # parse the user's options from the config entries
        for key, value in options.items():
            setattr(self, key, value)

    def process(self):
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", self.resource]
        up = subprocess.call(command) == 0

        if up is True:
            icon_class = "style='color:green'"
        else:
            icon_class = "style='color:red'"

        return f"<i class='material-icons right' {icon_class} >fiber_manual_record </i>"
