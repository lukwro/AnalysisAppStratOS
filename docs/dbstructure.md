# Schemat bazy danych dla warstwy surowej (RAW)

## 1. Cel
Warstwa `RAW` ma przyjąć dane z wielu aplikacji i formatów (`json`, `xml`, `xhtml`, `html`, `pdf`, `csv`, `txt`) bez utraty oryginału, z pełnym audytem i możliwością ponownego przetwarzania.

## 2. Założenia projektowe
- Zawsze przechowuj oryginalny payload lub referencję do pliku binarnego.
- Nie narzucaj jednego modelu biznesowego na etapie RAW.
- Każdy rekord musi mieć pochodzenie (`source app`, `source`, `external id`, `timestamps`).
- Dane surowe mogą być duplikowane - deduplikacja po `checksum/fingerprint`.
- Przetwarzanie jest asynchroniczne i wersjonowane.

## 3. Model RAW (PostgreSQL)

### 3.1 Slowniki zrodel
```sql
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE source_apps (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    code TEXT NOT NULL UNIQUE,
    name TEXT NOT NULL,
    app_type TEXT NOT NULL, -- internal, external, manual, crawler
    status TEXT NOT NULL DEFAULT 'active',
    api_key_hash TEXT,
    owner_team TEXT,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    last_seen_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE data_sources (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_app_id UUID NOT NULL REFERENCES source_apps(id),
    code TEXT NOT NULL,
    name TEXT NOT NULL,
    source_type TEXT NOT NULL, -- api, file_upload, webhook, scraper, email
    provider TEXT,
    base_url TEXT,
    auth_type TEXT,
    trust_level TEXT, -- low, medium, high
    schema_hint TEXT,
    refresh_frequency TEXT,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source_app_id, code)
);
```

### 3.2 Batch ingestu (jedno pobranie/import)
```sql
CREATE TABLE ingestion_batches (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_app_id UUID NOT NULL REFERENCES source_apps(id),
    data_source_id UUID REFERENCES data_sources(id),
    trigger_type TEXT NOT NULL, -- schedule, manual, webhook, retry
    batch_key TEXT,             -- np. id joba z systemu zewnetrznego
    status TEXT NOT NULL DEFAULT 'received', -- received, processing, partial, completed, failed
    started_at TIMESTAMPTZ,
    finished_at TIMESTAMPTZ,
    record_count INT NOT NULL DEFAULT 0,
    error_count INT NOT NULL DEFAULT 0,
    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    UNIQUE (source_app_id, batch_key)
);
```

### 3.3 Głowna tabela surowych rekordow
```sql
CREATE TABLE raw_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    source_app_id UUID NOT NULL REFERENCES source_apps(id),
    data_source_id UUID REFERENCES data_sources(id),
    ingestion_batch_id UUID REFERENCES ingestion_batches(id),

    external_id TEXT,
    parent_external_id TEXT,
    record_type TEXT NOT NULL,         -- financial_report, customer_list, market_news, indicator_dump
    content_type TEXT NOT NULL,        -- application/json, text/xml, text/html, application/pdf
    content_format TEXT NOT NULL,      -- json, xml, xhtml, html, pdf, csv, txt, unknown
    language_code TEXT,

    title TEXT,
    source_url TEXT,

    payload_text TEXT,                 -- dla tekstow/xml/html
    payload_json JSONB,                -- dla jsonow
    file_storage_uri TEXT,             -- np. s3://... lub local path
    file_name TEXT,
    file_size_bytes BIGINT,

    checksum_sha256 TEXT,
    fingerprint TEXT,                  -- hash stabilny po normalizacji

    collected_at TIMESTAMPTZ,
    received_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    ingest_status TEXT NOT NULL DEFAULT 'stored',       -- stored, rejected, quarantined
    processing_status TEXT NOT NULL DEFAULT 'pending',  -- pending, running, processed, failed

    metadata_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),

    CONSTRAINT chk_raw_payload_presence CHECK (
        payload_text IS NOT NULL
        OR payload_json IS NOT NULL
        OR file_storage_uri IS NOT NULL
    )
);
```

### 3.4 Zalaczniki i pliki powiazane
```sql
CREATE TABLE raw_record_files (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    raw_record_id UUID NOT NULL REFERENCES raw_records(id) ON DELETE CASCADE,
    role TEXT NOT NULL, -- original, attachment, extracted_text, preview
    storage_uri TEXT NOT NULL,
    file_name TEXT,
    mime_type TEXT,
    size_bytes BIGINT,
    checksum_sha256 TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### 3.5 Błędy ingestu i parsowania RAW
```sql
CREATE TABLE raw_record_errors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    raw_record_id UUID REFERENCES raw_records(id) ON DELETE CASCADE,
    ingestion_batch_id UUID REFERENCES ingestion_batches(id) ON DELETE CASCADE,
    stage TEXT NOT NULL, -- validate, decode, parse, store
    error_code TEXT NOT NULL,
    error_message TEXT NOT NULL,
    error_details_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    occurred_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

### 3.6 Dziennik przetwarzania surowych rekordow
```sql
CREATE TABLE raw_processing_runs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    raw_record_id UUID NOT NULL REFERENCES raw_records(id) ON DELETE CASCADE,
    processor_name TEXT NOT NULL,
    processor_version TEXT NOT NULL,
    run_type TEXT NOT NULL, -- extract_text, classify, extract_financials
    status TEXT NOT NULL,   -- running, success, failed
    started_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    finished_at TIMESTAMPTZ,
    input_hash TEXT,
    output_json JSONB NOT NULL DEFAULT '{}'::jsonb,
    error_message TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
```

## 4. Indeksy (krytyczne dla skali)
```sql
CREATE INDEX idx_raw_records_source_time
    ON raw_records (source_app_id, received_at DESC);

CREATE INDEX idx_raw_records_type_time
    ON raw_records (record_type, received_at DESC);

CREATE INDEX idx_raw_records_processing_status
    ON raw_records (processing_status, received_at DESC);

CREATE INDEX idx_raw_records_external
    ON raw_records (source_app_id, external_id)
    WHERE external_id IS NOT NULL;

CREATE UNIQUE INDEX uq_raw_records_checksum_source
    ON raw_records (source_app_id, checksum_sha256)
    WHERE checksum_sha256 IS NOT NULL;

CREATE INDEX idx_raw_records_payload_json_gin
    ON raw_records USING GIN (payload_json);

CREATE INDEX idx_raw_records_metadata_json_gin
    ON raw_records USING GIN (metadata_json);
```

## 5. Kontrakty danych wejsciowych (minimum)
- `source_app_id` wymagane.
- `record_type` wymagane.
- `content_type` i `content_format` wymagane.
- Jeden z: `payload_text` / `payload_json` / `file_storage_uri` wymagany.
- `file_size_bytes` > 0 dla rekordow plikowych.
- `received_at` ustawiane przez backend.

## 6. Dlaczego to dziala dla roznych formatow
- `payload_json` obsluguje natywne JSON/API.
- `payload_text` obsluguje `xml/xhtml/html/txt/csv` po dekodowaniu.
- `file_storage_uri` obsluguje duze pliki (`pdf`, archiwa, binaria).
- `metadata_json` pozwala dorzucac pola specyficzne dla zrodla bez migracji.
- `raw_processing_runs` pozwala wielokrotnie przetwarzac ten sam rekord nowym parserem.

## 7. Co dalej (kolejny etap)
Dopiero po tej warstwie dodaj warstwe `CORE/FACTS` (encje, metryki, relacje, trendy). RAW zostaje niezmiennym zrodlem prawdy.
