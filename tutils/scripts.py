"""Script management module."""

from pathlib import Path
from typing import List, Optional
from rich import print as rprint

from .config import get_config
from .repository.repositoryindexfile import RepositoryIndexFile
from .repository.scriptindexfile import ScriptIndexFile

'''
 scriptexample1
  |- code
  |- index.yaml  
'''


class ScriptManager:
    """Manage and execute scripts."""

    def __init__(self):
        """
        Initialize script manager.
        """

        config = get_config()
        self.repository:list = config.repository

    def list_scripts(self, printit:bool = False) -> List[str]:
        '''
        Read list of scripts.
        :param printit: is print it in console
        :return: list of scripts
        '''
        scriptlist:list = []
        for repository in self.repository:
            folder = Path(repository["path"])
            type = repository["type"]

            repository_yaml_path = Path(folder) / "index.yaml"
            if repository_yaml_path.exists():
                repository_index = RepositoryIndexFile(repository_yaml_path)
                if printit:
                    rprint(f'[bold]{repository_index.file.name}[/bold]:')

                # 使用 iterdir() 遍历第一层
                subdirs = [d for d in folder.iterdir() if d.is_dir()]
                for sd in subdirs:
                    script_index_path = Path(sd / "index.yaml")
                    if script_index_path.exists():
                        script_index = ScriptIndexFile(script_index_path)
                        if printit:
                            rprint(f'{script_index.file.name}')
                        scriptlist.append(f'{repository_index.file.name}.{script_index.file.name}')
        return scriptlist

    def list_repo(self,printit:bool = False) -> List[str]:
        '''
        Read list of repositories.
        :param printit: print it in console
        :return: list of repositories
        '''
        repolist:list = []
        for repository in self.repository:
            folder = Path(repository["path"])
            type = repository["type"]

            repository_yaml_path = Path(folder) / "index.yaml"
            if repository_yaml_path.exists():
                repository_index = RepositoryIndexFile(repository_yaml_path).get_instance()
                # if printit:
                    # rprint(f'[bold]{repository_index.file.name}[/bold]:')
                repolist.append(f'{repository_index.name}\[{repository_index.quickly}] Path:{folder.home()} Type:{type} ')
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