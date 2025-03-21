import os
from rich.console import Console

console = Console()

info = {
    'author':'ruxia-TJY',
    'email':'ruxia.tjy@qq.com',

    'helper': f'''\tremoveByExten path Extension1 Extension2 ...

    remove file by extension

 + path: the dir where the file is to be removed

 + Extension1: extension

 example:

 remove all txt and py files
 ```cmd
 python app.py -r removeByExten . txt py 
 ```
'''
}


rules = {
    "path": {
        'type':'str',
        'rules': 1,
        'value':None
    },
    "exten":{
        "type":"str",
        "rules":"*",
        "value":[]
    }
}

def main(cmd:dict):
    path = cmd['path']['value'][0]
    exten = []
    for i in cmd['exten']['value']:
        if not i.startswith('.'):
            exten.append(f'.{i}')
        else:
            exten.append(i)

    if not os.path.exists(path):
        raise Exception(f'File {path} does not exist')
    try:
        for fp, dn, fns in os.walk(path):
            for fn in fns:
                if os.path.splitext(os.path.join(fp, fn))[1] in exten:
                    os.remove(os.path.join(fp, fn))
                    Console().print(f'Remove {os.path.join(fp, fn)}',style='bold green')
        Console().print(f'All done!',style='bold green')
    except Exception as e:
        Console().print(f'Failed to remove {path}: {e}', style='bold red')