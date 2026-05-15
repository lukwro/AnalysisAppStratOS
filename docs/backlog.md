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
