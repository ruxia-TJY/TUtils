"""some const values for tutils"""
from pathlib import Path
from importlib.metadata import version as _get_version

try:
    version = _get_version("TUtils-cli")
except Exception:
    version = "0.0.0"
author = "Jared3Dev"
email = "ruxia.tjy@qq.com"
license = 'MIT'
copy = f'Copyright (c) 2026 {author} <{email}>. All rights reserved.'
thanks = [

]

url = "https://github.com/ruxia-TJY/TUtils"
issue = 'https://github.com/ruxia-TJY/TUtils/issues'

last_update_time = "Feb. 18, 2026"


info = f"""TUtils - A powerful command-line tool.
    Ver {version} by {author} <{email}> {last_update_time}. {license}
    
    Most of my work involves using the command line, and sometimes it's simply faster than launching new software. I love Python because countless talented developers have created powerful packages that let me accomplish all sorts of tasks through it. I want to build a command-line tool that lets me achieve what I need without worrying about the underlying code. And I'm still developing it.    
    
    Report Bug or Feature: {issue} 
    if you like TUtils, please give it a star on GitHub: {url}
"""


CONFIG_DIR = Path.home() / ".tutils"
SCRIPTS_DIR = CONFIG_DIR / "Scripts"
# DEFAULT_REPO_DIR = SCRIPTS_DIR / "default"

DEFAULT_REPO_LIST = [
    {
        "path": str(SCRIPTS_DIR / "File"),
        "type": "remote",
        "link":"https://raw.githubusercontent.com/ruxia-TJY/tutils-repo/main/File/index.yaml"
    },
    {
        "path": str(SCRIPTS_DIR / "Image"),
        "type": "remote",
        "link":"https://raw.githubusercontent.com/ruxia-TJY/tutils-repo/main/Image/index.yaml"
    }

]