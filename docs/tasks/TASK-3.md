# TASK-3: Warstwa RAW dla danych z systemow zewnetrznych

## Cel
Dodanie warstwy RAW w PostgreSQL do trwalego zapisu nieprzetworzonych danych z wielu zrodel, z zachowaniem audytu i mozliwosci ponownego przetwarzania.

## Zakres
- Rozszerzenie `init_db()` o DDL warstwy RAW.
- Utworzenie tabel:
  - `source_apps`,
  - `data_sources`,
  - `ingestion_batches`,
  - `raw_records`,
  - `raw_record_files`,
  - `raw_record_errors`,
  - `raw_processing_runs`.
- Dodanie indeksow wydajnosciowych i unikalnosci deduplikacyjnej.
- Dodanie constraintu `chk_raw_payload_presence` w `raw_records`.
- Zachowanie kompatybilnosci ze sciezka `companies`.

## Kryteria akceptacji
- `init_db()` tworzy wszystkie tabele RAW, jesli nie istnieja.
- Tworzone sa indeksy krytyczne dla wyszukiwania i przetwarzania.
- Constraint payloadu uniemozliwia zapis pustego rekordu RAW bez tresci.
- Istniejace API `POST /api/company` i tabela `companies` dzialaja bez regresji.
- Dodane testy automatyczne dla konfiguracji schematu RAW.

## Dodane/zmienione pliki
- `backend/app/db.py`
- `backend/tests/test_db.py`
- `docs/dbstructure.md`
- `docs/backlog.md`
- `docs/test-cases.md`

## Powiazane test case'y
- `TC-DB-RAW-INIT-001`
- `TC-DB-RAW-CONSTRAINT-001`
- `TC-DB-RAW-INDEX-001`
- `TC-DB-RAW-UNIQUE-CHECKSUM-001`
- `TC-DB-RAW-COMPAT-001`

## Status
DONE (dev scope)
