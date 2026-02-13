"""TUtils - A command-line tool."""

# 在模块导入时自动初始化配置
from .config import init_config

__version__ = "0.1.0"
__author__ = "Jared3Dev"
__email__ = "ruxia.tjy@qq.com"

# 初始化配置（使用默认位置 ~/.tutils/config.yaml）
_config_manager = init_config()


__all__ = ["__version__", "__author__", "__email__", "init_config"]


