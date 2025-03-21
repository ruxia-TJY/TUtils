import argparse
import sys
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import Python3Lexer
import os
from rich.console import Console
from rich.markdown import Markdown
import importlib.util
from pathlib import Path
import config
import utils

console = Console()


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

        if self.args.showhelp:
            self.showHelp(self.args.showhelp)
            return

        if self.args.showinfo:
            self.showInfo(self.args.showinfo)
            return

        if self.args.code:
            self.showCode(self.args.code)

        if self.args.run:
            self.runScript(self.args.run)
            return

    def showInfo(self,args):
        args = args[0]

        path = self.getPath(args)
        spec = importlib.util.spec_from_file_location(args, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[args] = module

        try:
            file_path = Path(path)
            file = file_path.name
            size = file_path.stat().st_size


            console.print(f'''[bold]File[/bold]: [green]{file}[/green]
Size: {size} Byte 
PATH: {file_path.as_uri()}''')


            for key,value in module.info.items():
                if key != "helper":
                    console.print(f'{key}: {value}')

            helper = Markdown(module.info["helper"])
            console.print('help:')
            console.print(helper)
        except AttributeError:
            pass
        except KeyError:
            pass
        except Exception as e:
            print(e)

    def getPath(self,name):
        path = None
        if '.' in name:
            ret = utils.checkInScriptDB(name)
            if ret is None:
                console.print(f"{name} not exist!", style="bold red")
                return None
            path = os.path.join(config.SCRIPT_DIR, ret.split('.')[0], '.'.join(ret.split('.')[1:]))
        else:
            ret = utils.find(name)
            if ret is None:
                console.print(f"{name} not exist!", style="bold red")
                return None
            path = os.path.join(config.SCRIPT_PATH, ret.split('.')[0], '.'.join(ret.split('.')[1:]))
        return path

    def showHelp(self,args):
        args = args[0]

        path = self.getPath(args)
        spec = importlib.util.spec_from_file_location(args, path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        sys.modules[args] = module

        try:
            markdown = Markdown(module.info["helper"])
            console.print(markdown)
        except KeyError:
            print("The script is no help")
        except Exception as e:
            print(e)


    def showCode(self,args):
        args = args[0]
        path = self.getPath(args)

        if path is not None:
            with open(path,'r',encoding='utf-8') as f:
                highlight_code = highlight(f.read(),Python3Lexer(),TerminalFormatter())
                print(highlight_code)

    def runScript(self,args):
        module_name = args[0]
        path = self.getPath(module_name)
        if path is None:
            return

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
        console.rule()
        for key in config.SCRIPTDB.keys():
            for file in config.SCRIPTDB[key]:
                if file.endswith(".py"):
                    print(f'{key}.{file}')
