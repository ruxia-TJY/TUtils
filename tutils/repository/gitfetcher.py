"""Fetch specific paths from a remote git repository using sparse-checkout."""
from __future__ import annotations

import subprocess
import shutil
from pathlib import Path
from typing import List, Optional

from ..exceptions import (
    RepositoryInvalidLinkError,
    RepositoryConnnectFailedError,
)
from .. import utils


def _run(cmd: List[str], cwd: Optional[Path] = None) -> subprocess.CompletedProcess:
    return subprocess.run(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )


class GitFetcher:
    """
    Download specific paths from a remote git repository
    via sparse-checkout without fetching the entire repo.

    Usage::

        fetcher = GitFetcher("https://github.com/owner/repo.git")
        fetcher.fetch(["scripts/foo", "scripts/bar"], dest=Path("./local_repo"))
    """

    def __init__(self, url: str):
        if not utils.is_url(url):
            raise RepositoryInvalidLinkError(f"Invalid repository URL: {url}")
        self.url = url

    def fetch(
        self,
        paths: List[str],
        dest: Path,
        branch: str = "HEAD",
        clean: bool = False,
    ) -> Path:
        """
        Clone only the specified paths into *dest* using sparse-checkout.

        :param paths:   List of repository-relative paths to check out.
        :param dest:    Local directory to clone into.
        :param branch:  Branch/tag/commit to check out (default: HEAD).
        :param clean:   Remove and re-clone if *dest* already exists.
        :returns:       Resolved path to the cloned directory.
        :raises RepositoryConnnectFailedError: If git clone fails.
        """
        dest = dest.expanduser().resolve()

        if dest.exists():
            if clean:
                shutil.rmtree(dest)
            else:
                return dest

        # Step 1: shallow clone without checking out any files
        result = _run([
            "git", "clone",
            "--filter=blob:none",
            "--no-checkout",
            "--depth=1",
            self.url,
            str(dest),
        ])
        if result.returncode != 0:
            raise RepositoryConnnectFailedError(
                f"Failed to clone {self.url}:\n{result.stderr.strip()}"
            )

        # Step 2: enable cone sparse-checkout
        _run(["git", "sparse-checkout", "init", "--cone"], cwd=dest)

        # Step 3: set desired paths
        _run(["git", "sparse-checkout", "set"] + paths, cwd=dest)

        # Step 4: checkout
        result = _run(["git", "checkout", branch], cwd=dest)
        if result.returncode != 0:
            raise RepositoryConnnectFailedError(
                f"Failed to checkout {branch}:\n{result.stderr.strip()}"
            )

        return dest