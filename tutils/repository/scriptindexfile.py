"""Parse Script index file index.yaml"""
from pathlib import Path
import yaml
from .model import ScriptIndexFileModel

class ScriptIndexFile:
    """Parse Script index file index.yaml"""
    def __init__(self, file_path:Path = None):
        """
        Parse Script index file index.yaml
        :param file_path: Script index file path
        """
        self.file_path = file_path
        self.file:ScriptIndexFileModel = self._load_file()

    def _load_file(self) -> ScriptIndexFileModel:
        """Load Script index file model"""
        with open(self.file_path, "r",encoding='utf-8') as f:
            data = yaml.safe_load(f) or {}

        file = ScriptIndexFileModel(**data)
        return file

    def get_instance(self):
        """get ScriptIndexFileModel"""
        return self.file

    def __str__(self):
        return str(self.file)




