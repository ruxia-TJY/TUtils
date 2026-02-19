"""Documentation server for TUtils - serves Markdown docs as HTML."""
import http.server
import socketserver
from pathlib import Path
from urllib.parse import urlparse, unquote

try:
    import markdown as _md

    def _render_markdown(text: str) -> str:
        return _md.markdown(text, extensions=["tables", "fenced_code", "toc"])
except ImportError:
    def _render_markdown(text: str) -> str:
        return f"<pre style='white-space:pre-wrap'>{text}</pre>"


_HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TUtils Docs{title_suffix}</title>
<style>
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;
  font-size:16px;line-height:1.6;color:#24292e;display:flex;min-height:100vh}}
nav{{width:240px;min-width:240px;background:#f6f8fa;border-right:1px solid #e1e4e8;
  padding:16px 0;position:sticky;top:0;height:100vh;overflow-y:auto}}
nav .logo{{font-size:15px;font-weight:700;padding:0 16px 14px;color:#24292e;
  border-bottom:1px solid #e1e4e8;margin-bottom:6px;display:block}}
nav .section{{padding:10px 16px 3px;font-size:11px;font-weight:600;color:#959da5;
  text-transform:uppercase;letter-spacing:.5px}}
nav a{{display:block;padding:4px 16px;color:#586069;text-decoration:none;font-size:13.5px}}
nav a:hover{{color:#0366d6;background:#e8f0fe}}
nav a.active{{color:#0366d6;font-weight:600;background:#e8f0fe}}
main{{flex:1;padding:36px 48px;max-width:860px}}
h1,h2,h3,h4{{margin-top:24px;margin-bottom:10px;font-weight:600;line-height:1.25}}
h1{{font-size:1.9em;padding-bottom:8px;border-bottom:1px solid #eaecef}}
h2{{font-size:1.45em;padding-bottom:6px;border-bottom:1px solid #eaecef}}
h3{{font-size:1.2em}}
p{{margin-bottom:14px}}
code{{background:#f6f8fa;border-radius:3px;padding:2px 5px;font-size:.87em;
  font-family:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace}}
pre{{background:#f6f8fa;border-radius:6px;padding:14px;overflow:auto;
  margin-bottom:14px;border:1px solid #e1e4e8}}
pre code{{background:none;padding:0;font-size:.87em}}
a{{color:#0366d6;text-decoration:none}}
a:hover{{text-decoration:underline}}
ul,ol{{padding-left:22px;margin-bottom:14px}}
li{{margin-bottom:3px}}
table{{border-collapse:collapse;width:100%;margin-bottom:14px}}
th,td{{border:1px solid #e1e4e8;padding:7px 12px;text-align:left}}
th{{background:#f6f8fa;font-weight:600}}
tr:nth-child(even){{background:#fafbfc}}
blockquote{{border-left:4px solid #dfe2e5;padding:0 14px;color:#6a737d;margin-bottom:14px}}
hr{{border:none;border-top:1px solid #e1e4e8;margin:20px 0}}
</style>
</head>
<body>
<nav>
  <span class="logo">TUtils Docs</span>
  {nav_html}
</nav>
<main>
{content_html}
</main>
</body>
</html>
"""

_NOT_FOUND = """\
<!DOCTYPE html><html><head><meta charset="UTF-8"><title>404</title></head>
<body style="font-family:sans-serif;padding:40px">
<h1>404 – Not Found</h1><p>The requested page was not found.</p>
<a href="/">← Back to Home</a></body></html>
"""


def _get_docs_dir() -> Path | None:
    """Find the docs directory (works in both dev and installed modes)."""
    # Dev mode: docs/ at project root (parent of tutils/)
    dev = Path(__file__).parent.parent / "docs"
    if dev.is_dir():
        return dev
    # Installed mode: docs/ bundled inside the package
    installed = Path(__file__).parent / "docs"
    if installed.is_dir():
        return installed
    return None


def _build_nav(docs_dir: Path, current_path: str) -> str:
    """Generate navigation HTML from the docs directory layout."""
    parts: list[str] = []

    def _label(stem: str) -> str:
        return stem.replace("-", " ").replace("_", " ").title()

    def _active(href: str) -> str:
        if current_path == href or current_path == href + "/" or current_path == href + ".md":
            return ' class="active"'
        return ""

    # Root-level .md files — index first, then alphabetical
    root_files = sorted(
        docs_dir.glob("*.md"),
        key=lambda f: (f.stem != "index", f.stem),
    )
    for f in root_files:
        href = "/" if f.stem == "index" else f"/{f.stem}"
        label = "Home" if f.stem == "index" else _label(f.stem)
        parts.append(f'<a href="{href}"{_active(href)}>{label}</a>')

    # Sub-directories
    for subdir in sorted(d for d in docs_dir.iterdir() if d.is_dir() and not d.name.startswith(".")):
        section_label = _label(subdir.name)
        parts.append(f'<div class="section">{section_label}</div>')
        sub_files = sorted(subdir.glob("*.md"), key=lambda f: (f.stem != "index", f.stem))
        for f in sub_files:
            href = f"/{subdir.name}/" if f.stem == "index" else f"/{subdir.name}/{f.stem}"
            label = "Overview" if f.stem == "index" else _label(f.stem)
            active = ""
            if current_path.startswith(f"/{subdir.name}"):
                # Check more specifically
                if current_path in (href, href + "/", href + ".md") or (
                    f.stem == "index" and current_path == f"/{subdir.name}"
                ):
                    active = ' class="active"'
            parts.append(f'<a href="{href}"{active}>{label}</a>')

    return "\n".join(parts)


def _resolve_path(docs_dir: Path, url_path: str) -> Path | None:
    """Map a URL path to a .md file on disk."""
    path = url_path.rstrip("/") or "/index"
    rel = path.lstrip("/") or "index"

    for candidate in [
        docs_dir / (rel + ".md"),
        docs_dir / rel / "index.md",
    ]:
        if candidate.is_file():
            return candidate

    # Already ends with .md
    if rel.endswith(".md"):
        candidate = docs_dir / rel
        if candidate.is_file():
            return candidate

    return None


class _DocsHandler(http.server.BaseHTTPRequestHandler):
    docs_dir: Path  # set when handler class is created

    def do_GET(self) -> None:
        url_path = unquote(urlparse(self.path).path)
        doc_path = _resolve_path(self.docs_dir, url_path)

        if doc_path is None:
            self._respond(404, _NOT_FOUND)
            return

        md_text = doc_path.read_text(encoding="utf-8")
        content_html = _render_markdown(md_text)

        # Extract <title> from first H1
        title_suffix = ""
        for line in md_text.splitlines():
            if line.startswith("# "):
                title_suffix = " – " + line[2:].strip()
                break

        html = _HTML_TEMPLATE.format(
            title_suffix=title_suffix,
            nav_html=_build_nav(self.docs_dir, url_path),
            content_html=content_html,
        )
        self._respond(200, html)

    def _respond(self, code: int, body: str) -> None:
        data = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args) -> None:  # noqa: A002
        pass  # suppress request logs


def create_server(port: int = 8765) -> socketserver.TCPServer:
    """Create (but do not start) the documentation HTTP server.

    Raises OSError if the port is already in use.
    """
    docs_dir = _get_docs_dir()
    if docs_dir is None:
        raise FileNotFoundError("Documentation directory not found.")

    handler = type("DocsHandler", (_DocsHandler,), {"docs_dir": docs_dir})
    server = socketserver.TCPServer(("127.0.0.1", port), handler)
    server.allow_reuse_address = True
    return server