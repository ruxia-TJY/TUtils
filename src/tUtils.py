import argparse
import sys
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import Python3Lexer
import os
from rich.console import Console
import importlib.util

import config
import utils

class TUtils:
    '''

    '''
    def __init__(self,args:argparse.Namespace):
        self.args = args

    def run(self):
        if not any(vars(self.args).values()):
            print('''TUtils means T's Utils
use -h or --help for more information

Author ruxia-TJY<ruxia.tjy@qq.com>
open source https://github.com/ruxia-TJY/TUtils
License MIT

Thanks for use!
            ''')

        if self.args.list:
            self.showList()
            return

        if self.args.code:
            self.showCode(self.args.code)

        if self.args.run:
            self.runScript(self.args.run)
            return

    def showCode(self,args):
        args = args[0]
        if '.' in args:
            ret = utils.checkInScriptDB(args)
            if ret is None:
                Console().print(f"{args} not exist!",style="bold red")
                return None
            path = os.path.join(config.SCRIPT_DIR, ret.split('.')[0], '.'.join(ret.split('.')[1:]))

            with open(path, 'r', encoding='utf-8') as f:
                highlight_code = highlight(f.read(), Python3Lexer(), TerminalFormatter())
                print(highlight_code)
        else:
            ret = utils.find(args)
            if ret is None:
                Console().print(f"{args} not exist!",style="bold red")
                return None
            path = os.path.join(config.SCRIPT_DIR,ret.split('.')[0],'.'.join(ret.split('.')[1:]))

            with open(path,'r',encoding='utf-8') as f:
                highlight_code = highlight(f.read(),Python3Lexer(),TerminalFormatter())
                print(highlight_code)

    def runScript(self,args):
        module_name = args[0]

        if '.' in module_name:
            ret = utils.checkInScriptDB(module_name)
            if ret is None:
                Console().print(f"{module_name} not exist!", style="bold red")
                return None
            path = os.path.join(config.SCRIPT_DIR, ret.split('.')[0], '.'.join(ret.split('.')[1:]))
        else:
            ret = utils.find(module_name)
            if ret is None:
                Console().print(f"{module_name} not exist!", style="bold red")
                return None
            path = os.path.join(config.SCRIPT_PATH, ret.split('.')[0], '.'.join(ret.split('.')[1:]))

        try:
            spec = importlib.util.spec_from_file_location(module_name, path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            sys.modules[module_name] = module

            args = args[1:]

            parseCmd = utils.parse(module.rules,args)
            module.main(parseCmd)
        except Exception as e:
            print(e)

    def showList(self):
        print("List:")
        Console().rule()
        for key in config.SCRIPTDB.keys():
            for file in config.SCRIPTDB[key]:
                if file.endswith(".py"):
                    print(f'{key}.{file}')
