"""Command-line interface using Typer."""

from typing import Optional, Annotated, Literal

import typer
from rich import print as rprint
from .scripts import get_script_manager

# 创建 Typer 应用
app = typer.Typer(
    name="TUtils",
    help="A powerful command-line tool.",
)

# 创建子命令组
repository_app = typer.Typer(help="Repository management commands.")
app.add_typer(repository_app,name="repository")

run_app = typer.Typer(help="Run Python scripts commands.")
app.add_typer(run_app,name="run")

# ==================== Main Command ====================

@app.callback(invoke_without_command=True)
def main(
        version_flag: Annotated[
            Optional[bool],
            typer.Option(
                "--version",
                "-v",
                help="Show version information.",
                is_eager=True,
            )
        ] = None,
) -> None:
    if version_flag:
        version()

@app.command()
def show_script() -> None:
    """
    Show scripts folder list.
    """
    scripts = get_script_manager()
    scripts.list_scripts(True)

@app.command()
def version() -> None:
    """Show version information."""
    from . import __version__
    typer.echo(f"TUtils version {__version__}")


# ==================== repository Command ====================
@repository_app.command("list")
def list_repo() -> None:
    '''Show repository list.'''
    scripts = get_script_manager()
    repos = scripts.list_repo()
    if not len(repos):
        rprint("empty:")
        return None

    for repo in repos:
        rprint(repo)

@repository_app.command()
def add(
        path:str = typer.Argument(
            ...,
            help="Path to the repository.",
        ),
        source: Annotated[
            Literal["local","web"],
            typer.Option("--type","-t"),
        ] = "local",
) -> None:
    """Add new repository."""
    scripts = get_script_manager()




if __name__ == "__main__":
    app()