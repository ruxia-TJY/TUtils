"""Command-line interface using Typer."""
from pathlib import Path
from typing import Optional, Annotated, Literal

import typer
from rich import print as rprint

from tutils.config import get_config, get_config_manager
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
    try:
        if version_flag:
            version()
    except Exception as e:
        typer.echo(e)
        raise typer.Exit(code=-1)

@app.command()
def show_script() -> None:
    """
    Show scripts folder list.
    """
    try:
        scripts = get_script_manager()
        scripts.list_scripts(None,True)
    except Exception as e:
        typer.echo(e)
        raise typer.Exit(code=-1)

@app.command()
def version() -> None:
    """Show version information."""
    from . import __version__
    typer.echo(f"TUtils version {__version__}")


# ==================== repository Command ====================
@repository_app.command("list")
def list_repo() -> None:
    '''Show repository list.'''
    try:
        scripts = get_script_manager()
        repos = scripts.list_repo(True)
        if not len(repos):
            rprint("empty.")
            return None
    except Exception as e:
        typer.echo(e)
        raise typer.Exit(code=-1)
    else:
        rprint(f'Done!')


@repository_app.command()
def add(
        path:Annotated[
            Path,
            typer.Argument(
                ...,
                help="Path to repository.",
                file_okay=False,
                dir_okay=True,
                resolve_path=True,
            )
        ],
        source: Annotated[
            Literal["local","web"],
            typer.Option("--type","-t"),
        ] = "local",
        link: Annotated[
            str,
            typer.Argument(
                ...,
                help="Path to repository.",
            )
        ] = "",
) -> None:
    """Add new repository."""
    try:
        if source == "web" and not len(link):
            rprint("empty link.")
            return None
        config = get_config()
        cm = get_config_manager()
        if not path.exists():
            rprint(f"Path {path.absolute()} does not exist. dir will be created.")
            path.mkdir(parents=True)
        repo = {"path":str(path), "type":source,"link":link}
        config.repository.append(repo)
        cm.save_config(config)
    except Exception as e:
        typer.echo(e)
        raise typer.Exit(code=-1)

@repository_app.command()
def remove(path: str) -> None:
    """Remove repository."""
    pass


@repository_app.command()
def update() -> None:
    """Update web repository to local."""
    pass




if __name__ == "__main__":
    app()