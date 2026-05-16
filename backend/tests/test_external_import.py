from backend.app import external_import
from backend.app.external_metrics import ExternalMetricsError


def test_import_external_metrics_success_with_duplicates(monkeypatch):
    monkeypatch.setenv("EXTERNAL_API_BASE_URL", "https://example.test")

    calls = {"inserted": 0, "duplicates": 0, "finalized": None}

    monkeypatch.setattr(external_import.db, "ensure_source_app", lambda *args, **kwargs: "s1")
    monkeypatch.setattr(external_import.db, "ensure_data_source", lambda *args, **kwargs: "d1")
    monkeypatch.setattr(external_import.db, "create_ingestion_batch", lambda *args, **kwargs: "b1")

    def fake_insert_raw_record_json(**kwargs):
        if kwargs["payload_json"]["metric_name"] == "Cash ratio":
            calls["inserted"] += 1
            return True
        calls["duplicates"] += 1
        return False

    monkeypatch.setattr(external_import.db, "insert_raw_record_json", fake_insert_raw_record_json)
    monkeypatch.setattr(external_import.db, "insert_raw_record_error", lambda **kwargs: None)

    def fake_finalize_ingestion_batch(**kwargs):
        calls["finalized"] = kwargs

    monkeypatch.setattr(external_import.db, "finalize_ingestion_batch", fake_finalize_ingestion_batch)
    monkeypatch.setattr(
        external_import,
        "fetch_external_metrics",
        lambda _q: {
            "items": [
                {
                    "metric_group": "liquidity",
                    "metric_name": "Cash ratio",
                    "value": 0.0757,
                    "rounded_value": 0.08,
                    "unit": "multiple",
                    "status": "calculated",
                    "year": 2024,
                },
                {
                    "metric_group": "liquidity",
                    "metric_name": "Current ratio",
                    "value": 1.2,
                    "rounded_value": 1.2,
                    "unit": "multiple",
                    "status": "calculated",
                    "year": 2024,
                },
            ],
            "page": 1,
            "page_size": 20,
            "total": 2,
        },
    )

    result = external_import.import_external_metrics({"page": 1, "page_size": 20, "nip": "1234563218"})

    assert result["inserted"] == 7
    assert result["skipped_duplicates"] == 7
    assert calls["finalized"]["status"] == "completed"


def test_import_external_metrics_marks_batch_failed_on_external_error(monkeypatch):
    monkeypatch.setenv("EXTERNAL_API_BASE_URL", "https://example.test")

    state = {"error_logged": False, "finalized": None}

    monkeypatch.setattr(external_import.db, "ensure_source_app", lambda *args, **kwargs: "s1")
    monkeypatch.setattr(external_import.db, "ensure_data_source", lambda *args, **kwargs: "d1")
    monkeypatch.setattr(external_import.db, "create_ingestion_batch", lambda *args, **kwargs: "b1")
    monkeypatch.setattr(external_import.db, "insert_raw_record_json", lambda **kwargs: True)

    def fake_insert_raw_record_error(**kwargs):
        state["error_logged"] = True

    monkeypatch.setattr(external_import.db, "insert_raw_record_error", fake_insert_raw_record_error)

    def fake_finalize_ingestion_batch(**kwargs):
        state["finalized"] = kwargs

    monkeypatch.setattr(external_import.db, "finalize_ingestion_batch", fake_finalize_ingestion_batch)

    def fake_fetch(_q):
        raise ExternalMetricsError(401, "External API returned status 401.")

    monkeypatch.setattr(external_import, "fetch_external_metrics", fake_fetch)

    try:
        external_import.import_external_metrics({"page": 1})
    except ExternalMetricsError:
        pass
    else:
        raise AssertionError("Expected ExternalMetricsError")

    assert state["error_logged"] is True
    assert state["finalized"]["status"] == "failed"
