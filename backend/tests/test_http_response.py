import json
from io import BytesIO

from backend.app import main
from backend.app.main import CompanyHandler


class _FakeHandler(CompanyHandler):
    def __init__(self):
        pass


def _call_json_response(status, payload):
    handler = _FakeHandler.__new__(_FakeHandler)
    captured = {}

    def send_response(code):
        captured["status"] = code

    def send_header(name, value):
        captured.setdefault("headers", {})[name] = value

    def end_headers():
        captured["ended"] = True

    class _Writer:
        def write(self, data):
            captured["body"] = data

    handler.send_response = send_response
    handler.send_header = send_header
    handler.end_headers = end_headers
    handler.wfile = _Writer()

    handler._json_response(status, payload)
    return captured


def test_json_response_formats_payload_and_headers() -> None:
    captured = _call_json_response(201, {"name": "ABC"})
    assert captured["status"] == 201
    assert captured["headers"]["Content-Type"].startswith("application/json")
    assert json.loads(captured["body"].decode("utf-8")) == {"name": "ABC"}


def _build_post_handler(path: str, payload: dict):
    handler = _FakeHandler.__new__(_FakeHandler)
    captured = {}
    raw_body = json.dumps(payload).encode("utf-8")

    def send_response(code):
        captured["status"] = code

    def send_header(name, value):
        captured.setdefault("headers", {})[name] = value

    def end_headers():
        captured["ended"] = True

    class _Writer:
        def write(self, data):
            captured["body"] = data

    handler.path = path
    handler.headers = {"Content-Length": str(len(raw_body))}
    handler.rfile = BytesIO(raw_body)
    handler.wfile = _Writer()
    handler.send_response = send_response
    handler.send_header = send_header
    handler.end_headers = end_headers
    return handler, captured


def test_do_post_persists_company_and_returns_201(monkeypatch) -> None:
    inserted = {}

    def fake_insert_company(name: str) -> None:
        inserted["name"] = name

    monkeypatch.setattr(main, "insert_company", fake_insert_company)
    handler, captured = _build_post_handler("/api/company", {"name": " Firma Testowa SA "})

    handler.do_POST()

    assert captured["status"] == 201
    assert inserted["name"] == "Firma Testowa SA"
    assert json.loads(captured["body"].decode("utf-8")) == {"name": "Firma Testowa SA"}


def test_do_post_returns_500_when_db_insert_fails(monkeypatch) -> None:
    def failing_insert_company(_name: str) -> None:
        raise RuntimeError("db down")

    monkeypatch.setattr(main, "insert_company", failing_insert_company)
    handler, captured = _build_post_handler("/api/company", {"name": "Firma Testowa SA"})

    handler.do_POST()

    assert captured["status"] == 500
    assert json.loads(captured["body"].decode("utf-8")) == {
        "message": "Blad zapisu do bazy danych."
    }


def _build_get_handler(path: str):
    handler = _FakeHandler.__new__(_FakeHandler)
    captured = {}

    def send_response(code):
        captured["status"] = code

    def send_header(name, value):
        captured.setdefault("headers", {})[name] = value

    def end_headers():
        captured["ended"] = True

    class _Writer:
        def write(self, data):
            captured["body"] = data

    handler.path = path
    handler.wfile = _Writer()
    handler.send_response = send_response
    handler.send_header = send_header
    handler.end_headers = end_headers
    return handler, captured


def test_do_get_raw_records_returns_records(monkeypatch) -> None:
    def fake_fetch_raw_records_by_nip(nip: str):
        assert nip == "1234563218"
        return [
            {"id": "r1", "external_id": "1234563218", "record_type": "financial_report"},
            {"id": "r2", "external_id": "1234563218", "record_type": "market_news"},
        ]

    monkeypatch.setattr(main, "fetch_raw_records_by_nip", fake_fetch_raw_records_by_nip)
    handler, captured = _build_get_handler("/api/raw-records?nip=123-456-32-18")

    handler.do_GET()

    payload = json.loads(captured["body"].decode("utf-8"))
    assert captured["status"] == 200
    assert payload["nip"] == "1234563218"
    assert len(payload["records"]) == 2


def test_do_get_raw_records_returns_400_for_invalid_nip() -> None:
    handler, captured = _build_get_handler("/api/raw-records?nip=123")

    handler.do_GET()

    assert captured["status"] == 400
    payload = json.loads(captured["body"].decode("utf-8"))
    assert payload["message"] == "NIP musi miec dokladnie 10 cyfr."


def test_do_get_raw_records_returns_empty_list_for_valid_nip(monkeypatch) -> None:
    monkeypatch.setattr(main, "fetch_raw_records_by_nip", lambda _nip: [])
    handler, captured = _build_get_handler("/api/raw-records?nip=9999999999")

    handler.do_GET()

    assert captured["status"] == 200
    payload = json.loads(captured["body"].decode("utf-8"))
    assert payload["nip"] == "9999999999"
    assert payload["records"] == []


def test_do_post_external_metrics_import_returns_200(monkeypatch) -> None:
    monkeypatch.setattr(
        main,
        "import_external_metrics",
        lambda payload: {
            "batch_id": "b1",
            "inserted": 1,
            "skipped_duplicates": 0,
            "errors": 0,
            "page": 1,
            "page_size": 20,
            "total": 1,
        },
    )
    handler, captured = _build_post_handler(
        "/api/external/metrics/import",
        {"page": 1, "page_size": 20, "nip": "1234563218"},
    )

    handler.do_POST()

    payload = json.loads(captured["body"].decode("utf-8"))
    assert captured["status"] == 200
    assert payload["batch_id"] == "b1"
    assert payload["inserted"] == 1
    assert payload["page"] == 1
    assert payload["page_size"] == 20
    assert payload["total"] == 1


def test_do_post_external_metrics_import_returns_400_for_bad_request(monkeypatch) -> None:
    def raise_external_error(_payload):
        raise main.ExternalMetricsError(400, "Parametr 'page' musi byc >= 1.")

    monkeypatch.setattr(main, "import_external_metrics", raise_external_error)
    handler, captured = _build_post_handler("/api/external/metrics/import", {"page": 0})

    handler.do_POST()

    payload = json.loads(captured["body"].decode("utf-8"))
    assert captured["status"] == 400
    assert "page" in payload["message"]


def test_do_post_external_metrics_import_returns_502_for_external_error(monkeypatch) -> None:
    def raise_external_error(_payload):
        raise main.ExternalMetricsError(401, "External API returned status 401.")

    monkeypatch.setattr(main, "import_external_metrics", raise_external_error)
    handler, captured = _build_post_handler("/api/external/metrics/import", {"page": 1})

    handler.do_POST()

    payload = json.loads(captured["body"].decode("utf-8"))
    assert captured["status"] == 502
    assert "401" in payload["message"]
