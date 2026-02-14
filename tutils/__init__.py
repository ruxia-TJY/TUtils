"""TUtils - A command-line tool."""
import platform
from .env import env
import pathlib
from . import const as C

# 在模块导入时自动初始化配置
from .config import init_config


# 初始化配置（使用默认位置 ~/.tutils/config.yaml）
_config_manager = init_config()

__version__ = C.version
__author__ = C.author
__email__ = C.email

__all__ = ["__version__", "__author__", "__email__", "init_config"]


env.OS_TYPE = platform.system()
env.WORK_DIR = pathlib.Path.cwd()