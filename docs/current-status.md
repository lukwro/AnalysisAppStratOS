## Current Status (2026-05-15)

- TASK-1: DONE
- TASK-2: DONE
- TASK-3: DONE (dev scope)

### TASK-3 delivery
- Backend `init_db()` rozszerzony o pelny schemat RAW i indeksy.
- Dodane testy automatyczne schematu RAW w `backend/tests/test_db.py`.
- Dodany opis zadania w `docs/tasks/TASK-3.md`.
- Backlog i test case'y zaktualizowane.

### Open items
- Review/merge.
- Uruchomienie testow integracyjnych z realnym PostgreSQL dla scenariuszy:
  - `TC-DB-RAW-UNIQUE-CHECKSUM-001`
  - `TC-DB-RAW-COMPAT-001`
