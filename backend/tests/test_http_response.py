import json

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
