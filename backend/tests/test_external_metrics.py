import pytest

from backend.app.external_metrics import ExternalMetricsError, normalize_query


def test_normalize_query_uses_defaults() -> None:
    q = normalize_query({})
    assert q.page == 1
    assert q.page_size == 20
    assert q.nip is None
    assert q.year is None


def test_normalize_query_validates_page_size() -> None:
    with pytest.raises(ExternalMetricsError):
        normalize_query({"page_size": 101})


def test_normalize_query_validates_nip_digits() -> None:
    with pytest.raises(ExternalMetricsError):
        normalize_query({"nip": "123-45"})
