from __future__ import annotations

import json
import os
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .company import CompanyValidationError, create_company_record
from .db import init_db, insert_company


FRONTEND_FILE = Path(__file__).resolve().parents[2] / "frontend" / "index.html"


class CompanyHandler(BaseHTTPRequestHandler):
    def _json_response(self, status: HTTPStatus, payload: dict) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def _html_response(self, html: str) -> None:
        raw = html.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/", "/index.html"):
            self._html_response(FRONTEND_FILE.read_text(encoding="utf-8"))
            return
        self._json_response(HTTPStatus.NOT_FOUND, {"message": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/api/company":
            self._json_response(HTTPStatus.NOT_FOUND, {"message": "Not found"})
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length)

        try:
            payload = json.loads(body.decode("utf-8"))
            record = create_company_record(payload.get("name"))
        except json.JSONDecodeError:
            self._json_response(HTTPStatus.BAD_REQUEST, {"message": "Niepoprawny JSON."})
            return
        except CompanyValidationError as exc:
            self._json_response(HTTPStatus.BAD_REQUEST, {"message": str(exc)})
            return
        try:
            insert_company(record.name)
        except Exception:
            self._json_response(
                HTTPStatus.INTERNAL_SERVER_ERROR,
                {"message": "Blad zapisu do bazy danych."},
            )
            return

        self._json_response(HTTPStatus.CREATED, {"name": record.name})


def run_server(host: str = "0.0.0.0", port: int = 8000) -> None:
    init_db()
    server = ThreadingHTTPServer((host, port), CompanyHandler)
    print(f"Server listening at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    app_port = int(os.environ.get("PORT", "8000"))
    run_server(port=app_port)
