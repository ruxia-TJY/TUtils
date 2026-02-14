"""repository and script model"""
from pydantic import BaseModel, Field
from typing import Any, Dict, List


class RepositoryIndexFileModel(BaseModel):
    """Repository index file yaml model."""
    name:str = Field(default="",description="Name of the index file")
    scripts:List[str] = Field(default_factory=list,description="Script files")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump()

class ScriptIndexFileModel(BaseModel):
    """Script index repository yaml model."""
    name: str = Field(default="",description="Name of the script")
    version: str = Field(default="0.0.1",description="Version of the script")
    description: str = Field(default="",description="Description of the script")
    author:str = Field(default="",description="Author of the script")
    email:str = Field(default="",description="Email of the script")
    run:str = Field(default="",description="EnterPoint of the script")
    src:List[str] = Field(default_factory=list,description="Source code of the script")
    license:str = Field(default="",description="License of the script")
    param:List[Dict[str, str]] = Field(default_factory=list,description="Parameters of the script")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.model_dump()
