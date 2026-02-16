"""
    Script management module.

 script-example
  |- folder
  |- code-file
  |- index.yaml
"""

from pathlib import Path
from typing import List, Optional, Dict
from rich import print as rprint

from .config import get_config
from .repository.repositoryindexfile import RepositoryIndexFile
from .utils import indent_print,get_table
from .model import RepositoryModel,ScriptModel


class ScriptManager:
    """Manage and execute scripts."""

    def __init__(self):
        """
        Initialize script manager.
        """

        config = get_config()

        self.repository:list[RepositoryModel] = [RepositoryModel(i) for i in config.repository]

    def get_script_by_path(self,script_path:str) -> Optional[ScriptModel]:
        """
            get script by path, like repo_name.script_name
        :param script_path: script path, like repo_name.script_name
        :return: ScriptModel instance or None if not found
        """
        repo_name,script_name = script_path.split(".")
        repo = next((i for i in self.repository if i.name == repo_name),None)
        if not repo: return None
        scripts = repo.read_script_list()

        script = next((i for i in scripts if i.name == script_name),None)
        if not script: return None
        return script

    def list_scripts(self, repo_name:Optional[List] = None,printit:bool = False) -> List[str]:
        '''
          list of scripts.
        :param repo_name: if None, return all scripts, else return which want
        :param printit: print it in console if True
        :return: list of scripts
        '''
        scriptlist:list = []

        repositories = [i for i in self.repository if Path(i.index_file_path).exists()]

        if repo_name is None:
            repo_name = [i.name for i in repositories]

        # filter which want repo
        repositories = [i for i in repositories if i.name in repo_name]

        for repo in repositories:
            if printit: rprint(f'[bold]{repo.name}[/bold]:')
            scripts = repo.read_script_list()
            for script in scripts:
                if printit:indent_print(script.name)
                scriptlist.append(f'{repo.name}.{script.name}')
        return scriptlist

    def list_repo(self,printit:bool = False) -> List[RepositoryModel]:
        """
            list of repositories.
        :param printit: print it if True
        :return:
        """
        repolist:list = []

        table = get_table()
        table.add_column("ID",justify="center",style="cyan",no_wrap=True)
        table.add_column("Name",justify="center")
        table.add_column("Path",justify="center")
        table.add_column("Type",justify="center")
        table.add_column("link",justify="center")
        table.add_column("Script Count",justify="center",style="green")

        for idx,repository in enumerate(self.repository):
            scripts_count = len(repository.scripts)

            table.add_row(str(idx),
                          repository.name,
                          str(repository.path),
                          repository.type,
                          repository.link,
                          str(scripts_count))

            repolist.append(repository)
        if printit and len(repolist): rprint(table)

        return repolist

    def create_repo(self,repo:RepositoryIndexFile) -> bool:
        """Create a new repository."""

        path = Path(repo.file_path).parent

        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                rprint(f"Failed to create repository directory: {e}")
                return False

        repo.save_file()

        return True

#  全局脚本管理器实例
_script_manager: Optional[ScriptManager] = None


def get_script_manager() -> ScriptManager:
    """
    Get or create global script manager.

    Returns:
        ScriptManager instance
    """
    global _script_manager
    if _script_manager is None:
        _script_manager = ScriptManager()
    return _script_manager