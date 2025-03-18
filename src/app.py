import argparse
import os
import sys

import config
from tUtils import *
console = Console()

def parseArgs() -> TUtils:
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description="TUtils means T's Utils")
    parser.add_argument("--list",'-l', action="store_true",default=False,
                        help="The list of files to be processed")
    parser.add_argument('--run','-r',type=str,nargs='+',
                        help="run script")
    parser.add_argument('--code',type=str,nargs='+',
                        help="show script code")
    args = parser.parse_args()
    tUtils = TUtils(args)
    return tUtils

if __name__ == '__main__':
    config.ROOT_DIR = os.path.abspath(sys.argv[0])
    tUtils = parseArgs()
    utils.readDataList()
    tUtils.run()
