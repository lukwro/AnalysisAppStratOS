from __future__ import annotations

import os

import psycopg


RAW_SCHEMA_STATEMENTS = [
    """
    CREATE EXTENSION IF NOT EXISTS pgcrypto
    """,
    """
    CREATE TABLE IF NOT EXISTS source_apps (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        code TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        app_type TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'active',
        api_key_hash TEXT,
        owner_team TEXT,
        metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
        last_seen_at TIMESTAMPTZ,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS data_sources (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        source_app_id UUID NOT NULL REFERENCES source_apps(id),
        code TEXT NOT NULL,
        name TEXT NOT NULL,
        source_type TEXT NOT NULL,
        provider TEXT,
        base_url TEXT,
        auth_type TEXT,
        trust_level TEXT,
        schema_hint TEXT,
        refresh_frequency TEXT,
        metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        UNIQUE (source_app_id, code)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS ingestion_batches (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        source_app_id UUID NOT NULL REFERENCES source_apps(id),
        data_source_id UUID REFERENCES data_sources(id),
        trigger_type TEXT NOT NULL,
        batch_key TEXT,
        status TEXT NOT NULL DEFAULT 'received',
        started_at TIMESTAMPTZ,
        finished_at TIMESTAMPTZ,
        record_count INT NOT NULL DEFAULT 0,
        error_count INT NOT NULL DEFAULT 0,
        metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        UNIQUE (source_app_id, batch_key)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS raw_records (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        source_app_id UUID NOT NULL REFERENCES source_apps(id),
        data_source_id UUID REFERENCES data_sources(id),
        ingestion_batch_id UUID REFERENCES ingestion_batches(id),
        external_id TEXT,
        parent_external_id TEXT,
        record_type TEXT NOT NULL,
        content_type TEXT NOT NULL,
        content_format TEXT NOT NULL,
        language_code TEXT,
        title TEXT,
        source_url TEXT,
        payload_text TEXT,
        payload_json JSONB,
        file_storage_uri TEXT,
        file_name TEXT,
        file_size_bytes BIGINT,
        checksum_sha256 TEXT,
        fingerprint TEXT,
        collected_at TIMESTAMPTZ,
        received_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        ingest_status TEXT NOT NULL DEFAULT 'stored',
        processing_status TEXT NOT NULL DEFAULT 'pending',
        metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        CONSTRAINT chk_raw_payload_presence CHECK (
            payload_text IS NOT NULL
            OR payload_json IS NOT NULL
            OR file_storage_uri IS NOT NULL
        )
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS raw_record_files (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        raw_record_id UUID NOT NULL REFERENCES raw_records(id) ON DELETE CASCADE,
        role TEXT NOT NULL,
        storage_uri TEXT NOT NULL,
        file_name TEXT,
        mime_type TEXT,
        size_bytes BIGINT,
        checksum_sha256 TEXT,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS raw_record_errors (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        raw_record_id UUID REFERENCES raw_records(id) ON DELETE CASCADE,
        ingestion_batch_id UUID REFERENCES ingestion_batches(id) ON DELETE CASCADE,
        stage TEXT NOT NULL,
        error_code TEXT NOT NULL,
        error_message TEXT NOT NULL,
        error_details_json JSONB NOT NULL DEFAULT '{}'::jsonb,
        occurred_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS raw_processing_runs (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        raw_record_id UUID NOT NULL REFERENCES raw_records(id) ON DELETE CASCADE,
        processor_name TEXT NOT NULL,
        processor_version TEXT NOT NULL,
        run_type TEXT NOT NULL,
        status TEXT NOT NULL,
        started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
        finished_at TIMESTAMPTZ,
        input_hash TEXT,
        output_json JSONB NOT NULL DEFAULT '{}'::jsonb,
        error_message TEXT,
        created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_raw_records_source_time
        ON raw_records (source_app_id, received_at DESC)
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_raw_records_type_time
        ON raw_records (record_type, received_at DESC)
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_raw_records_processing_status
        ON raw_records (processing_status, received_at DESC)
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_raw_records_external
        ON raw_records (source_app_id, external_id)
        WHERE external_id IS NOT NULL
    """,
    """
    CREATE UNIQUE INDEX IF NOT EXISTS uq_raw_records_checksum_source
        ON raw_records (source_app_id, checksum_sha256)
        WHERE checksum_sha256 IS NOT NULL
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_raw_records_payload_json_gin
        ON raw_records USING GIN (payload_json)
    """,
    """
    CREATE INDEX IF NOT EXISTS idx_raw_records_metadata_json_gin
        ON raw_records USING GIN (metadata_json)
    """,
]


def get_db_connection() -> psycopg.Connection:
    database_url = os.environ.get("DATABASE_URL")
    if database_url:
        return psycopg.connect(database_url)

    host = os.environ.get("DB_HOST") or os.environ.get("PGHOST", "127.0.0.1")
    port = os.environ.get("DB_PORT") or os.environ.get("PGPORT", "5432")
    dbname = os.environ.get("DB_NAME") or os.environ.get("PGDATABASE", "analysis_app")
    user = os.environ.get("DB_USER") or os.environ.get("PGUSER", "analysis_user")
    password = os.environ.get("DB_PASSWORD") or os.environ.get("PGPASSWORD", "analysis_pass")

    conn_string = (
        f"host={host} port={port} dbname={dbname} user={user} password={password}"
    )
    return psycopg.connect(conn_string)


def init_db() -> None:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS companies (
                    id BIGSERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                )
                """
            )
            for statement in RAW_SCHEMA_STATEMENTS:
                cur.execute(statement)
        conn.commit()


def insert_company(name: str) -> None:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO companies (name) VALUES (%s)", (name,))
        conn.commit()
