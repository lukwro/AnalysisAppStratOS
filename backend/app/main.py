from __future__ import annotations

import json
import os
import traceback
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .company import CompanyValidationError, create_company_record
from .db import fetch_raw_records_by_nip, init_db, insert_company
from .external_import import import_external_metrics
from .external_metrics import ExternalMetricsError
from .nip import NipValidationError, validate_nip


FRONTEND_FILE = Path(__file__).resolve().parents[2] / "frontend" / "index.html"


class CompanyHandler(BaseHTTPRequestHandler):
    def _json_response(self, status: HTTPStatus, payload: dict) -> None:
        raw = json.dumps(payload, ensure_ascii=False, default=str).encode("utf-8")
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
        parsed = urlparse(self.path)
        if parsed.path == "/api/raw-records":
            nip_values = parse_qs(parsed.query).get("nip")
            nip_value = nip_values[0] if nip_values else None
            try:
                nip = validate_nip(nip_value)
                records = fetch_raw_records_by_nip(nip)
            except NipValidationError as exc:
                self._json_response(HTTPStatus.BAD_REQUEST, {"message": str(exc)})
                return
            except Exception:
                self._json_response(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    {"message": "Blad odczytu z bazy danych."},
                )
                return
            self._json_response(HTTPStatus.OK, {"nip": nip, "records": records})
            return
        self._json_response(HTTPStatus.NOT_FOUND, {"message": "Not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path not in ("/api/company", "/api/external/metrics/import"):
            self._json_response(HTTPStatus.NOT_FOUND, {"message": "Not found"})
            return

        content_length = int(self.headers.get("Content-Length", "0"))
        body = self.rfile.read(content_length)

        if self.path == "/api/external/metrics/import":
            try:
                payload = json.loads(body.decode("utf-8")) if body else {}
                result = import_external_metrics(payload)
            except json.JSONDecodeError:
                self._json_response(
                    HTTPStatus.BAD_REQUEST, {"message": "Niepoprawny JSON."}
                )
                return
            except ExternalMetricsError as exc:
                status = HTTPStatus.BAD_REQUEST if exc.status_code == 400 else HTTPStatus.BAD_GATEWAY
                self._json_response(status, {"message": str(exc), "details": exc.details})
                return
            except Exception:
                traceback.print_exc()
                self._json_response(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    {"message": "Blad importu metryk z external API."},
                )
                return
            self._json_response(HTTPStatus.OK, result)
            return

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
