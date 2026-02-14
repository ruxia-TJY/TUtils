"""Constants for tutils app"""

class Env:
    """Environment variables for subprocesses."""
    OS_TYPE: str = ""       # System type, e.g., "Windows", "Linux", "Darwin"
    WORK_DIR: str = ""      # Current working directory

    def to_dict(self):
        return vars(self)
env = Env()
