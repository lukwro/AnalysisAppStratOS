from __future__ import annotations

import os

import psycopg


def get_db_connection() -> psycopg.Connection:
    host = os.environ.get("DB_HOST", "127.0.0.1")
    port = os.environ.get("DB_PORT", "5432")
    dbname = os.environ.get("DB_NAME", "analysis_app")
    user = os.environ.get("DB_USER", "analysis_user")
    password = os.environ.get("DB_PASSWORD", "analysis_pass")

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
        conn.commit()


def insert_company(name: str) -> None:
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO companies (name) VALUES (%s)", (name,))
        conn.commit()
