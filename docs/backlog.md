[TASK-1] Prosta aplikacja z inputem nazwy firmy

Cel biznesowy:
Użytkownik może wpisać nazwę firmy, zapisać ją w aplikacji i zobaczyć wynik w tabeli na stronie.

Zakres:

- Przygotowanie prostej strony z jednym polem input: `nazwa firmy`.
- Dodanie przycisku zapisu danych.
- Walidacja podstawowa po stronie backendu:
  - pole wymagane,
  - usunięcie spacji z początku i końca,
  - maksymalna długość 200 znaków.
- Przekazanie danych z frontendu do backendu przez endpoint `POST /api/company`.
- Zwrócenie odpowiedzi API z zapisaną nazwą firmy.
- Wyświetlenie zapisanej nazwy firmy w tabeli na stronie.
- Wyświetlenie czytelnego komunikatu błędu w przypadku niepoprawnych danych.

Minimalny zakres danych do odczytu:

- nazwa firmy.

Poza zakresem:

- Upload plików.
- Parsowanie XHTML/PDF.
- Integracje z zewnętrznymi aplikacjami.
- Zaawansowana analityka finansowa.
- Edycja i usuwanie danych.

Kryteria akceptacji (AC):

- [x] Użytkownik widzi formularz z jednym polem nazwy firmy.
- [x] Użytkownik może wysłać poprawną nazwę firmy.
- [x] Backend waliduje wymagane pole oraz limit długości.
- [x] Dla poprawnych danych API zwraca status `201`.
- [x] Strona pokazuje zapisaną nazwę firmy w tabeli.
- [x] Dla pustej lub niepoprawnej wartości użytkownik widzi czytelny błąd.

Definition of Done (DoD):

- [x] Kod frontendu
- [x] Kod backendu
- [x] Endpoint API `POST /api/company`
- [x] Walidacja danych wejściowych
- [x] Obsługa błędów użytkownika
- [x] Testy jednostkowe walidacji
- [x] Aktualizacja dokumentacji
- [ ] Review/merge

Status: DONE

Powiązane test case’y:
TC-FORM-COMPANY-001, TC-API-COMPANY-001, TC-VALIDATION-COMPANY-001, TC-FIN-TABLE-001


[TASK-2] PostgreSQL i połączenie aplikacji z bazą

Cel biznesowy:
Aplikacja zapisuje dane firmy do relacyjnej bazy PostgreSQL zamiast do pliku lokalnego, aby zapewnić trwałość i gotowość do dalszej rozbudowy.

Zakres:

- Postawienie bazy PostgreSQL lokalnie (`docker-compose`).
- Konfiguracja zmiennych środowiskowych połączenia DB:
  - `DB_HOST`,
  - `DB_PORT`,
  - `DB_NAME`,
  - `DB_USER`,
  - `DB_PASSWORD`.
- Dodanie warstwy połączenia do bazy w backendzie.
- Inicjalizacja tabeli `companies` przy starcie aplikacji.
- Zapis nazwy firmy do tabeli `companies` z endpointu `POST /api/company`.
- Obsługa błędu połączenia/zapisu do bazy i zwrócenie czytelnego komunikatu API.
- Aktualizacja dokumentacji uruchomienia lokalnego i deployu Railway.

Minimalny zakres danych do odczytu:

- `id`,
- `name`,
- `created_at`.

Poza zakresem:

- Migracje wielu tabel biznesowych.
- Replikacja, backup i HA.
- Zaawansowany pooling połączeń.
- Integracja z zewnętrznym secret managerem.

Kryteria akceptacji (AC):

- [x] PostgreSQL uruchamia się przez `docker compose`.
- [x] Backend łączy się z bazą przez zmienne `DB_*`.
- [x] Tabela `companies` jest tworzona automatycznie, jeśli nie istnieje.
- [x] Wysłanie formularza zapisuje rekord w PostgreSQL.
- [x] W przypadku błędu DB użytkownik otrzymuje czytelny komunikat.
- [x] Dodane są testy warstwy konfiguracji połączenia.

Definition of Done (DoD):

- [x] Konfiguracja PostgreSQL (`docker-compose`)
- [x] Kod backendu połączenia DB
- [x] Inicjalizacja tabeli `companies`
- [x] Integracja endpointu `POST /api/company` z bazą
- [x] Test konfiguracji połączenia DB
- [x] Aktualizacja dokumentacji
- [ ] Review/merge

Status: DONE

Powiązane test case’y:
TC-DB-CONNECT-001, TC-DB-INSERT-COMPANY-001, TC-API-COMPANY-DB-001, TC-DB-ERROR-001


[TASK-3] Warstwa RAW danych z systemów zewnętrznych

Cel biznesowy:
Aplikacja posiada trwałą warstwę RAW do zapisu nieprzetworzonych danych z wielu źródeł, tak aby umożliwić audyt, deduplikację i wielokrotne przetwarzanie.

Zakres:

- Rozszerzenie inicjalizacji bazy o schemat RAW.
- Utworzenie tabel:
  - `source_apps`,
  - `data_sources`,
  - `ingestion_batches`,
  - `raw_records`,
  - `raw_record_files`,
  - `raw_record_errors`,
  - `raw_processing_runs`.
- Dodanie indeksów wspierających wyszukiwanie i skalę:
  - indeksy czasowe i statusowe dla `raw_records`,
  - indeks po `external_id`,
  - unikalny indeks checksum per source,
  - indeksy GIN dla `payload_json` i `metadata_json`.
- Dodanie constraintu walidującego obecność payloadu (`payload_text` lub `payload_json` lub `file_storage_uri`).
- Zachowanie kompatybilności z istniejącą tabelą `companies`.

Minimalny zakres danych do odczytu:

- Identyfikacja źródła (`source_app_id`, `data_source_id`),
- status ingestu/przetwarzania,
- dane payloadu (`payload_text`, `payload_json`, `file_storage_uri`),
- metadane i znaczniki czasu.

Poza zakresem:

- Endpointy API do zapisu/odczytu RAW.
- Proces ETL do warstwy CORE/FACTS.
- Walidacja semantyczna payloadów per źródło.

Kryteria akceptacji (AC):

- [x] `init_db()` tworzy wszystkie tabele warstwy RAW, jeśli nie istnieją.
- [x] Tworzone są kluczowe indeksy dla `raw_records`.
- [x] Constraint `chk_raw_payload_presence` jest obecny.
- [x] Dotychczasowa funkcjonalność `companies` pozostaje bez regresji na poziomie schematu.
- [x] Udokumentowane test case’y dla nowej warstwy RAW.

Definition of Done (DoD):

- [x] Kod backendu rozszerzony o DDL RAW
- [x] Inicjalizacja DB uruchamia DDL RAW
- [x] Aktualizacja dokumentacji schematu (`docs/dbstructure.md`)
- [x] Aktualizacja backlogu
- [x] Aktualizacja test case’ów
- [ ] Review/merge

Status: DONE (dev scope)

Powiązane test case’y:
TC-DB-RAW-INIT-001, TC-DB-RAW-CONSTRAINT-001, TC-DB-RAW-INDEX-001, TC-DB-RAW-UNIQUE-CHECKSUM-001, TC-DB-RAW-COMPAT-001


[TASK-4] Wyszukiwanie i podglad raw_records po NIP

Cel biznesowy:
Uzytkownik moze wpisac NIP w interfejsie i zobaczyc wszystkie dane z tabeli `raw_records` powiazane z tym NIP.

Zakres:

- Dodanie endpointu `GET /api/raw-records?nip=...`.
- Walidacja NIP (normalizacja i 10 cyfr).
- Odczyt `raw_records` z DB po NIP:
  - `metadata_json->>'nip'`,
  - `external_id`.
- Renderowanie wszystkich pol rekordow RAW w tabeli frontendu.
- Obsluga bledow 400/500 i komunikatow dla uzytkownika.

Kryteria akceptacji (AC):

- [x] Dla poprawnego NIP API zwraca `200` i liste rekordow.
- [x] Dla niepoprawnego NIP API zwraca `400`.
- [x] Frontend pobiera dane po NIP i wyswietla wszystkie pola rekordow.
- [x] Dla braku danych frontend pokazuje czytelny komunikat.
- [x] Dodane testy jednostkowe i handlera HTTP dla nowego flow.

Definition of Done (DoD):

- [x] Kod backendu endpointu GET
- [x] Walidacja NIP
- [x] Zapytanie DB po NIP
- [x] Kod frontendu do wyswietlania `raw_records`
- [x] Testy backendowe
- [ ] Review/merge

Status: DONE (dev scope)

Powiązane test case’y:
TC-API-RAW-BY-NIP-001, TC-API-RAW-BY-NIP-002, TC-UI-RAW-BY-NIP-001, TC-UI-RAW-BY-NIP-002


[TASK-5] Integracja external API metrics i zapis do warstwy RAW

Cel biznesowy:
Aplikacja pobiera metryki finansowe z zewnętrznego endpointu `GET /api/v1/external/metrics` i zapisuje surowe dane oraz metadane ingestu do tabel RAW, tak aby zapewnić audyt i dalsze przetwarzanie.

Zakres:

- Dodanie klienta external API dla endpointu `GET /api/v1/external/metrics`.
- Obsługa query params:
  - `page` (domyslnie `1`),
  - `page_size` (domyslnie `20`, max `100`),
  - `nip` (opcjonalnie, tylko cyfry),
  - `year` (opcjonalnie, np. `2024`).
- Obsługa statusów external API:
  - `200` -> zapis danych,
  - `400/401/403/404/500` -> zapis błędu ingestu + czytelny status API po naszej stronie.
- Upsert/utrzymanie rekordów referencyjnych:
  - `source_apps` (np. `external_finance_api`),
  - `data_sources` (np. `external_metrics_v1`).
- Tworzenie `ingestion_batches` dla każdego pobrania (status lifecycle: `received` -> `processing` -> `completed`/`failed`).
- Zapis payloadu z `items` do `raw_records`:
  - `record_type`: `financial_metric`,
  - `content_type`: `application/json`,
  - `content_format`: `json`,
  - `payload_json`: pojedynczy item lub strona odpowiedzi (decyzja implementacyjna opisana w tasku technicznym),
  - `metadata_json`: `nip`, `year`, `page`, `page_size`, `total`, `metric_group`, `metric_name`, `unit`, `status`.
- Dedup i idempotencja:
  - wyliczanie `checksum_sha256` dla zapisywanego payloadu,
  - unikanie duplikatów dla tego samego `source_app_id` + checksum,
  - brak nadpisywania istniejacych rekordow RAW (insert-only; konflikt -> `ON CONFLICT DO NOTHING`).
- Zapis błędów do `raw_record_errors` (stage: `fetch`/`store`) z `error_code` i `error_details_json`.
- Dodanie endpointu w naszej aplikacji do ręcznego triggera importu, np. `POST /api/external/metrics/import`.

Minimalny zakres danych do odczytu:

- z external API: `items[]`, `page`, `page_size`, `total`,
- z item: `metric_group`, `metric_name`, `value`, `rounded_value`, `unit`, `status`, `year`.

Poza zakresem:

- Warstwa CORE/FACTS i agregacje biznesowe.
- Scheduler produkcyjny (cron) poza ręcznym triggerem.
- UI analityczne metryk (poza debug/listing RAW).

Kryteria akceptacji (AC):

- [x] Trigger importu wywołuje external API z poprawnymi parametrami.
- [x] Dla `200` dane są zapisywane do `raw_records` oraz batch ma status `completed`.
- [x] Dla `400/401/403/404/500` batch ma status `failed`, a błąd jest zapisany w `raw_record_errors`.
- [x] Rekordy `source_apps` i `data_sources` są tworzone/uzupełniane automatycznie.
- [x] Import jest idempotentny dla tego samego payloadu (dedup po checksum).
- [x] Ponowne wywolanie tego samego zapytania z tym samym payloadem nie nadpisuje istniejących rekordów.
- [x] Dodane testy jednostkowe i integracyjne dla mappingu i obsługi statusów.

Definition of Done (DoD):

- [x] Klient HTTP external API
- [x] Endpoint triggera importu w backendzie
- [x] Serwis zapisu do RAW (`source_apps`, `data_sources`, `ingestion_batches`, `raw_records`, `raw_record_errors`)
- [x] Logika checksum/idempotencji
- [x] Testy (unit + integration)
- [x] Aktualizacja dokumentacji API i uruchomienia
- [ ] Review/merge

Status: DONE (dev scope)

Powiązane test case’y:
TC-EXT-METRICS-IMPORT-001, TC-EXT-METRICS-IMPORT-002, TC-EXT-METRICS-ERROR-001, TC-EXT-METRICS-IDEMPOTENCY-001, TC-EXT-METRICS-MAPPING-001


[TASK-6] Widok danych RAW po NIP z czytelnym stanem braku danych

Cel biznesowy:
Uzytkownik wpisuje NIP i otrzymuje czytelny wynik: tabela `raw_records` gdy dane istnieja albo jasny komunikat, ze danych brak.

Zakres:

- Ujednolicenie flow wyszukiwania po NIP w UI i API.
- Dla poprawnego NIP i danych:
  - wyswietlenie tabeli z rekordami `raw_records`,
  - prezentacja wszystkich istotnych pol rekordu.
- Dla poprawnego NIP i braku danych:
  - brak renderu tabeli wynikowej,
  - widoczny komunikat: `Brak danych RAW dla podanego NIP.`.
- Dla niepoprawnego NIP:
  - czytelny komunikat walidacyjny,
  - brak zapytania do backendu (walidacja frontend) lub odpowiedz `400` (backend).
- Zachowanie zgodnosci z endpointem `GET /api/raw-records?nip=...`.

Minimalny zakres danych do odczytu:

- `id`,
- `external_id`,
- `record_type`,
- `received_at`,
- `metadata_json`.

Poza zakresem:

- Paginacja tabeli wynikowej.
- Sortowanie i filtrowanie po kolumnach.
- Edycja/usuwanie rekordow RAW.

Kryteria akceptacji (AC):

- [x] Dla poprawnego NIP i istniejacych rekordow tabela jest wyswietlana.
- [x] Dla poprawnego NIP bez rekordow wyswietlany jest komunikat `Brak danych RAW dla podanego NIP.`.
- [x] Dla niepoprawnego NIP uzytkownik otrzymuje komunikat walidacyjny.
- [x] UI nie pokazuje jednoczesnie tabeli i komunikatu o braku danych.
- [x] Dodane testy API i UI dla scenariusza dane/brak danych.

Definition of Done (DoD):

- [x] Doprecyzowana obsluga stanów (`success`, `empty`, `validation_error`) w frontendzie
- [x] Spójna odpowiedz API dla pustej listy rekordow
- [x] Testy backendowe (`GET /api/raw-records`)
- [x] Testy UI dla widoku danych i pustego wyniku
- [x] Aktualizacja dokumentacji i backlogu
- [ ] Review/merge

Status: DONE (dev scope)

Powiązane test case’y:
TC-API-RAW-BY-NIP-003, TC-UI-RAW-BY-NIP-003, TC-UI-RAW-BY-NIP-004


---
## Szczegółowe specyfikacje tasków (przeniesione z docs/tasks)


### TASK-1

# TASK-1: Podstawowa aplikacja i pole nazwy firmy

## Cel
Stworzenie minimalnej aplikacji jako fundament pod kolejne zadania (upload i parser).

## Zakres
- Frontend z jednym polem `nazwa firmy` i przyciskiem zapisu.
- Backend API `POST /api/company`.
- Walidacja nazwy firmy (wymagane, trim, max 200 znakow).
- Zapis danych do prostego storage JSON.
- Prezentacja zapisanej nazwy firmy w tabeli na stronie.
- Komunikat bledu dla niepoprawnych danych.

## Kryteria akceptacji
- Uzytkownik wpisuje nazwe firmy i wysyla formularz.
- Backend zwraca `201` dla poprawnej nazwy.
- Dane sa zapisane w pliku `backend/data/company.json`.
- Frontend pokazuje wynik w tabeli.
- Dla pustej nazwy uzytkownik widzi czytelny blad.

## Testy
- `backend/tests/test_company.py`:
  - walidacja poprawnej nazwy,
  - odrzucenie pustej nazwy,
  - odrzucenie za dlugiej nazwy,
  - zapis rekordu do pliku.
- `backend/tests/test_http_response.py`:
  - poprawny format odpowiedzi JSON i naglowkow.

### TASK-2

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

### TASK-3

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

### TASK-4

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

### TASK-5

# TASK-5: Integracja external metrics API -> warstwa RAW

## Cel
Zintegrowac aplikacje z endpointem `GET /api/v1/external/metrics` i zapisywac odpowiedzi do tabel warstwy RAW wraz z pelnym audytem ingestu.

## Wejscie API zewnetrznego
- Endpoint: `GET /api/v1/external/metrics`
- Query params:
  - `page` (int, default `1`)
  - `page_size` (int, default `20`, max `100`)
  - `nip` (string, opcjonalnie, tylko cyfry)
  - `year` (int, opcjonalnie)
- Statusy:
  - `200`, `400`, `401`, `403`, `404`, `500`

## Mapowanie do warstwy RAW

### 1) source_apps
- `code`: `external_finance_api`
- `name`: `External Finance API`
- `app_type`: `external`
- `status`: `active`

### 2) data_sources
- `code`: `external_metrics_v1`
- `name`: `External Metrics API v1`
- `source_type`: `api`
- `provider`: nazwa dostawcy
- `base_url`: bazowy URL API
- `auth_type`: `api_key`

### 3) ingestion_batches
- Tworzony per request importu
- `trigger_type`: `manual` (na start)
- `status`: `received` -> `processing` -> `completed`/`failed`
- `record_count`: liczba zapisanych rekordow `raw_records`
- `error_count`: liczba bledow
- `metadata_json`: `page`, `page_size`, `nip`, `year`, `total`

### 4) raw_records
- Jeden rekord per element `items[]`
- `source_app_id`, `data_source_id`, `ingestion_batch_id`
- `external_id`: deterministyczny klucz np. `nip:year:metric_group:metric_name:page`
- `record_type`: `financial_metric`
- `content_type`: `application/json`
- `content_format`: `json`
- `payload_json`: obiekt pojedynczej metryki (item)
- `metadata_json`: pola requestu i paginacji + metadane itemu
- `checksum_sha256`: hash z kanonicznego JSON itemu
- `collected_at`: czas odpowiedzi z API (jezeli dostepny), w innym przypadku czas importu

## Zasada idempotencji i braku nadpisan
- Warstwa RAW dziala w trybie `append/insert-only`.
- Dla rekordu z tym samym `source_app_id` + `checksum_sha256`:
  - NIE wykonujemy `UPDATE`,
  - NIE nadpisujemy `payload_json` ani `metadata_json`,
  - rekord jest pomijany (`ON CONFLICT DO NOTHING`).
- W `ingestion_batches` zapisujemy metryki:
  - `record_count`: liczba nowo dodanych rekordow,
  - `metadata_json.skipped_duplicates`: liczba pominietych duplikatow.

### 5) raw_record_errors
- Dla statusow `400/401/403/404/500` i bledow zapisu
- `stage`: `fetch` lub `store`
- `error_code`: np. `EXT_API_401`, `EXT_API_500`, `DB_WRITE_FAILED`
- `error_message`: skrot problemu
- `error_details_json`: status HTTP, params, response body (zanonimizowany)

## Kryteria akceptacji
- Trigger importu dostepny w backendzie (np. `POST /api/external/metrics/import`).
- Poprawna obsluga paginacji i filtrow (`nip`, `year`).
- Zapis slownikow zrodel (`source_apps`, `data_sources`) jest automatyczny.
- Dla `200` rekordy sa zapisywane do `raw_records`.
- Dla bledow API i DB zapis do `raw_record_errors` + `ingestion_batches.status='failed'`.
- Idempotencja: brak duplikatow dla tego samego payloadu (checksum).
- Brak nadpisan: ponowny import tego samego payloadu nie zmienia istniejacych rekordow.

## Testy do realizacji
- `TC-EXT-METRICS-IMPORT-001`: status 200 i zapis rekordow RAW.
- `TC-EXT-METRICS-IMPORT-002`: poprawny zapis batch metadata i licznikow.
- `TC-EXT-METRICS-ERROR-001`: statusy 4xx/5xx tworza blad ingestu i failed batch.
- `TC-EXT-METRICS-IDEMPOTENCY-001`: ponowny import tego samego payloadu nie duplikuje danych.
- `TC-EXT-METRICS-IDEMPOTENCY-001`: ponowny import tego samego payloadu nie duplikuje ani nie nadpisuje danych.
- `TC-EXT-METRICS-MAPPING-001`: mapowanie pol item -> raw_records/payload_json/metadata_json.

## Status
READY FOR REVIEW (scope definition)
