#!/usr/bin/env python3
"""Simple static file server for Covenant School website."""
import http.server
import os
import socketserver
from pathlib import Path

PORT = 5000
PAGES_DIR = Path(__file__).parent / "pages"
ASSETS_DIR = Path(__file__).parent / "assets"
PDFS_DIR = Path(__file__).parent / "pdfs"


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/")

        # Route /assets/* to the assets directory
        if path.startswith("/assets/"):
            file_path = ASSETS_DIR / path[len("/assets/"):]
            self.serve_file(file_path)
            return

        # Route /pdfs/* to the pdfs directory
        if path.startswith("/pdfs/"):
            file_path = PDFS_DIR / path[len("/pdfs/"):]
            self.serve_file(file_path)
            return

        # Root → index.html
        if path == "" or path == "/":
            self.serve_file(PAGES_DIR / "index.html")
            return

        # Try exact match as HTML page
        clean = path.lstrip("/")
        candidates = [
            PAGES_DIR / clean,
            PAGES_DIR / (clean + ".html"),
        ]
        for candidate in candidates:
            if candidate.exists():
                self.serve_file(candidate)
                return

        # 404
        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"Page not found")

    def serve_file(self, path: Path):
        if not path.exists():
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return
        suffix = path.suffix.lower()
        content_types = {
            ".html": "text/html; charset=utf-8",
            ".css": "text/css",
            ".js": "application/javascript",
            ".png": "image/png",
            ".jpg": "image/jpeg",
            ".jpeg": "image/jpeg",
            ".webp": "image/webp",
            ".pdf": "application/pdf",
            ".svg": "image/svg+xml",
            ".ico": "image/x-icon",
            ".woff": "font/woff",
            ".woff2": "font/woff2",
        }
        content_type = content_types.get(suffix, "application/octet-stream")
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        print(f"{self.address_string()} - {format % args}")


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Serving Covenant School website on port {PORT}")
        httpd.serve_forever()
