"""
    Script management module.

 script-example
  |- folder
  |- code-file
  |- index.yaml
"""

from pathlib import Path
from typing import List, Optional

from cryptography.utils import read_only_property
from rich import print as rprint

from .config import get_config
from .repository.repositoryindexfile import RepositoryIndexFile
from .repository.scriptindexfile import ScriptIndexFile
from .utils import indent_print,get_table

class ScriptManager:
    """Manage and execute scripts."""

    def __init__(self):
        """
        Initialize script manager.
        """

        config = get_config()
        self.repository:list = config.repository

    def _get_repo_script_list(self,repo:dict) -> List[str]:
        """

        :param repo:
        :return:
        """
        scriptlist:list = []
        if repo["type"]=="local":
            dirpath = repo["path"].parent
            for idx,script in enumerate(repo["scripts"]):
                script_path = dirpath / script / "index.yaml"
                if not script_path.exists():
                    continue
                script_model = ScriptIndexFile(script_path).get_instance()
                scriptlist.append(script_model.name)
        return scriptlist

    def list_scripts(self, repo_name:List|None = None,printit:bool = False) -> List[str]:
        '''
        Read list of scripts.
        :param repo_name: if None, return all scripts, else return which want
        :param printit: is print it in console
        :return: list of scripts
        '''
        scriptlist:list = []

        repositories = [{"path":(Path(i["path"]) / "index.yaml"),"type":i["type"] }for i in self.repository]
        repositories = [i for i in repositories if i["path"].exists()]

        repositories_model = [RepositoryIndexFile(Path(i["path"])).to_dict() for i in repositories]

        merged = [
            {**d1,**d2}
            for d1,d2 in zip(repositories_model,repositories)
        ]

        if repo_name is None:
            repo_name = [i["name"] for i in repositories_model]
        # filter which want repo
        repositories = [i for i in merged if i["name"] in repo_name]


        for repo in repositories:
            if printit:
                rprint(f'[bold]{repo["name"]}[/bold]\[{repo["quickly"]}]:')
            scripts = self._get_repo_script_list(repo)
            for script in scripts:
                indent_print(script)
        return scriptlist

    def list_repo(self,printit:bool = False) -> List[str]:
        '''
        Read list of repositories.

        :return: list of repositories
        '''
        repolist:list = []

        table = get_table()
        table.add_column("ID",justify="center",style="cyan",no_wrap=True)
        table.add_column("Name",justify="center")
        table.add_column("Quickly",justify="center",style="green")
        table.add_column("Path",justify="center")
        table.add_column("Type",justify="center")
        table.add_column("link",justify="center")
        table.add_column("Script Count",justify="center",style="green")

        for idx,repository in enumerate(self.repository):
            folder = Path(repository["path"])
            type = repository["type"]
            link = repository["link"] if type == "web" else ""

            repository_yaml_path = Path(folder) / "index.yaml"
            if repository_yaml_path.exists():
                repository_index = RepositoryIndexFile(repository_yaml_path).get_instance()
                scripts_count = len(repository_index.scripts)
                table.add_row(str(idx),
                              repository_index.name,
                              repository_index.quickly,
                              str(folder.resolve()),
                              type,
                              link,
                              str(scripts_count))
                repolist.append(f'{repository_index.name}\[{repository_index.quickly}] Path:{folder.home()} Type:{type} ')
        if printit:
            rprint(table)
        return repolist


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