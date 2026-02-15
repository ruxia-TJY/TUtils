"""Command-line interface using Typer."""
from pathlib import Path
from typing import Optional, Annotated, Literal, List
import shlex
import typer
from rich.console import Console
from rich import print as rprint

from .repository.repositoryindexfile import RepositoryIndexFile
from . import const as C
from .model import ScriptModel,RepositoryModel
from .runner import ProcessRunner
from .config import get_config, get_config_manager
from .scripts import get_script_manager
from . import utils

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
            typer.Exit(0)

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
            List[str],
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
        typer.Option(...,"-d","--debug", help="Enable debug mode.")
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

        args_list = args if args else []

        res = runner.run_script(str(script),
                                args=args_list,
                                timeout=timeout,
                                max_lines=max_lines,
                                debug=debug)
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
                # resolve_path=True,
            )
        ],
        name:Annotated[
            str,
            typer.Argument(
                ...,
                help="Name of the repository.",
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

        path = utils.resolve_repo_path(path)

        # check path in config
        if cm.check_repo_exist(path):
            rprint("Repository already exists in config.")
            raise typer.Exit()
        sm = get_script_manager()
        repos = sm.list_repo()
        if any(i for i in repos if i.name == str(name)):
            rprint(f"Repository name {name} already exists in repositories.")

        repo = RepositoryIndexFile(
            file_path=path / "index.yaml"
        )

        repo.file.name = name

        if not sm.create_repo(repo):
            rprint("Failed to create repository.")
            raise typer.Exit()

        repo = {"path": str(path), "type": source, "link": link}
        config.repository.append(repo)
        cm.save_config(config)
        rprint("Repository added successfully!")

    except Exception as e:
        typer.echo(e)
        raise typer.Exit(code=-1)

@repository_app.command()
def remove(
        repo_name: Annotated[
            List[str],
            typer.Argument(
                ...,
                help="Path to repository to remove. Can be the path or the name of the repository.",
            ),
        ],
        remove_file: Annotated[
            bool,
            typer.Option(
            "-d", "--delete",
                help="Delete the repository files from disk.",
            ),
        ] = False,
) -> None:
    """Remove repository."""
    try:
        repos = get_script_manager().list_repo()
        exist_repo_list = [i for i in repos if i.name in repo_name]
        no_repo_list = [i for i in repo_name if i not in [j.name for j in exist_repo_list]]
        if len(no_repo_list):
            rprint("Repository not found: " + ", ".join(no_repo_list)) if len(no_repo_list) else None
            raise typer.Exit(code=-1)

        config = get_config()
        cm = get_config_manager()

        for repo in exist_repo_list:
            repo_config = {"path": repo.path, "type": repo.type, "link": repo.link}
            config.repository.remove(repo_config)

        cm.save_config(config)
        if remove_file:
            for repo in exist_repo_list:
                path = Path(repo.path)
                if path.exists() and path.is_dir():
                    utils.remove_directory(path)
        rprint("Repository removed successfully!")
        if not remove_file:
            rprint(
                "Note: Repository files are not deleted. Use --delete option to remove files from disk."
            )

    except Exception as e:
        typer.echo(e)
        raise typer.Exit(code=-1)



@repository_app.command()
def update() -> None:
    """Update web repository to local."""
    pass

# ==================== run Command ====================


if __name__ == "__main__":
    app()