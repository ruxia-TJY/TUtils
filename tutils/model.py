"""Configuration data models using Pydantic."""
from functools import total_ordering
from pathlib import Path
from typing import Any, Dict, Optional, List
import time

from .repository.model import RepositoryIndexFileModel
from .repository.repositoryindexfile import RepositoryIndexFile
from .repository.scriptindexfile import ScriptIndexFile
from pydantic import BaseModel, Field
from . import utils
from . import exceptions
from rich.console import Console
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
import requests


class AppConfig(BaseModel):
    """Application configuration model."""

    # 应用配置
    debug: bool = Field(default=False, description="Enable debug mode")
    log_level: str = Field(default="INFO", description="Logging level")

    # 输出配置
    use_color: bool = Field(default=True, description="Use colored output")
    verbose: bool = Field(default=False, description="Verbose output")

    # 仓库配置
    repository:List[Dict[str,Any]] = Field(default_factory=list, description="Scripts Folder")
    # 自定义配置
    custom: Dict[str, Any] = Field(default_factory=dict, description="Custom configuration")

    class ConfigDict:
        """Pydantic config."""

        extra = "allow"  # 允许额外的字段
        case_sensitive = False  # 不区分大小写

    def __str__(self) -> str:
        """String representation."""
        return (
            f"AppConfig(debug={self.debug}, "
            f"log_level={self.log_level})"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump()



class ScriptModel(BaseModel):
    """Script model."""
    repository:str = Field(default="",description="Repository of the script")
    name:str = Field(default="",description="Name of the script")
    version:str = Field(default="",description="Version of the script")
    description:str = Field(default="",description="Description of the script")
    author:str = Field(default="",description="Author of the script")
    email:str = Field(default="",description="Email of the script")
    run:str = Field(default="",description="EnterPoint of the script")
    src:List[str] = Field(default_factory=list,description="Source code of the script")
    license:str = Field(default="",description="License of the script")
    folder_path:str = Field(default="",description="Path to the script")

    def read_by_index_file(self) -> None:
        """As Option, just try load if used"""
        pass

class RepositoryModel(BaseModel):
    """Repository model."""
    def __init__(self,config:Optional[dict] = None,**kwargs) -> None:
        super().__init__(**kwargs)
        if config is not None:
            self.set_by_config(config)
    name:str = Field(default="",description="Name of the repository")
    path:str = Field(default="",description="Path to the repository")
    type: str = Field(default="local",description="Type of the repository")
    link:str = Field(default="",description="Link to the repository")
    scripts:List[str] = Field(default_factory=list,description="Script files in the repository")
    index_file_path:str = Field(default="",description="Path to the index file")

    def set_by_index_file(self) -> None:
        if len(self.index_file_path):
            repository_index = RepositoryIndexFile(Path(self.index_file_path)).get_instance()
            self.name = repository_index.name
            self.scripts = repository_index.scripts

    def read_script_list(self) -> List[ScriptModel]:
        """As Option, just try load if used"""
        scriptlist:list[ScriptModel] = []
        dirpath = Path(self.path)
        for idx,script in enumerate(self.scripts):
            script_path = dirpath / script / "index.yaml"
            if not script_path.exists():
                continue
            script_model = ScriptIndexFile(script_path).get_instance()
            scriptlist.append(ScriptModel(
                repository=self.name,
                name=script_model.name,
                version=script_model.version,
                description=script_model.description,
                author=script_model.author,
                email=script_model.email,
                run=script_model.run,
                src=script_model.src,
                license=script_model.license,
                folder_path=str(dirpath / script)
            ))
        return scriptlist

    def set_by_config(self,config:dict):
        """set value by config dict, like {"path": "path/to/repo", "type": "local", "link": ""}"""
        self.path = config["path"]
        self.type = config["type"]
        self.link = config["link"]
        self.index_file_path = (str)(Path(self.path) / "index.yaml")
        self.set_by_index_file()

    def __str__(self) -> str:
        return f'name:{self.name} path:{self.path} type:{self.type} link:{self.link}'

    def to_config(self):
        return {
            "path": self.path,
            "type": self.type,
            "link": self.link
        }

    def update_to_local(self):

        console = Console()

        try:
            console.log(f'Update {self.name}')
            if self.type == "local":
                return
            if self.link is None:
                return

            path = Path(self.path)

            if not path.exists():
                raise exceptions.RepositoryLocalPathNotExistError(f"Path does not exist: {self.path}")

            if not utils.is_url(self.link):
                raise exceptions.RepositoryInvalidLinkError(f"Invalid url: {self.link}")

            if not utils.is_url_status_ok(self.link):
                raise exceptions.RepositoryConnnectFailedError(f"Connect Failed: {self.link}")

            # download repository index file
            repo_index_file_path = path / "index.yaml"
            utils.download_file(self.link, repo_index_file_path)
            self.set_by_index_file()

            repo_remote_dir_path = utils.url_dirname(self.link)

            # download script
            for idx,script in enumerate(self.scripts):
                script_local_dir_path = path / script
                script_local_index_file_path = script_local_dir_path / "index.yaml"
                script_remote_dir_path = utils.url_join(repo_remote_dir_path, script)
                script_remote_index_file_path = utils.url_join(script_remote_dir_path, "index.yaml")

                utils.download_file(script_remote_index_file_path, script_local_index_file_path)

                script_model = ScriptIndexFile(script_local_index_file_path).get_instance()
                files = script_model.src
                for file in files:
                    file_remote_path = utils.url_join(script_remote_dir_path, file)
                    file_local_path = script_local_dir_path / file

                    utils.download_file(file_remote_path, file_local_path)

            console.log(f"[green]Repository {self.name} is updated![/green]")
        except Exception as e:
            console.log(f'{e}')
            console.print('[red]Update Failed[/red]')