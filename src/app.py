import argparse
import os
from fontTools.misc.cython import returns
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import Python3Lexer
from rich.console import Console

from tUtils import *

console = Console()

def parseArgs() -> TUtils:
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description="TUtils means T's Utils")
    parser.add_argument("--list",'-l', action="store_true", help="The list of files to be processed")
    parser.add_argument('run',type=str,nargs='+',help="run script")
    args = parser.parse_args()
    tUtils = TUtils(args)
    return tUtils

if __name__ == '__main__':
    tUtils = parseArgs()
    tUtils.run()