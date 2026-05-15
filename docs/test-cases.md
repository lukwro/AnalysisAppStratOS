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


[TC-API-RAW-BY-NIP-001] API zwraca rekordy RAW dla poprawnego NIP
Cel:
Weryfikacja endpointu `GET /api/raw-records` dla poprawnego NIP.

Warunki wstępne:
Backend uruchomiony.
W `raw_records` istnieją rekordy powiazane z NIP.

Kroki:
1. Wyślij `GET /api/raw-records?nip=123-456-32-18`.

Oczekiwany rezultat:
Status HTTP: `200`.
Body zawiera `nip` po normalizacji (`1234563218`) oraz tablicę `records`.

Status: TODO


[TC-API-RAW-BY-NIP-002] API odrzuca niepoprawny NIP
Cel:
Weryfikacja walidacji parametru `nip`.

Warunki wstępne:
Backend uruchomiony.

Kroki:
1. Wyślij `GET /api/raw-records?nip=123`.

Oczekiwany rezultat:
Status HTTP: `400`.
Komunikat: `NIP musi miec dokladnie 10 cyfr.`.

Status: TODO


[TC-UI-RAW-BY-NIP-001] Frontend renderuje wszystkie pola raw_records
Cel:
Weryfikacja prezentacji danych RAW po wyszukaniu po NIP.

Warunki wstępne:
Frontend i backend uruchomione.
API zwraca rekordy dla testowego NIP.

Kroki:
1. Wpisz poprawny NIP.
2. Kliknij `Pobierz raw_records`.

Oczekiwany rezultat:
Widoczna jest tabela z kolumnami odpowiadajacymi polom rekordow.
Widoczne sa wszystkie zwrocone rekordy.

Status: TODO


[TC-UI-RAW-BY-NIP-002] Frontend pokazuje komunikat przy braku danych
Cel:
Weryfikacja obslugi pustego wyniku wyszukiwania.

Warunki wstępne:
Frontend i backend uruchomione.
Brak rekordow dla podanego NIP.

Kroki:
1. Wpisz poprawny NIP bez danych w `raw_records`.
2. Kliknij `Pobierz raw_records`.

Oczekiwany rezultat:
Tabela wynikow nie jest wyswietlana.
Uzytkownik widzi komunikat: `Brak rekordow raw_records dla podanego NIP.`.

Status: TODO


[TC-EXT-METRICS-IMPORT-001] Import metryk external API zapisuje raw_records
Cel:
Weryfikacja podstawowego scenariusza importu danych metryk finansowych.

Warunki wstępne:
Backend uruchomiony.
Skonfigurowany klucz API do external service.
External API zwraca status `200` i `items`.

Kroki:
1. Wywołaj endpoint triggera importu z parametrami `page`, `page_size`, opcjonalnie `nip`, `year`.
2. Sprawdź rekordy zapisane w `raw_records`.

Oczekiwany rezultat:
Import kończy się sukcesem.
Każdy element `items[]` jest zapisany jako rekord `raw_records` z `record_type=financial_metric`.

Status: TODO


[TC-EXT-METRICS-IMPORT-002] Poprawny zapis ingestion_batches
Cel:
Weryfikacja pełnego audytu ingestu.

Warunki wstępne:
Import external metrics uruchomiony.

Kroki:
1. Uruchom import metryk.
2. Odczytaj wpis w `ingestion_batches`.

Oczekiwany rezultat:
Batch posiada `status=completed` dla sukcesu.
`record_count` odpowiada liczbie zapisanych `raw_records`.
`metadata_json` zawiera `page`, `page_size`, `nip`, `year`, `total`.

Status: TODO


[TC-EXT-METRICS-ERROR-001] Obsługa błędów external API
Cel:
Weryfikacja obsługi statusów `400/401/403/404/500`.

Warunki wstępne:
Możliwość zasymulowania odpowiedzi błędnej external API.

Kroki:
1. Wywołaj import i wymuś odpowiedź błędną API (np. `401`).
2. Sprawdź `ingestion_batches` i `raw_record_errors`.

Oczekiwany rezultat:
Batch ma `status=failed`.
W `raw_record_errors` zapisany jest wpis z `stage=fetch` i odpowiednim `error_code`.

Status: TODO


[TC-EXT-METRICS-IDEMPOTENCY-001] Idempotencja importu po checksum
Cel:
Weryfikacja, że ponowne pobranie tego samego payloadu nie dubluje danych.

Warunki wstępne:
Dostępny ten sam payload z external API w dwóch kolejnych importach.

Kroki:
1. Uruchom import pierwszy raz.
2. Uruchom import drugi raz z tymi samymi parametrami i odpowiedzią.
3. Porównaj liczbę rekordów i checksumy.

Oczekiwany rezultat:
Brak duplikatów dla tego samego `source_app_id` + `checksum_sha256`.

Status: TODO


[TC-EXT-METRICS-MAPPING-001] Poprawne mapowanie pól metryk do RAW
Cel:
Weryfikacja mapowania danych z external API na strukturę RAW.

Warunki wstępne:
Import z odpowiedzią `200` zawierającą przykładowe `items`.

Kroki:
1. Wykonaj import.
2. Sprawdź `payload_json` i `metadata_json` zapisanych rekordów.

Oczekiwany rezultat:
`payload_json` zawiera dane metryki (`metric_group`, `metric_name`, `value`, `rounded_value`, `unit`, `status`, `year`).
`metadata_json` zawiera kontekst requestu (`nip`, `page`, `page_size`, `total`).

Status: TODO


[TC-API-RAW-BY-NIP-003] API zwraca pustą listę dla poprawnego NIP bez danych
Cel:
Weryfikacja pustego wyniku wyszukiwania po poprawnym NIP.

Warunki wstępne:
Backend uruchomiony.
Brak rekordów `raw_records` dla wskazanego NIP.

Kroki:
1. Wyślij `GET /api/raw-records?nip=9999999999`.

Oczekiwany rezultat:
Status HTTP: `200`.
Body zawiera poprawny `nip` i `records: []`.

Status: TODO


[TC-UI-RAW-BY-NIP-003] UI pokazuje tabelę dla NIP z danymi
Cel:
Weryfikacja stanu sukcesu wyszukiwania po NIP.

Warunki wstępne:
Frontend i backend uruchomione.
API zwraca co najmniej 1 rekord dla testowego NIP.

Kroki:
1. Wpisz poprawny NIP z istniejącymi danymi.
2. Kliknij `Pobierz raw_records`.

Oczekiwany rezultat:
Tabela wynikowa jest widoczna.
Komunikat o braku danych nie jest widoczny.

Status: TODO


[TC-UI-RAW-BY-NIP-004] UI pokazuje komunikat o braku danych dla poprawnego NIP
Cel:
Weryfikacja stanu pustego wyniku wyszukiwania.

Warunki wstępne:
Frontend i backend uruchomione.
API zwraca pustą listę `records` dla wskazanego NIP.

Kroki:
1. Wpisz poprawny NIP bez danych.
2. Kliknij `Pobierz raw_records`.

Oczekiwany rezultat:
Widoczny komunikat: `Brak danych RAW dla podanego NIP.`.
Tabela wynikowa nie jest widoczna.

Status: TODO
