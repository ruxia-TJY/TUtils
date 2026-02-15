import os
import signal
import sys
from rich.console import Console
_stop = False

def _handle_term(signum, frame):
    global _stop
    _stop = True
    print(f"Received signal {signum}, will stop soon...", flush=True)

signal.signal(signal.SIGTERM, _handle_term)
signal.signal(signal.SIGINT, _handle_term)

def main():
    console = Console()
    path = "/home/jared/.tutils"
    if not os.path.exists(path):
        raise Exception(f'File {path} does not exist')

    fileCount = 0
    dirCount = 0

    if "show" in sys.argv:
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
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
