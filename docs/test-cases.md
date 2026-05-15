[TC-FORM-COMPANY-001] Formularz przyjmuje nazwę firmy
Cel:
Weryfikacja, że użytkownik może wpisać nazwę firmy i wysłać formularz.

Warunki wstępne:
Aplikacja uruchomiona.
Strona główna dostępna.

Kroki:
1. Wejdź na stronę aplikacji.
2. Wpisz w polu "Nazwa firmy" wartość: "Firma Testowa SA".
3. Kliknij "Zapisz".

Oczekiwany rezultat:
Żądanie jest wysłane do backendu.
Tabela wyników jest widoczna.
W tabeli widoczna jest nazwa "Firma Testowa SA".

Status: PASS


[TC-API-COMPANY-001] API zwraca 201 dla poprawnych danych
Cel:
Weryfikacja poprawnej odpowiedzi endpointu POST /api/company.

Warunki wstępne:
Backend uruchomiony.

Kroki:
1. Wyślij POST /api/company z body: {"name":"Firma Testowa SA"}.

Oczekiwany rezultat:
Status HTTP: 201.
JSON odpowiedzi zawiera pole "name" z wartością "Firma Testowa SA".

Status: PASS


[TC-VALIDATION-COMPANY-001] Walidacja odrzuca pustą nazwę
Cel:
Weryfikacja walidacji pola wymagane.

Warunki wstępne:
Backend uruchomiony.

Kroki:
1. Wyślij POST /api/company z body: {"name":"   "}.

Oczekiwany rezultat:
Status HTTP: 400.
Komunikat błędu: "Pole 'nazwa firmy' jest wymagane.".

Status: PASS


[TC-FIN-TABLE-001] Prezentacja danych w tabeli
Cel:
Weryfikacja prezentacji danych zwróconych przez API.

Warunki wstępne:
Frontend i backend uruchomione.

Kroki:
1. Wprowadź poprawną nazwę firmy.
2. Wyślij formularz.

Oczekiwany rezultat:
Tabela wynikowa jest odświeżona.
Wiersz tabeli zawiera nazwę firmy zwróconą przez API.

Status: PASS


[TC-DB-CONNECT-001] Backend łączy się z PostgreSQL
Cel:
Weryfikacja połączenia backendu z bazą danych przez DB_*.

Warunki wstępne:
PostgreSQL uruchomiony przez docker compose.
Zmienne DB_* ustawione poprawnie.

Kroki:
1. Uruchom backend.

Oczekiwany rezultat:
Backend startuje bez błędu połączenia.
Tabela companies zostaje utworzona automatycznie (jeśli nie istniała).

Status: PASS


[TC-DB-INSERT-COMPANY-001] Zapis rekordu firmy do tabeli companies
Cel:
Weryfikacja zapisu danych do PostgreSQL.

Warunki wstępne:
Backend połączony z PostgreSQL.

Kroki:
1. Wyślij POST /api/company z poprawną nazwą firmy.
2. Odczytaj dane z tabeli companies.

Oczekiwany rezultat:
W tabeli companies istnieje nowy rekord z nazwą firmy.
Pole created_at jest ustawione.

Status: PASS


[TC-API-COMPANY-DB-001] API zapisuje do DB i zwraca dane
Cel:
Weryfikacja pełnego przepływu API + DB.

Warunki wstępne:
Frontend, backend i PostgreSQL uruchomione.

Kroki:
1. Wpisz nazwę firmy w formularzu.
2. Kliknij "Zapisz".

Oczekiwany rezultat:
API zwraca 201.
Dane są zapisane do DB.
Frontend pokazuje zapisany rekord.

Status: PASS


[TC-DB-ERROR-001] Czytelny błąd przy niedostępnej bazie
Cel:
Weryfikacja obsługi błędu zapisu do DB.

Warunki wstępne:
Backend uruchomiony.
Baza PostgreSQL niedostępna lub błędna konfiguracja DB_*.

Kroki:
1. Wyślij POST /api/company z poprawną nazwą firmy.

Oczekiwany rezultat:
Status HTTP: 500.
Komunikat API: "Blad zapisu do bazy danych.".
Frontend pokazuje czytelny komunikat błędu.

Status: PASS


[TC-DB-RAW-INIT-001] Inicjalizacja tworzy tabele warstwy RAW
Cel:
Weryfikacja, że `init_db()` tworzy wszystkie tabele RAW.

Warunki wstępne:
PostgreSQL uruchomiony.
Backend ma dostęp do DB.

Kroki:
1. Uruchom backend (wywołanie `init_db()`).
2. Sprawdź obecność tabel: `source_apps`, `data_sources`, `ingestion_batches`, `raw_records`, `raw_record_files`, `raw_record_errors`, `raw_processing_runs`.

Oczekiwany rezultat:
Wszystkie wskazane tabele istnieją w bazie.

Status: TODO


[TC-DB-RAW-CONSTRAINT-001] Constraint payloadu w raw_records
Cel:
Weryfikacja działania constraintu `chk_raw_payload_presence`.

Warunki wstępne:
Tabela `raw_records` istnieje.
Istnieje poprawny rekord w `source_apps`.

Kroki:
1. Spróbuj wstawić rekord do `raw_records` bez `payload_text`, `payload_json` i `file_storage_uri`.
2. Spróbuj wstawić rekord z przynajmniej jednym polem payloadu.

Oczekiwany rezultat:
Pierwszy insert kończy się błędem constraintu.
Drugi insert kończy się powodzeniem.

Status: TODO


[TC-DB-RAW-INDEX-001] Krytyczne indeksy raw_records istnieją
Cel:
Weryfikacja utworzenia indeksów wydajnościowych.

Warunki wstępne:
`init_db()` wykonane.

Kroki:
1. Odczytaj metadane indeksów dla tabeli `raw_records`.
2. Zweryfikuj obecność:
   - `idx_raw_records_source_time`,
   - `idx_raw_records_type_time`,
   - `idx_raw_records_processing_status`,
   - `idx_raw_records_external`,
   - `idx_raw_records_payload_json_gin`,
   - `idx_raw_records_metadata_json_gin`.

Oczekiwany rezultat:
Wszystkie indeksy istnieją z oczekiwanymi nazwami.

Status: TODO


[TC-DB-RAW-UNIQUE-CHECKSUM-001] Unikalność checksum per source
Cel:
Weryfikacja unikalnego indeksu `uq_raw_records_checksum_source`.

Warunki wstępne:
Istnieje `source_app_id`.
Tabela `raw_records` istnieje.

Kroki:
1. Wstaw rekord `raw_records` z `source_app_id=A` i `checksum_sha256=X`.
2. Spróbuj wstawić drugi rekord z `source_app_id=A` i `checksum_sha256=X`.
3. Wstaw rekord z innym `source_app_id=B` i `checksum_sha256=X`.

Oczekiwany rezultat:
Krok 2 kończy się błędem unikalności.
Krok 3 kończy się powodzeniem.

Status: TODO


[TC-DB-RAW-COMPAT-001] Kompatybilność z istniejącą tabelą companies
Cel:
Weryfikacja braku regresji po dodaniu schematu RAW.

Warunki wstępne:
Backend uruchomiony z nowym `init_db()`.

Kroki:
1. Wyślij `POST /api/company` z poprawną nazwą firmy.
2. Odczytaj rekord z tabeli `companies`.

Oczekiwany rezultat:
API zwraca `201`.
Rekord jest poprawnie zapisany w `companies`.

Status: TODO
