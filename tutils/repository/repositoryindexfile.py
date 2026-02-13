"""Parse repository index file. index.yaml"""
from pathlib import Path
from typing import Dict

import yaml
from .model import RepositoryIndexFileModel

class RepositoryIndexFile:
    """Parse repository index file. index.yaml"""
    def __init__(self, file_path:Path = None):
        """
        Parse repository index file. index.yaml
        :param file_path: repository index file path
        """
        self.file_path = file_path
        self.file:RepositoryIndexFileModel = self._load_file()

    def _load_file(self) -> RepositoryIndexFileModel:
        """Load repository index file model"""
        if not self.file_path:
            return RepositoryIndexFileModel()
        with open(self.file_path, "r",encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}

        file = RepositoryIndexFileModel(**data)
        return file

    def to_dict(self) -> Dict[str, any]:
        """
        to dict
        :return:
        """
        return self.file.to_dict()

    def get_instance(self):
        """get repository index file model"""
        return self.file

    def __str__(self):
        return str(self.file)





