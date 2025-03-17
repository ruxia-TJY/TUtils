import os
from rich.console import Console

def main(path:str,extension:str):
    if not os.path.exists(path):
        raise Exception(f'File {path} does not exist')
    try:
        for fp, dn, fns in os.walk(path):
            for fn in fns:
                if os.path.splitext(os.path.join(fp, fn))[1] in extension:
                    os.remove(os.path.join(fp, fn))
                    Console().print(f'Remove {os.path.join(fp, fn)}',style='bold green')
        Console().print(f'All done!',style='bold green')
    except Exception as e:
        Console().print(f'Failed to remove {path}: {e}', style='bold red')
        return False
    else:
        return True