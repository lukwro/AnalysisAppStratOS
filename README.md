# AnalysisAppStratOS

Minimalna aplikacja: formularz nazwy firmy + API zapisu do PostgreSQL.

## Wymagania
- Docker + Docker Compose
- Python 3.11+

## Lokalnie

1. Uruchom PostgreSQL:
`docker compose up -d postgres`

2. Zainstaluj zaleznosci:
`pip install -r requirements.txt`

3. Ustaw zmienne srodowiskowe (PowerShell):
`$env:DB_HOST='127.0.0.1'`
`$env:DB_PORT='5432'`
`$env:DB_NAME='analysis_app'`
`$env:DB_USER='analysis_user'`
`$env:DB_PASSWORD='analysis_pass'`

4. Uruchom backend (serwuje tez frontend):
`python -m backend.app.main`

5. Otworz:
`http://127.0.0.1:8000`

## Testy
`python -m pytest -q`

## Deploy na Railway

1. Wrzuc repo na GitHub.
2. W Railway wybierz `New Project` -> `Deploy from GitHub repo`.
3. Dodaj Postgres plugin w Railway.
4. Polacz backend z usluga Postgres (Reference/Variables). Najprosciej ustawic `DATABASE_URL` z Railway Postgres.
5. Alternatywnie aplikacja obsluzy tez `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`.
6. Railway uruchomi aplikacje komenda:
`python -m backend.app.main`

## Pliki deploy
- `railway.toml`
- `Procfile`
- `requirements.txt`
