#!/usr/bin/env python3
"""Simple static file server for Covenant School website."""
import http.server
import json
import os
import smtplib
import socketserver
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path
import email.parser
import email.policy

PORT = 5000
PAGES_DIR = Path(__file__).parent / "pages"
ASSETS_DIR = Path(__file__).parent / "assets"
PDFS_DIR = Path(__file__).parent / "pdfs"

RECIPIENT_EMAIL = "fboren@covenantschool.com"


def parse_multipart(headers, body_bytes):
    """Parse multipart/form-data into (fields_dict, files_dict) using stdlib."""
    content_type = headers.get('Content-Type', '')
    raw = f"Content-Type: {content_type}\r\n\r\n".encode('utf-8') + body_bytes
    msg = email.parser.BytesParser(policy=email.policy.compat32).parsebytes(raw)
    fields, files = {}, {}
    if not msg.is_multipart():
        return fields, files
    for part in msg.get_payload():
        cd = part.get('Content-Disposition', '')
        name = filename = None
        for item in cd.split(';'):
            item = item.strip()
            if item.startswith('name='):
                name = item[5:].strip('"')
            elif item.startswith('filename='):
                filename = item[9:].strip('"')
        if name is None:
            continue
        payload = part.get_payload(decode=True) or b''
        if filename:
            files[name] = {
                'filename': filename,
                'data': payload,
                'content_type': part.get_content_type(),
            }
        else:
            fields[name] = payload.decode('utf-8', errors='replace')
    return fields, files


class Handler(http.server.SimpleHTTPRequestHandler):

    def _safe_resolve(self, base: Path, rel: str):
        """Resolve a relative path under base, returning None if it escapes."""
        try:
            resolved = (base / rel).resolve()
            if resolved.is_relative_to(base.resolve()):
                return resolved
        except Exception:
            pass
        return None

    # ── GET ────────────────────────────────────────────────────────────────

    def do_GET(self):
        path = self.path.split("?")[0].rstrip("/")

        if path.startswith("/assets/"):
            rel = path[len("/assets/"):]
            file_path = self._safe_resolve(ASSETS_DIR, rel)
            if file_path is None:
                self.send_response(403)
                self.end_headers()
                return
            self.serve_file(file_path)
            return

        if path.startswith("/pdfs/"):
            rel = path[len("/pdfs/"):]
            file_path = self._safe_resolve(PDFS_DIR, rel)
            if file_path is None:
                self.send_response(403)
                self.end_headers()
                return
            self.serve_file(file_path)
            return

        if path in ("", "/"):
            self.serve_file(PAGES_DIR / "index.html")
            return

        clean = path.lstrip("/")
        for suffix in ("", ".html"):
            file_path = self._safe_resolve(PAGES_DIR, clean + suffix)
            if file_path and file_path.exists():
                self.serve_file(file_path)
                return

        self.send_response(404)
        self.end_headers()
        self.wfile.write(b"Page not found")

    # ── POST ───────────────────────────────────────────────────────────────

    def do_POST(self):
        path = self.path.split("?")[0]
        if path == "/submit-employment":
            self.handle_employment_form()
            return
        self.send_response(404)
        self.end_headers()

    def handle_employment_form(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)

        try:
            fields, files = parse_multipart(self.headers, body)
        except Exception as e:
            print(f"Form parse error: {e}")
            self._json({"success": False, "error": "Could not read the form. Please try again."})
            return

        name     = fields.get('full_name', '').strip()
        email_addr = fields.get('email', '').strip()
        phone    = fields.get('phone', '').strip()
        position = fields.get('position', '').strip()
        comments = fields.get('comments', '').strip()
        resume   = files.get('resume')

        if not all([name, email_addr, phone, position, comments]):
            self._json({"success": False, "error": "Please fill in all required fields."})
            return

        try:
            self._send_email(name, email_addr, phone, position, comments, resume)
            self._json({"success": True})
        except ValueError as e:
            # Config error — tell user to contact directly
            print(f"SMTP config error: {e}")
            self._json({"success": False, "error": str(e)})
        except Exception as e:
            print(f"Email send error: {e}")
            self._json({"success": False,
                        "error": "Unable to send your application right now. "
                                 "Please email us directly at info@covenantschool.com."})

    def _send_email(self, name, email_addr, phone, position, comments, resume):
        smtp_host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
        smtp_port = int(os.environ.get('SMTP_PORT', '587'))
        smtp_user = os.environ.get('SMTP_USER', '')
        smtp_pass = os.environ.get('SMTP_PASS', '')

        if not smtp_user or not smtp_pass:
            raise ValueError(
                "The email server hasn't been configured yet. "
                "Please contact us directly at info@covenantschool.com."
            )

        msg = MIMEMultipart()
        msg['From']     = f"Covenant School Website <{smtp_user}>"
        msg['To']       = RECIPIENT_EMAIL
        msg['Reply-To'] = email_addr
        msg['Subject']  = f"Employment Application: {name} \u2014 {position}"

        resume_line = (f"\nRésumé attached: {resume['filename']}" if resume and resume.get('filename') else "")
        body = f"""\
New Employment Application submitted via the Covenant Christian School website.

{'─'*50}
APPLICANT DETAILS
{'─'*50}
Name:      {name}
Email:     {email_addr}
Phone:     {phone}
Position:  {position}

COMMENTS / QUALIFICATIONS
{'─'*50}
{comments}
{resume_line}
"""
        msg.attach(MIMEText(body, 'plain'))

        if resume and resume.get('data') and resume.get('filename'):
            att = MIMEApplication(resume['data'], Name=resume['filename'])
            att['Content-Disposition'] = f'attachment; filename="{resume["filename"]}"'
            msg.attach(att)

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

    # ── Helpers ────────────────────────────────────────────────────────────

    def _json(self, data):
        body = json.dumps(data).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def serve_file(self, path: Path):
        if not path.exists():
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Not found")
            return
        content_types = {
            '.html': 'text/html; charset=utf-8',
            '.css': 'text/css',
            '.js': 'application/javascript',
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.webp': 'image/webp',
            '.pdf': 'application/pdf',
            '.svg': 'image/svg+xml',
            '.ico': 'image/x-icon',
            '.woff': 'font/woff',
            '.woff2': 'font/woff2',
        }
        content_type = content_types.get(path.suffix.lower(), 'application/octet-stream')
        data = path.read_bytes()
        self.send_response(200)
        self.send_header('Content-Type', content_type)
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        print(f"{self.address_string()} - {fmt % args}")


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        print(f"Serving Covenant School website on port {PORT}")
        httpd.serve_forever()
