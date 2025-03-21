import os
from rich.console import Console
console = Console()


info = {
    'author':'ruxia-TJY',
    'email':'ruxia.tjy@qq.com',

    'helper': f'''\tgetCount path [show_file]

    get file and dir count in path

 + path: the dir path you want to get file and dir count

 + show_file: default is False. to show file name

 example:

 to get current dir file count:
 ```cmd
 python app.py -r getCount . 
 ```
'''
}



rules = {
    "path": {
        'type':'str',
        'rules': 1,
        'value':None
    },
    "hide":{
        "type":"bool",
        "rules":"?",
        "value":False
    }
}


def main(cmd:dict):
    path = cmd['path']['value'][0]

    if not os.path.exists(path):
        raise Exception(f'File {path} does not exist')

    fileCount = 0
    dirCount = 0

    if cmd['hide']['value']:
        for root, dirs, files in os.walk(path):
            for dir in dirs:
                dirCount += 1
                console.print(os.path.join(root, dir),style='bold yellow')

            for file in files:
                fileCount += 1
                console.print(os.path.join(root, file),style='#af00ff')
    else:
        for root, dirs, files in os.walk(path):
            dirCount += len(dirs)
            fileCount += len(files)

    console.rule()
    console.print(f'Files Count:{fileCount}',style='bold green')
    console.print(f'Dirs Count:{dirCount}',style='bold green')
    console.print(f'Total Files:{fileCount + dirCount}',style='bold green')