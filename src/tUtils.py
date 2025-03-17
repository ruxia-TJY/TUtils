import argparse
import ftplib
import numbers
import os
import config
from rich.console import Console
from utils import *

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

        if self.args.run:
            self.runScript(self.args.run)

    def runScript(self,args):
        # TODO check args exist
        if '.' in args[1]:
            print("has")
        else:
            try:
                module_name = args[1]
                target = f'import script.file.{args[1]} as f'
                exec(target,globals())
                args_len = len(args) - 2
                cur_index = 0
                # for i,arg in enumerate(f.args):
                for i in range(args_len):
                    if i < cur_index:
                        continue

                    if(f.args[args]['rules'] == '?'):
                        if i < args_len:
                            f.args[args]['value'] = args[i+2]
                            cur_index += 1
                    elif(isinstance(f.args[args]['rules'],numbers.Number)):
                        lst = []
                        for i in range(i,args[i+2] + f.args[arg]['rules']):
                            lst.append(args[i + 2])
                        cur_index += f.args[arg]['rules']

                        # f.args[arg]['value'] = [args[i+2]]

                        # f.args[arg]['value'] = args[i + 2]
                f.prints()
            except Exception as e:
                print(e)





    def showList(self):
        print("List:")
        Console().rule()
        subdirs = [d for d in os.listdir(config.script_dir) if os.path.isdir(os.path.join(config.script_dir,d))]
        for dir in subdirs:
            for file in os.listdir(os.path.join(config.script_dir,dir)):
                if file.endswith(".py"):
                    print(f'{dir}.{file}')