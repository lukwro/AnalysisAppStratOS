from backend.app import db


def test_get_db_connection_prefers_database_url(monkeypatch):
    captured = {}

    def fake_connect(conn_string):
        captured["conn_string"] = conn_string
        return object()

    monkeypatch.setenv("DATABASE_URL", "postgresql://user:pass@host:5432/name")
    monkeypatch.setattr(db.psycopg, "connect", fake_connect)

    db.get_db_connection()

    assert captured["conn_string"] == "postgresql://user:pass@host:5432/name"


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


def test_get_db_connection_falls_back_to_pg_env_vars(monkeypatch):
    captured = {}

    def fake_connect(conn_string):
        captured["conn_string"] = conn_string
        return object()

    monkeypatch.setenv("PGHOST", "pg.internal")
    monkeypatch.setenv("PGPORT", "6432")
    monkeypatch.setenv("PGDATABASE", "pgdb")
    monkeypatch.setenv("PGUSER", "pguser")
    monkeypatch.setenv("PGPASSWORD", "pgsecret")
    monkeypatch.setattr(db.psycopg, "connect", fake_connect)

    db.get_db_connection()

    assert "host=pg.internal" in captured["conn_string"]
    assert "port=6432" in captured["conn_string"]
    assert "dbname=pgdb" in captured["conn_string"]
    assert "user=pguser" in captured["conn_string"]


class _FakeCursor:
    def __init__(self) -> None:
        self.executed: list[str] = []
        self.last_params = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False

    def execute(self, statement: str, _params=None) -> None:
        self.executed.append(statement)
        self.last_params = _params

    def fetchone(self):
        return None


class _FakeConnection:
    def __init__(self) -> None:
        self.cursor_obj = _FakeCursor()
        self.committed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb) -> bool:
        return False

    def cursor(self) -> _FakeCursor:
        return self.cursor_obj

    def commit(self) -> None:
        self.committed = True


def test_init_db_creates_companies_and_raw_schema(monkeypatch):
    fake_conn = _FakeConnection()

    def fake_get_db_connection():
        return fake_conn

    monkeypatch.setattr(db, "get_db_connection", fake_get_db_connection)

    db.init_db()

    executed_sql = "\n".join(fake_conn.cursor_obj.executed)
    assert "CREATE TABLE IF NOT EXISTS companies" in executed_sql
    assert "CREATE TABLE IF NOT EXISTS source_apps" in executed_sql
    assert "CREATE TABLE IF NOT EXISTS data_sources" in executed_sql
    assert "CREATE TABLE IF NOT EXISTS ingestion_batches" in executed_sql
    assert "CREATE TABLE IF NOT EXISTS raw_records" in executed_sql
    assert "CREATE TABLE IF NOT EXISTS raw_record_files" in executed_sql
    assert "CREATE TABLE IF NOT EXISTS raw_record_errors" in executed_sql
    assert "CREATE TABLE IF NOT EXISTS raw_processing_runs" in executed_sql
    assert fake_conn.committed is True


def test_raw_schema_contains_payload_constraint():
    ddl = "\n".join(db.RAW_SCHEMA_STATEMENTS)
    assert "CONSTRAINT chk_raw_payload_presence CHECK" in ddl
    assert "payload_text IS NOT NULL" in ddl
    assert "payload_json IS NOT NULL" in ddl
    assert "file_storage_uri IS NOT NULL" in ddl


def test_raw_schema_contains_critical_indexes():
    ddl = "\n".join(db.RAW_SCHEMA_STATEMENTS)
    assert "idx_raw_records_source_time" in ddl
    assert "idx_raw_records_type_time" in ddl
    assert "idx_raw_records_processing_status" in ddl
    assert "idx_raw_records_external" in ddl
    assert "uq_raw_records_checksum_source" in ddl
    assert "idx_raw_records_payload_json_gin" in ddl
    assert "idx_raw_records_metadata_json_gin" in ddl


def test_fetch_raw_records_by_nip_returns_rows(monkeypatch):
    class _FetchCursor(_FakeCursor):
        def __init__(self) -> None:
            super().__init__()
            self.rows = [{"id": "a1"}, {"id": "a2"}]

        def fetchall(self):
            return self.rows

    class _FetchConnection(_FakeConnection):
        def __init__(self) -> None:
            self.cursor_obj = _FetchCursor()
            self.committed = False

        def cursor(self, row_factory=None):
            return self.cursor_obj

    fake_conn = _FetchConnection()

    def fake_get_db_connection():
        return fake_conn

    monkeypatch.setattr(db, "get_db_connection", fake_get_db_connection)

    result = db.fetch_raw_records_by_nip("1234567890")

    assert result == [{"id": "a1"}, {"id": "a2"}]
    executed_sql = "\n".join(fake_conn.cursor_obj.executed)
    assert "FROM raw_records" in executed_sql


def test_insert_raw_record_json_uses_on_conflict_do_nothing(monkeypatch):
    class _InsertCursor(_FakeCursor):
        def __init__(self) -> None:
            super().__init__()
            self.return_inserted = True

        def fetchone(self):
            return ("new-id",) if self.return_inserted else None

    class _InsertConnection(_FakeConnection):
        def __init__(self) -> None:
            self.cursor_obj = _InsertCursor()
            self.committed = False

    fake_conn = _InsertConnection()

    monkeypatch.setattr(db, "get_db_connection", lambda: fake_conn)

    inserted = db.insert_raw_record_json(
        source_app_id="s1",
        data_source_id="d1",
        ingestion_batch_id="b1",
        external_id="ext1",
        record_type="financial_metric",
        payload_json={"metric_name": "Cash ratio"},
        checksum_sha256="abc123",
        metadata_json={"page": 1},
    )

    assert inserted is True
    executed_sql = "\n".join(fake_conn.cursor_obj.executed)
    assert "ON CONFLICT (source_app_id, checksum_sha256)" in executed_sql
    assert "WHERE checksum_sha256 IS NOT NULL" in executed_sql
    assert "DO NOTHING" in executed_sql
