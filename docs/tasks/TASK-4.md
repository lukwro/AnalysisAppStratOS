# TASK-4: Podglad danych RAW po NIP

## Cel
Umozliwic uzytkownikowi wpisanie NIP i wyswietlenie wszystkich danych z tabeli `raw_records` powiazanych z tym NIP.

## Zakres
- Dodanie endpointu `GET /api/raw-records?nip=...`.
- Walidacja parametru `nip` (10 cyfr po normalizacji).
- Pobranie rekordow z `raw_records` po NIP (na podstawie `metadata_json->>'nip'` lub `external_id`).
- Prezentacja wszystkich pol zwroconych rekordow w tabeli frontendu.
- Obsluga bledow walidacji i bledow odczytu z bazy.

## Kryteria akceptacji
- Dla poprawnego NIP API zwraca `200` i tablice `records`.
- Dla niepoprawnego NIP API zwraca `400` i czytelny komunikat.
- Frontend wysyla zapytanie po NIP i renderuje wszystkie kolumny zwroconych rekordow.
- Dla braku rekordow frontend pokazuje czytelny komunikat.

## Testy
- `backend/tests/test_nip.py`
- `backend/tests/test_http_response.py` (GET `/api/raw-records`)
- `backend/tests/test_db.py` (`fetch_raw_records_by_nip`)

## Status
DONE (dev scope)
