import argparse
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import Python3Lexer
import os

import config
from rich.console import Console
import utils

class TUtils:
    def __init__(self,args:argparse.Namespace):
        self.args = args

    def run(self):
        if not any(vars(self.args).values()):
            print('''TUtils means T's Utils'
build by ruxia-TJY<ruxia.tjy@qq.com>
use -h or --help for more information
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
        if '.' in args[0]:
            print("has")
        else:
            try:
                module_name = args[0]
                target = f'import script.file.{args[0]} as f'
                exec(target,globals())

                args = args[1:]
                try:
                    d = utils.parse(f.rules,args)
                    f.main(d)
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)

    def showList(self):
        print("List:")
        Console().rule()
        for key in config.SCRIPTDB.keys():
            for file in config.SCRIPTDB[key]:
                if file.endswith(".py"):
                    print(f'{key}.{file}')
