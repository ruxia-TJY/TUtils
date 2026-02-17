"""runner to run script with subprocess, stream output, support timeout, max_lines and passing env/args."""
from __future__ import annotations
import os
import sys
from .env import env
import threading
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

    def _reader_thread(self, stream, collect: List[str], stream_name: str, print_prefix: str,
                       stop_event: threading.Event, line_limit: Optional[int], on_limit_hit):
        count = 0

        for raw in iter(stream.readline, b''):
            if stop_event.is_set():
                break

            if len(raw):
                collect.append(raw)
                print(f"{print_prefix}{raw}",end="")
            count += 1
            if line_limit is not None and count >= line_limit:
                on_limit_hit()
                break
        try:
            stream.close()
        except Exception:
            pass

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
        proc_env = {**proc_env,"FORCE_COLOR": "1"}  # ensure color output
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=env.WORK_DIR,
            env=proc_env,
            bufsize=1,
            text=True
        )

        stdout_lines: List[str] = []
        stderr_lines: List[str] = []
        stop_event = threading.Event()
        limit_hit = {"flag": False}

        def on_limit_hit():
            # called from reader thread when max_lines reached
            limit_hit["flag"] = True
            # try to terminate process gracefully
            try:
                proc.terminate()
            except Exception:
                pass

        threads = []
        if proc.stdout:
            t = threading.Thread(
                target=self._reader_thread,
                args=(proc.stdout, stdout_lines, "stdout", "", stop_event, max_lines, on_limit_hit),
                daemon=True,
            )
            threads.append(t)
            t.start()
        if proc.stderr:
            t2 = threading.Thread(
                target=self._reader_thread,
                args=(proc.stderr, stderr_lines, "stderr", "ERR: ", stop_event, max_lines, on_limit_hit),
                daemon=True,
            )
            threads.append(t2)
            t2.start()

        timed_out = False
        try:
            proc.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            timed_out = True
            try:
                proc.terminate()
                # 等待短时间再强杀
                try:
                    proc.wait(timeout=2)
                except subprocess.TimeoutExpired:
                    proc.kill()
            except Exception:
                pass
        finally:
            # ensure readers stop
            stop_event.set()
            # join threads
            for t in threads:
                t.join(timeout=1)



        exit_code = proc.poll()
        # if limit hit and process still alive, ensure killed
        killed_by_limit = limit_hit["flag"]
        if killed_by_limit and exit_code is None:
            try:
                proc.kill()
            except Exception:
                pass

        return {
            "exit_code": exit_code,
            "stdout_lines": stdout_lines,
            "stderr_lines": stderr_lines,
            "timed_out": timed_out,
            "killed_by_limit": killed_by_limit,
        }

