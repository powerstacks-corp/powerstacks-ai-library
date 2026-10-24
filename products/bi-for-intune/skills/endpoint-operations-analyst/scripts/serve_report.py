"""Preview a generated report on this computer only.

Usage:
    python serve_report.py --file briefing.html [--port N] [--no-browser]

Serves only the report file at http://127.0.0.1:<port>/ and opens it in the
default browser. The server listens on the loopback address only, so other
computers cannot reach it, serves no other file, and rejects requests that are
not addressed to 127.0.0.1 or localhost. Press Ctrl+C to stop.
This is a local proof of concept, not a production hosting method.
Uses only the Python standard library.
"""

import argparse
import http.server
import os
import sys
import urllib.parse
import webbrowser


class ReportHandler(http.server.BaseHTTPRequestHandler):
    """Serve one file only, and only to requests addressed to the loopback host."""

    report_path = None
    allowed_hosts = ()

    def log_message(self, fmt, *args):
        pass

    def _send(self, code, body, ctype="text/plain; charset=utf-8"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "no-referrer")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def do_GET(self):
        if self.headers.get("Host", "") not in self.allowed_hosts:
            return self._send(403, b"Forbidden")
        path = urllib.parse.urlsplit(self.path).path
        if path not in ("/", "/" + urllib.parse.quote(os.path.basename(self.report_path))):
            return self._send(404, b"Not found")
        with open(self.report_path, "rb") as f:
            self._send(200, f.read(), "text/html; charset=utf-8")

    do_HEAD = do_GET


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--file", required=True, help="Report .html file to preview")
    ap.add_argument("--port", type=int, default=0, help="Port (default: a free port chosen by the system)")
    ap.add_argument("--no-browser", action="store_true")
    args = ap.parse_args(argv)

    path = os.path.abspath(args.file)
    if not os.path.isfile(path):
        sys.exit(f"Report not found: {path}")
    name = os.path.basename(path)
    server = http.server.ThreadingHTTPServer(("127.0.0.1", args.port), ReportHandler)
    port = server.server_address[1]
    ReportHandler.report_path = path
    ReportHandler.allowed_hosts = (f"127.0.0.1:{port}", f"localhost:{port}")
    url = f"http://127.0.0.1:{port}/{urllib.parse.quote(name)}"
    print(f"Serving {name} at {url} (this computer only). Press Ctrl+C to stop.")
    if not args.no_browser:
        webbrowser.open(url)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
