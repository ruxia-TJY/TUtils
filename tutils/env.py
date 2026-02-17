"""Constants for tutils app"""

class Env:
    """Environment variables for subprocesses."""
    OS_TYPE: str = ""       # System type, e.g., "Windows", "Linux", "Darwin"
    WORK_DIR: str = ""      # Current working directory

    def to_dict(self):
        return {k: str(v) for k, v in vars(self).items()}
env = Env()
