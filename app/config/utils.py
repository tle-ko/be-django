from typing import Any
from django.core.management.color import no_style
from django.utils.log import ServerFormatter


class ColorlessServerFormatter(ServerFormatter):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.style = no_style()
