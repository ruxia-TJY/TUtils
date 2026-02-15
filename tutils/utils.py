"""Utility functions for the package."""
from pathlib import Path
from rich.console import Console
from rich.padding import Padding
from . import const as C
from rich.table import Table
from rich import box
import shutil

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

def resolve_repo_path(p:Path) -> Path:
    """Resolve a path, expanding user and making it absolute."""
    if not p.parent or str(p.parent) == ".":
        p =  C.SCRIPTS_DIR / p.name
    return p.expanduser().resolve()

def remove_directory(path: Path):
    """Remove a directory and all its contents."""
    shutil.rmtree(path)