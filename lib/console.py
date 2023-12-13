from datetime import datetime
from typing import IO, Callable, Literal, Mapping, Optional, Union
from rich._log_render import FormatTimeCallable
from rich.console import Console as RichConsole, HighlighterType
from rich.emoji import EmojiVariant
from rich.highlighter import ReprHighlighter
from rich.style import StyleType
from rich.theme import Theme

class Console(RichConsole):
    def __init__(self):
        super().__init__()
        self.use_theme(theme=Theme({
            "repr.number": "bold green blink"
        }))
        
    def info(self, message):
        self.print(message, style="reset", markup=True)

    def warning(self, message):
        self.print(message, style="magenta", markup=True)

    def danger(self, message):
        self.print(message, style="bold red", markup=True)