"""Utility functions for the package."""

from rich.console import Console
from rich.padding import Padding

from rich.table import Table
from rich import box

def indent_print(content: str):
    Console().print(Padding(content, (0, 0, 0, 4)))

def get_table(title:str=None) -> Table:
    if title is None:
        table = Table(
            show_header=True,
            header_style="bold magenta",
            box=box.ROUNDED,
            row_styles=["none", "dim"],
            expand=True
        )
    else:
        table = Table(
            title=title,
            show_header=True,
            header_style="bold magenta",
            box=box.ROUNDED,
            row_styles=["none", "dim"],
            expand=True
        )
    return table