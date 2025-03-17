import os
from rich.console import Console

console = Console()

args = {
    "path": {
        'type':'str',
        'rules': 2,
        'value':None
    },
    "hide":{
        "type":"bool",
        "rules":"?",
        "value":False
    }
}


def prints():
    for  arg in args:
        print(args[arg]['value'])

def main():
    path = args['path']['value']
    if not os.path.exists(path):
        raise Exception(f'File {path} does not exist')
    fileCount = 0
    dirCount = 0
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            dirCount += 1
            console.print(os.path.join(root, dir),style='bold yellow')

        for file in files:
            fileCount += 1
            console.print(os.path.join(root, file),style='#af00ff')

    console.rule()
    console.print(f'Files Count:{fileCount}',style='bold green')
    console.print(f'Dirs Count:{dirCount}',style='bold green')
    console.print(f'Total Files:{fileCount + dirCount}',style='bold green')