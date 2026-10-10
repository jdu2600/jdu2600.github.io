"""Local preview of index.html without installing Jekyll.

Renders the Liquid template with _data/*.yml (re-rendered on every page load,
so edit the YAML and refresh) and serves the repo at http://127.0.0.1:8765/.
PDF links under /conference_talks/ are served from a sibling checkout of the
conference_talks repo, if there is one.

    pip install python-liquid pyyaml
    python _preview.py
"""
import functools
import http.server
import pathlib
import urllib.parse
import webbrowser

import liquid
import yaml

ROOT = pathlib.Path(__file__).resolve().parent
ARCHIVE = ROOT.parent / "conference_talks"
PORT = 8765


def render():
    src = (ROOT / "index.html").read_text(encoding="utf-8")
    if src.startswith("---"):
        src = src.split("---", 2)[2].lstrip("\n")  # drop Jekyll front matter
    data = {p.stem: yaml.safe_load(p.read_text(encoding="utf-8"))
            for p in (ROOT / "_data").glob("*.yml")}
    return liquid.Environment().from_string(src).render(site={"data": data})


class Handler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = urllib.parse.unquote(path.split("?")[0])
        if path.startswith("/conference_talks/"):
            return str(ARCHIVE / path.removeprefix("/conference_talks/"))
        return super().translate_path(path)

    def do_GET(self):
        if self.path.split("?")[0] in ("/", "/index.html"):
            try:
                body, status = render().encode("utf-8"), 200
            except Exception as e:  # show template/YAML errors in the browser
                body, status = f"<pre>{e}</pre>".encode("utf-8"), 500
            self.send_response(status)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()


if __name__ == "__main__":
    url = f"http://127.0.0.1:{PORT}/"
    server = http.server.ThreadingHTTPServer(
        ("127.0.0.1", PORT), functools.partial(Handler, directory=str(ROOT)))
    print(f"Previewing at {url} (Ctrl+C to stop)")
    webbrowser.open(url)
    server.serve_forever()
