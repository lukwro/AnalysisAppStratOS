from __future__ import annotations

import hashlib
import json
import os
from dataclasses import asdict
from typing import Any, Iterator

from . import db
from .external_metrics import ExternalMetricsError, normalize_query, fetch_external_metrics


def _item_checksum(item: dict[str, Any]) -> str:
    canonical = json.dumps(item, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _build_external_id(nip: str | None, item: dict[str, Any], page: int) -> str:
    return ":".join(
        [
            nip or "none",
            str(item.get("year", "none")),
            str(item.get("metric_group", "none")),
            str(item.get("metric_name", "none")),
            str(page),
        ]
    )


def _raw_value_parts(value: Any) -> dict[str, Any]:
    parts: dict[str, Any] = {
        "raw_value_text": None,
        "raw_value_number": None,
        "raw_value_boolean": None,
        "raw_value_date": None,
        "raw_value_timestamp": None,
        "raw_value_json": None,
    }
    if isinstance(value, bool):
        parts["raw_value_boolean"] = value
    elif isinstance(value, (int, float)):
        parts["raw_value_number"] = value
    elif isinstance(value, str):
        parts["raw_value_text"] = value
    elif value is not None:
        parts["raw_value_json"] = value
    return parts


def _atomic_fields(value: Any, prefix: str = "") -> Iterator[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, nested in value.items():
            label = f"{prefix}.{key}" if prefix else str(key)
            yield from _atomic_fields(nested, label)
        return
    if isinstance(value, list):
        for index, nested in enumerate(value):
            label = f"{prefix}[{index}]" if prefix else f"[{index}]"
            yield from _atomic_fields(nested, label)
        return
    label = prefix or "value"
    yield (label, value)


def _atomic_checksum(item_checksum: str, label: str, value: Any) -> str:
    canonical = json.dumps({"label": label, "value": value}, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(f"{item_checksum}:{canonical}".encode("utf-8")).hexdigest()


def import_external_metrics(payload: dict[str, Any]) -> dict[str, Any]:
    query = normalize_query(payload)
    source_app_id = db.ensure_source_app("external_finance_api", "External Finance API")
    data_source_id = db.ensure_data_source(
        source_app_id=source_app_id,
        code="external_metrics_v1",
        name="External Metrics API v1",
        base_url=(os.environ.get("EXTERNAL_API_BASE_URL") or "").rstrip("/"),
    )
    batch_key = (
        f"metrics:{query.page}:{query.page_size}:{query.nip or 'none'}:{query.year or 'none'}"
    )
    batch_id = db.create_ingestion_batch(
        source_app_id=source_app_id,
        data_source_id=data_source_id,
        trigger_type="manual",
        batch_key=batch_key,
        metadata_json=asdict(query),
    )

    inserted_count = 0
    skipped_duplicates = 0
    error_count = 0
    try:
        response = fetch_external_metrics(query)
        items = response.get("items", [])
        if not isinstance(items, list):
            raise ExternalMetricsError(500, "Pole 'items' musi byc tablica.")

        for item in items:
            if not isinstance(item, dict):
                error_count += 1
                db.insert_raw_record_error(
                    ingestion_batch_id=batch_id,
                    stage="store",
                    error_code="INVALID_ITEM",
                    error_message="Element items[] nie jest obiektem JSON.",
                    error_details_json={"item": item},
                )
                continue

            item_checksum = _item_checksum(item)
            for raw_label, raw_value in _atomic_fields(item):
                inserted = db.insert_raw_record_json(
                    source_app_id=source_app_id,
                    data_source_id=data_source_id,
                    ingestion_batch_id=batch_id,
                    external_id=_build_external_id(query.nip, item, query.page),
                    record_type="financial_metric",
                    payload_json=item,
                    checksum_sha256=_atomic_checksum(item_checksum, raw_label, raw_value),
                    nip=query.nip,
                    year=query.year,
                    page=query.page,
                    page_size=query.page_size,
                    total=response.get("total"),
                    metric_group=item.get("metric_group"),
                    metric_name=item.get("metric_name"),
                    unit=item.get("unit"),
                    metric_status=item.get("status"),
                    raw_label=raw_label,
                    **_raw_value_parts(raw_value),
                )
                if inserted:
                    inserted_count += 1
                else:
                    skipped_duplicates += 1

        final_metadata = {
            **asdict(query),
            "total": response.get("total"),
            "skipped_duplicates": skipped_duplicates,
        }
        db.finalize_ingestion_batch(
            batch_id=batch_id,
            status="completed",
            record_count=inserted_count,
            error_count=error_count,
            metadata_json=final_metadata,
        )
        return {
            "batch_id": batch_id,
            "inserted": inserted_count,
            "skipped_duplicates": skipped_duplicates,
            "errors": error_count,
            "page": response.get("page"),
            "page_size": response.get("page_size"),
            "total": response.get("total"),
        }
    except ExternalMetricsError as exc:
        error_count += 1
        db.insert_raw_record_error(
            ingestion_batch_id=batch_id,
            stage="fetch",
            error_code=f"EXT_API_{exc.status_code}",
            error_message=str(exc),
            error_details_json=exc.details,
        )
        db.finalize_ingestion_batch(
            batch_id=batch_id,
            status="failed",
            record_count=inserted_count,
            error_count=error_count,
            metadata_json={
                **asdict(query),
                "skipped_duplicates": skipped_duplicates,
                "error_status": exc.status_code,
            },
        )
        raise
    except Exception as exc:
        error_count += 1
        db.insert_raw_record_error(
            ingestion_batch_id=batch_id,
            stage="store",
            error_code="DB_WRITE_FAILED",
            error_message=str(exc),
            error_details_json={},
        )
        db.finalize_ingestion_batch(
            batch_id=batch_id,
            status="failed",
            record_count=inserted_count,
            error_count=error_count,
            metadata_json={**asdict(query), "skipped_duplicates": skipped_duplicates},
        )
        raise
