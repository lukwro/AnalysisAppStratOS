# AnalysisAppStratOS

Minimalna aplikacja pod kolejne taski: formularz nazwy firmy + API zapisu.

## Lokalnie

1. Zainstaluj zaleznosci:
`pip install -r requirements.txt`
2. Uruchom backend (serwuje tez frontend):
`python -m backend.app.main`
3. Otworz:
`http://127.0.0.1:8000`

## Deploy na Railway

1. Wrzuc repo na GitHub.
2. W Railway wybierz `New Project` -> `Deploy from GitHub repo`.
3. Railway wykryje `railway.toml` i uruchomi komenda:
`python -m backend.app.main`
4. Aplikacja nasluchuje na porcie z `PORT` (ustawiany automatycznie przez Railway).
5. Po deployu otworz wygenerowany URL Railway.

## Struktura deploy

- `railway.toml` - konfiguracja build/deploy
- `Procfile` - fallback komendy startowej
- `requirements.txt` - zaleznosci Pythona
