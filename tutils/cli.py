"""Command-line interface using Typer."""
from pathlib import Path
from typing import Optional, Annotated, Literal
import shlex
import typer
from rich.console import Console
from rich import print as rprint

from . import const as C
from .model import ScriptModel
from .runner import ProcessRunner
from .config import get_config, get_config_manager
from .scripts import get_script_manager

# 创建 Typer 应用
app = typer.Typer(
    name="TUtils",
    help=C.info,
)

# 创建子命令组
repository_app = typer.Typer(help="Repository management commands.")
app.add_typer(repository_app,name="repository")

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
            raise typer.Exit()

    except Exception as e:
        typer.echo(e)
        raise typer.Exit(code=-1)

@app.command()
def show_script() -> None:
    """
    Show scripts list.
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
    rprint(C.version)

@app.command("run")
def run_script(
    script: Annotated[
        Path,
        typer.Argument(
            ...,
            help="Path to python script to run.",
            file_okay=True,
            dir_okay=False,
            resolve_path=True)
    ],
        args: Annotated[
            Optional[str],
            typer.Argument(..., help="Arguments string passed to script (shell-like).")
        ] = None,
    timeout: Annotated[
        Optional[float],
        typer.Option("--timeout", help="Timeout seconds (float).")
    ] = None,
    max_lines: Annotated[
        Optional[int],
        typer.Option("--max-lines", help="Max output lines before stopping the process.")
    ] = None,
    debug: Annotated[
        Optional[bool],
        typer.Option("--debug", help="Enable debug mode.")
    ] = None,
):
    """
    Run a python script with streaming output and controls.
    """
    try:

        runner = ProcessRunner()
        script_model:ScriptModel

        # assume script is path
        if not script.exists():
            # if do not exist, try to find in repositories
            scripts = get_script_manager()
            script_list = scripts.list_scripts(printit=False)
            name = next((i for i in script_list if i.endswith(script.name)), None)
            if name is None:
                rprint(f"Script {script.name} not found.")
                raise typer.Exit(code=-1)
            script_model = scripts.get_script_by_path(name)
            script = Path(script_model.folder_path) / script_model.run

        args_list = shlex.split(args) if args else []

        res = runner.run_script(str(script), args=args_list, timeout=timeout, max_lines=max_lines)
        if debug:
            Console().rule()
            rprint("Debug:")
            rprint(res)
    except Exception as e:
        rprint(e)
        raise typer.Exit(code=-1)



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

# ==================== run Command ====================


if __name__ == "__main__":
    app()