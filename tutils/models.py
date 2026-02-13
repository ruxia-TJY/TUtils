"""Configuration data models using Pydantic."""

from typing import Any, Dict, Optional, List

from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    """Application configuration model."""

    # 应用配置
    app_name: str = Field(default="TUtils", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
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
            f"AppConfig(app_name={self.app_name}, debug={self.debug}, "
            f"log_level={self.log_level})"
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return self.dict()