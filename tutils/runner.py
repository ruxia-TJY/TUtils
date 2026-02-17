"""runner to run script with subprocess, stream output, support timeout, max_lines and passing env/args."""
from __future__ import annotations
import os
import sys
from .env import env
import subprocess
from typing import List, Dict, Optional
from rich import print as rprint

class ProcessRunner:
    """
    Helper to run a python script with subprocess, stream output,
    support timeout, max_lines and passing env/args.
    """
    def __init__(self, exe: Optional[str] = None):
        self.exe = exe or sys.executable

    def run_script(
        self,
        script_path: str,
        args: Optional[List[str]] = None,
        timeout: Optional[float] = None,
        max_lines: Optional[int] = None,
        debug:Optional[bool] = False,
    ) -> Dict:
        """
        Run script and stream output.

        Returns a dict with keys:
          exit_code, stdout_lines, stderr_lines, timed_out, killed_by_limit
        """
        args = args or []
        args = [i[1:] for i in args]

        cmd = [self.exe, script_path] + args
        if debug:
            rprint(cmd)
        proc_env = os.environ.copy()

        proc_env.update(env.to_dict())
        # Let subprocess inherit the terminal directly so rich/color output works natively
        proc = subprocess.Popen(
            cmd,
            cwd=env.WORK_DIR,
            env=proc_env,
        )

        timed_out = False
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                proc.terminate()
                try:
                    proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    proc.kill()
            except Exception:
                pass

        exit_code = proc.poll()

        return {
            "exit_code": exit_code,
            "stdout_lines": [],
            "stderr_lines": [],
            "timed_out": timed_out,
            "killed_by_limit": False,
        }