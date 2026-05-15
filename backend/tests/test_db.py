from backend.app import db


def test_get_db_connection_uses_env_vars(monkeypatch):
    captured = {}

    def fake_connect(conn_string):
        captured["conn_string"] = conn_string
        return object()

    monkeypatch.setenv("DB_HOST", "db.local")
    monkeypatch.setenv("DB_PORT", "5544")
    monkeypatch.setenv("DB_NAME", "mydb")
    monkeypatch.setenv("DB_USER", "myuser")
    monkeypatch.setenv("DB_PASSWORD", "secret")
    monkeypatch.setattr(db.psycopg, "connect", fake_connect)

    db.get_db_connection()

    assert "host=db.local" in captured["conn_string"]
    assert "port=5544" in captured["conn_string"]
    assert "dbname=mydb" in captured["conn_string"]
    assert "user=myuser" in captured["conn_string"]
