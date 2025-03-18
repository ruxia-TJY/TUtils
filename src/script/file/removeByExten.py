import os
from rich.console import Console

console = Console()

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