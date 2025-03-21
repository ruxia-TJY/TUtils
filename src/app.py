'''
    TUtils

    ruxia-TJY<ruxia.tjy@qq.com>

    MIT License
'''
import os
import sys
import argparse

from tUtils import TUtils
import config
import utils

def parseArgs() -> TUtils:
    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description="TUtils means T's Utils")
    parser.add_argument("--list",'-l', action="store_true",default=False,
                        help="The list of files to be processed")
    parser.add_argument('--run','-r',type=str,nargs='+',
                        help="run script")
    parser.add_argument('--code',type=str,nargs='+',
                        help="show script code")
    parser.add_argument("--showhelp",type=str,nargs='+',
                        help="Show script help")
    parser.add_argument("--showinfo",type=str,nargs='+',
                        help="Show script info")
    args = parser.parse_args()
    tUtils = TUtils(args)
    return tUtils

if __name__ == '__main__':
    config.ROOT_DIR = os.path.abspath(sys.argv[0])
    tUtils = parseArgs()
    utils.readDataList()
    tUtils.run()
