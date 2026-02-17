"""Utility functions for the package."""
from pathlib import Path
from urllib.parse import urlparse, urlunparse
import posixpath
import socket
import urllib.request
import urllib.error
from rich.console import Console
from rich.padding import Padding
from rich.progress import Progress, BarColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
from . import const as C
from rich.table import Table
from rich import box
import shutil

def indent_print(content: str):
    Console().print(Padding(content, (0, 0, 0, 4)))

def get_table(title:str=None) -> Table:
    if title is None:
        table = Table(
            show_header=True,
            header_style="bold magenta",
            box=box.ROUNDED,
            row_styles=["none", "dim"],
            expand=True
        )
    else:
        table = Table(
            title=title,
            show_header=True,
            header_style="bold magenta",
            box=box.ROUNDED,
            row_styles=["none", "dim"],
            expand=True
        )
    return table

def resolve_repo_path(p:Path) -> Path:
    """Resolve a path, expanding user and making it absolute."""
    if not p.parent or str(p.parent) == ".":
        p =  C.SCRIPTS_DIR / p.name
    return p.expanduser().resolve()

def remove_directory(path: Path):
    """Remove a directory and all its contents."""
    shutil.rmtree(path)


def is_url(string: str) -> bool:
    """Check if a string is a valid URL (http/https/ftp)."""
    try:
        result = urlparse(string.strip())
        return all([result.scheme in ("http", "https", "ftp"), result.netloc])
    except ValueError:
        return False


def url_dirname(url: str) -> str:
    """Return the directory part of a URL path, with trailing slash.

    Examples::

        url_dirname("https://example.com/foo/bar/file.txt")
        # "https://example.com/foo/bar/"

        url_dirname("https://example.com/foo/bar/")
        # "https://example.com/foo/bar/"

        url_dirname("https://example.com/file.txt")
        # "https://example.com/"
    """
    parsed = urlparse(url.strip())
    parent = parsed.path.rstrip("/").rsplit("/", 1)[0] + "/"
    return parsed._replace(path=parent, params="", query="", fragment="").geturl()


def url_join(base: str, *parts: str) -> str:
    """Join a base URL with one or more path segments.

    Unlike ``urljoin``, this always appends to the base path
    and ignores leading slashes in *parts*.

    Example::

        url_join("https://example.com/foo", "bar", "baz.txt")
        # "https://example.com/foo/bar/baz.txt"
    """
    parsed = urlparse(base)
    path = posixpath.join(parsed.path.rstrip("/"), *[p.lstrip("/") for p in parts])
    return urlunparse(parsed._replace(path=path))


_NO_CACHE_HEADERS = {
    "Cache-Control": "no-cache, no-store",
    "Pragma": "no-cache",
}


def download_file(url: str, dest: Path, chunk_size: int = 8192) -> Path:
    """Download a file from *url* to *dest* with a Rich progress bar.

    Sends no-cache headers to bypass CDN caching (e.g. GitHub raw content).

    :param url:        Remote file URL.
    :param dest:       Local destination path (file, not directory).
    :param chunk_size: Read chunk size in bytes.
    :returns:          Resolved path of the downloaded file.
    :raises OSError:            If the destination directory cannot be created or written to.
    :raises requests.HTTPError: If the server returns an error status.
    :raises ValueError:         If the server returns HTML instead of a file.
    """
    dest = dest.expanduser().resolve()
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers=_NO_CACHE_HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            content_type = response.headers.get("Content-Type", "")
            if "text/html" in content_type:
                raise ValueError(f"Unexpected HTML response from: {url}")
            total = int(response.headers.get("Content-Length", 0)) or None

            with Progress(
                "[progress.description]{task.description}",
                BarColumn(),
                DownloadColumn(),
                TransferSpeedColumn(),
                TimeRemainingColumn(),
            ) as progress:
                task = progress.add_task(f"[cyan]{dest.name}", total=total)

                with open(dest, "wb") as f:
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        progress.advance(task, len(chunk))

    except Exception:
        if dest.exists():
            dest.unlink()
        raise

    return dest


def is_url_status_ok(url: str) -> bool:
    """Check if a URL returns HTTP 200."""
    req = urllib.request.Request(url, headers=_NO_CACHE_HEADERS, method="HEAD")
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            return response.status == 200
    except urllib.error.URLError:
        return False

def is_reachable(url: str, timeout: int = 3) -> bool:
    """Check if a URL host is reachable via TCP connection."""
    parsed = urlparse(url.strip())
    host = parsed.hostname
    port = parsed.port or (443 if parsed.scheme == "https" else 80)
    if not host:
        return False
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, socket.error, OSError):
        return False