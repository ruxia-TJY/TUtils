"""Configuration management module with auto-initialization."""

import json
from pathlib import Path
from typing import Dict, Optional
import typer
import yaml

from .models import AppConfig


class ConfigManager:
    """Manage application configuration with auto-initialization."""

    # 默认配置目录位置
    DEFAULT_CONFIG_DIR = Path.home() / ".tutils"
    DEFAULT_CONFIG_NAME = "config.yaml"

    def __init__(self, config_path: Optional[Path] = None):
        """
        Initialize config manager.

        Args:
            config_path: Full path to config repository.
                        If None, uses ~/.tutils/config.yaml
        """
        if config_path is None:
            self.config_dir = self.DEFAULT_CONFIG_DIR
            self.config_path = self.config_dir / self.DEFAULT_CONFIG_NAME
        else:
            self.config_path = Path(config_path)
            self.config_dir = self.config_path.parent

        # 确保配置目录存在
        self.config_dir.mkdir(parents=True, exist_ok=True)

        # 加载或创建配置
        self.config: AppConfig = self._load_or_create_config()

    def _load_or_create_config(self) -> AppConfig:
        """
        Load configuration from repository, or create default if not exists.

        Returns:
            AppConfig object
        """
        if self.config_path.exists():
            return self._load_config()
        else:
            return self._create_default_config()

    def _load_config(self) -> AppConfig:
        """
        Load configuration from repository.

        Returns:
            AppConfig object
        """
        try:
            suffix = self.config_path.suffix.lower()

            if suffix in [".yaml", ".yml"]:
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
            elif suffix == ".json":
                with open(self.config_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                return AppConfig()

            config = AppConfig(**data)
            return config

        except Exception as e:
            return AppConfig()

    def _create_default_config(self) -> AppConfig:
        """
        Create and save default configuration.

        Returns:
            AppConfig object
        """
        config = AppConfig()
        defaultpath = Path.home() / ".tutils" / "Scripts"
        responsity = {
            "path":str(defaultpath),
            "type":"local",
            "link":"https://github.com/tutils/tutils/index.yaml",
        }

        config.repository.append(responsity)
        self.save_config(config)
        return config

    def save_config(self, config: Optional[AppConfig] = None) -> None:
        """
        Save configuration to repository.

        Args:
            config: AppConfig object to save. If None, uses self.config
        """
        if config is None:
            config = self.config

        try:
            suffix = self.config_path.suffix.lower()

            if suffix in [".yaml", ".yml"]:
                with open(self.config_path, "w", encoding="utf-8") as f:
                    yaml.dump(
                        config.dict(),
                        f,
                        default_flow_style=False,
                        allow_unicode=True,
                        sort_keys=False,
                    )
            elif suffix == ".json":
                with open(self.config_path, "w", encoding="utf-8") as f:
                    json.dump(config.dict(), f, indent=2, ensure_ascii=False)
            else:
                raise ValueError(f"Unsupported format: {suffix}")
        except Exception as e:
            raise typer.Exit(code=1)

    def load_from_file(self, filepath: Path) -> AppConfig:
        """
        Load configuration from a specific repository.

        Args:
            filepath: Path to configuration repository

        Returns:
            AppConfig object
        """
        if not filepath.exists():
            raise FileNotFoundError(f"Config repository not found: {filepath}")

        try:
            suffix = filepath.suffix.lower()

            if suffix in [".yaml", ".yml"]:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
            elif suffix == ".json":
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
            else:
                raise ValueError(f"Unsupported repository format: {suffix}")

            return AppConfig(**data)
        except Exception as e:
            typer.echo(f"✗ Error loading config from {filepath}: {e}", err=True, color=True)
            raise

    def save_to_file(self, filepath: Path, config: Optional[AppConfig] = None, format: str = "yaml") -> None:
        """
        Save configuration to a specific repository.

        Args:
            filepath: Path to save configuration
            config: AppConfig to save. If None, uses self.config
            format: File format (yaml, json, toml)
        """
        if config is None:
            config = self.config

        try:
            filepath.parent.mkdir(parents=True, exist_ok=True)

            if format.lower() in ["yaml", "yml"]:
                with open(filepath, "w", encoding="utf-8") as f:
                    yaml.dump(
                        config.dict(),
                        f,
                        default_flow_style=False,
                        allow_unicode=True,
                        sort_keys=False,
                    )
            elif format.lower() == "json":
                with open(filepath, "w", encoding="utf-8") as f:
                    json.dump(config.dict(), f, indent=2, ensure_ascii=False)
            else:
                raise ValueError(f"Unsupported format: {format}")

            typer.echo(f"✓ Config saved to: {filepath}", color=True)
        except Exception as e:
            typer.echo(f"✗ Error saving config: {e}", err=True, color=True)
            raise typer.Exit(code=1)

    def get(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """
        Get configuration value by key.

        Args:
            key: Configuration key (supports dot notation: app.debug)
            default: Default value if key not found

        Returns:
            Configuration value
        """
        keys = key.split(".")
        value: any = self.config.dict()

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value

    def set(self, key: str, value: any) -> None:
        """
        Set configuration value by key.

        Args:
            key: Configuration key (supports dot notation: app.debug)
            value: Value to set
        """
        keys = key.split(".")
        config_dict = self.config.dict()
        current = config_dict

        for k in keys[:-1]:
            if k not in current:
                current[k] = {}
            current = current[k]

        current[keys[-1]] = value
        self.config = AppConfig(**config_dict)

# 全局配置管理器实例
_config_manager: Optional[ConfigManager] = None


def init_config(config_path: Optional[Path] = None) -> ConfigManager:
    """
    Initialize global config manager.

    Args:
        config_path: Path to config repository

    Returns:
        ConfigManager instance
    """
    global _config_manager
    _config_manager = ConfigManager(config_path)
    return _config_manager


def get_config_manager() -> ConfigManager:
    """
    Get global config manager.

    Returns:
        ConfigManager instance

    Raises:
        RuntimeError: If config manager not initialized
    """
    global _config_manager
    if _config_manager is None:
        raise RuntimeError("Config manager not initialized. Call init_config() first.")
    return _config_manager


def get_config() -> AppConfig:
    """Get current configuration."""
    return get_config_manager().config