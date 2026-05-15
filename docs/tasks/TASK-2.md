# TASK-2: PostgreSQL i polaczenie backendu z baza

## Cel
Postawienie lokalnej bazy PostgreSQL i podlaczenie aplikacji backendowej do zapisu danych.

## Zakres
- Konfiguracja PostgreSQL przez Docker Compose.
- Dodanie warstwy polaczenia w backendzie (`backend/app/db.py`).
- Automatyczna inicjalizacja tabeli `companies` przy starcie backendu.
- Zapis danych z endpointu `POST /api/company` do PostgreSQL.
- Konfiguracja przez zmienne srodowiskowe (`DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`).

## Kryteria akceptacji
- Baza PostgreSQL uruchamia sie lokalnie przez `docker compose up -d postgres`.
- Backend laczy sie z baza i tworzy tabele `companies`.
- Wyslanie nazwy firmy przez formularz zapisuje rekord w PostgreSQL.
- Bledy zapisu do bazy zwracaja czytelny komunikat API.
- Dodane testy warstwy konfiguracji DB.

## Dodane pliki
- `docker-compose.yml`
- `.env.example`
- `backend/app/db.py`
- `backend/tests/test_db.py`

## Notatka
W deploymentcie Railway nalezy podpiac Railway Postgres i ustawic zmienne `DB_*` zgodnie z danymi uslugi.
