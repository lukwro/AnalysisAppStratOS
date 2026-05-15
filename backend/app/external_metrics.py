from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Any
from urllib import error, parse, request


class ExternalMetricsError(RuntimeError):
    def __init__(self, status_code: int, message: str, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.status_code = status_code
        self.details = details or {}


@dataclass
class ExternalMetricsQuery:
    page: int = 1
    page_size: int = 20
    nip: str | None = None
    year: int | None = None


def _validate_digits_only(value: str | None, field_name: str) -> str | None:
    if value is None:
        return None
    if not value.isdigit():
        raise ExternalMetricsError(400, f"Parametr '{field_name}' musi zawierac tylko cyfry.")
    return value


def normalize_query(payload: dict[str, Any]) -> ExternalMetricsQuery:
    page = int(payload.get("page", 1))
    page_size = int(payload.get("page_size", 20))
    if page < 1:
        raise ExternalMetricsError(400, "Parametr 'page' musi byc >= 1.")
    if page_size < 1 or page_size > 100:
        raise ExternalMetricsError(400, "Parametr 'page_size' musi byc w zakresie 1..100.")

    year_raw = payload.get("year")
    year = int(year_raw) if year_raw is not None else None
    nip = _validate_digits_only(payload.get("nip"), "nip")

    return ExternalMetricsQuery(page=page, page_size=page_size, nip=nip, year=year)


def fetch_external_metrics(query: ExternalMetricsQuery) -> dict[str, Any]:
    base_url = os.environ.get("EXTERNAL_API_BASE_URL", "").rstrip("/")
    api_key = os.environ.get("EXTERNAL_API_KEY", "")
    if not base_url:
        raise ExternalMetricsError(500, "Brak konfiguracji EXTERNAL_API_BASE_URL.")
    if not api_key:
        raise ExternalMetricsError(500, "Brak konfiguracji EXTERNAL_API_KEY.")

    params = {
        "page": query.page,
        "page_size": query.page_size,
    }
    if query.nip:
        params["nip"] = query.nip
    if query.year is not None:
        params["year"] = query.year

    url = f"{base_url}/api/v1/external/metrics?{parse.urlencode(params)}"
    req = request.Request(
        url,
        method="GET",
        headers={
            "Accept": "application/json",
            "X-API-Key": api_key,
        },
    )

    try:
        with request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw)
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise ExternalMetricsError(
            exc.code,
            f"External API returned status {exc.code}.",
            {"response_body": body},
        ) from exc
    except error.URLError as exc:
        raise ExternalMetricsError(500, "Brak polaczenia z external API.") from exc
    except json.JSONDecodeError as exc:
        raise ExternalMetricsError(500, "External API zwrocilo niepoprawny JSON.") from exc
