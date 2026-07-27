#!/usr/bin/env python3
"""Local preview server at http://localhost:8801 — serves dist/site with clean
URLs (directory index resolution). Zero deps: stdlib only."""
import http.server
import os
import socketserver

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, "dist", "site")
PORT = int(os.environ.get("PORT", "8801"))


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=SITE, **k)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache")
        super().end_headers()

    def log_message(self, fmt, *args):
        pass  # quiet


class ReuseTCPServer(socketserver.TCPServer):
    allow_reuse_address = True


if __name__ == "__main__":
    if not os.path.isdir(SITE):
        print("dist/site not found — run `python3 build.py` first.")
        raise SystemExit(1)
    with ReuseTCPServer(("127.0.0.1", PORT), Handler) as httpd:
        print(f"preview → http://localhost:{PORT}  (serving {SITE})")
        httpd.serve_forever()
