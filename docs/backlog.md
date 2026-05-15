## Backlog

## [TASK-1] Prosta aplikacja z inputem nazwy firmy

**Cel biznesowy:**
Użytkownik może wpisać nazwę firmy, zapisać ją w aplikacji i zobaczyć wynik w tabeli na stronie.

**Zakres:**
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

**Minimalny zakres danych do odczytu:**
- `nazwa firmy`.

**Poza zakresem:**
- Upload plików.
- Parsowanie XHTML/PDF.
- Integracje z zewnętrznymi aplikacjami.
- Zaawansowana analityka finansowa.
- Edycja i usuwanie danych.

**Kryteria akceptacji (AC):**
- [x] Użytkownik widzi formularz z jednym polem nazwy firmy.
- [x] Użytkownik może wysłać poprawną nazwę firmy.
- [x] Backend waliduje wymagane pole oraz limit długości.
- [x] Dla poprawnych danych API zwraca status `201`.
- [x] Strona pokazuje zapisaną nazwę firmy w tabeli.
- [x] Dla pustej lub niepoprawnej wartości użytkownik widzi czytelny błąd.

**Definition of Done (DoD):**
- [x] Kod frontendu
- [x] Kod backendu
- [x] Endpoint API `POST /api/company`
- [x] Walidacja danych wejściowych
- [x] Obsługa błędów użytkownika
- [x] Testy jednostkowe walidacji
- [x] Aktualizacja dokumentacji
- [ ] Review/merge

**Status:** DONE

**Powiązane test case’y:**
`TC-FORM-COMPANY-001`, `TC-API-COMPANY-001`, `TC-VALIDATION-COMPANY-001`, `TC-FIN-TABLE-001`

## [TASK-2] PostgreSQL i połączenie aplikacji z bazą

**Cel biznesowy:**
Aplikacja zapisuje dane firmy do relacyjnej bazy PostgreSQL zamiast do pliku lokalnego.

**Zakres:**
- Postawienie bazy PostgreSQL lokalnie (`docker-compose`).
- Konfiguracja zmiennych środowiskowych: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`.
- Dodanie warstwy połączenia do bazy w backendzie.
- Inicjalizacja tabeli `companies` przy starcie aplikacji.
- Zapis nazwy firmy do tabeli `companies` z endpointu `POST /api/company`.
- Obsługa błędu połączenia/zapisu do bazy.

**Kryteria akceptacji (AC):**
- [x] PostgreSQL uruchamia się przez `docker compose`.
- [x] Backend łączy się z bazą przez zmienne `DB_*`.
- [x] Tabela `companies` jest tworzona automatycznie, jeśli nie istnieje.
- [x] Wysłanie formularza zapisuje rekord w PostgreSQL.
- [x] W przypadku błędu DB użytkownik otrzymuje czytelny komunikat.
- [x] Dodane są testy warstwy konfiguracji połączenia.

**Definition of Done (DoD):**
- [x] Konfiguracja PostgreSQL (`docker-compose`)
- [x] Kod backendu połączenia DB
- [x] Inicjalizacja tabeli `companies`
- [x] Integracja endpointu `POST /api/company` z bazą
- [x] Test konfiguracji połączenia DB
- [x] Aktualizacja dokumentacji
- [ ] Review/merge

**Status:** DONE

**Powiązane test case’y:**
`TC-DB-CONNECT-001`, `TC-DB-INSERT-COMPANY-001`, `TC-API-COMPANY-DB-001`, `TC-DB-ERROR-001`

## [TASK-3] Warstwa RAW danych z systemów zewnętrznych

**Cel biznesowy:**
Aplikacja posiada trwałą warstwę RAW do zapisu nieprzetworzonych danych z wielu źródeł.

**Zakres:**
- Rozszerzenie inicjalizacji bazy o schemat RAW.
- Utworzenie tabel: `source_apps`, `data_sources`, `ingestion_batches`, `raw_records`, `raw_record_files`, `raw_record_errors`, `raw_processing_runs`.
- Dodanie indeksów wspierających wyszukiwanie i skalę.
- Dodanie constraintu obecności payloadu.
- Zachowanie kompatybilności z tabelą `companies`.

**Kryteria akceptacji (AC):**
- [x] `init_db()` tworzy wszystkie tabele warstwy RAW.
- [x] Tworzone są kluczowe indeksy dla `raw_records`.
- [x] Constraint `chk_raw_payload_presence` jest obecny.
- [x] Funkcjonalność `companies` pozostaje bez regresji.
- [x] Udokumentowane test case’y dla warstwy RAW.

**Definition of Done (DoD):**
- [x] Kod backendu rozszerzony o DDL RAW
- [x] Inicjalizacja DB uruchamia DDL RAW
- [x] Aktualizacja dokumentacji schematu
- [x] Aktualizacja backlogu
- [x] Aktualizacja test case’ów
- [ ] Review/merge

**Status:** DONE (dev scope)

**Powiązane test case’y:**
`TC-DB-RAW-INIT-001`, `TC-DB-RAW-CONSTRAINT-001`, `TC-DB-RAW-INDEX-001`, `TC-DB-RAW-UNIQUE-CHECKSUM-001`, `TC-DB-RAW-COMPAT-001`

## [TASK-4] Wyszukiwanie i podgląd `raw_records` po NIP

**Cel biznesowy:**
Użytkownik może wpisać NIP i zobaczyć dane z `raw_records` powiązane z tym NIP.

**Zakres:**
- Endpoint `GET /api/raw-records?nip=...`.
- Walidacja NIP (normalizacja i 10 cyfr).
- Odczyt `raw_records` po `metadata_json->>'nip'` lub `external_id`.
- Renderowanie wszystkich pól rekordów RAW w tabeli frontendu.
- Obsługa błędów 400/500 i komunikatów.

**Kryteria akceptacji (AC):**
- [x] Dla poprawnego NIP API zwraca `200` i listę rekordów.
- [x] Dla niepoprawnego NIP API zwraca `400`.
- [x] Frontend wyświetla pola rekordów.
- [x] Dla braku danych frontend pokazuje czytelny komunikat.
- [x] Dodane testy jednostkowe i handlera HTTP.

**Definition of Done (DoD):**
- [x] Kod backendu endpointu GET
- [x] Walidacja NIP
- [x] Zapytanie DB po NIP
- [x] Kod frontendu
- [x] Testy backendowe
- [ ] Review/merge

**Status:** DONE (dev scope)

**Powiązane test case’y:**
`TC-API-RAW-BY-NIP-001`, `TC-API-RAW-BY-NIP-002`, `TC-UI-RAW-BY-NIP-001`, `TC-UI-RAW-BY-NIP-002`

## [TASK-5] Integracja external API metrics i zapis do warstwy RAW

**Cel biznesowy:**
Aplikacja pobiera metryki finansowe z `GET /api/v1/external/metrics` i zapisuje dane do tabel RAW.

**Zakres:**
- Klient external API i obsługa parametrów (`page`, `page_size`, `nip`, `year`).
- Obsługa statusów external API (`200`, `400`, `401`, `403`, `404`, `500`).
- Utrzymanie `source_apps`, `data_sources`.
- Tworzenie i finalizacja `ingestion_batches`.
- Zapis `items` do `raw_records`.
- Zapis błędów do `raw_record_errors`.
- Trigger importu: `POST /api/external/metrics/import`.
- Idempotencja i brak nadpisywania (`checksum` + `ON CONFLICT DO NOTHING`).

**Kryteria akceptacji (AC):**
- [x] Trigger importu wywołuje external API.
- [x] Dla `200` dane zapisują się do `raw_records`, batch ma `completed`.
- [x] Dla błędów batch ma `failed`, błąd zapisany w `raw_record_errors`.
- [x] Rekordy `source_apps` i `data_sources` są tworzone/uzupełniane automatycznie.
- [x] Import jest idempotentny i nie nadpisuje istniejących rekordów.
- [x] Dodane testy jednostkowe/integracyjne.

**Definition of Done (DoD):**
- [x] Klient HTTP external API
- [x] Endpoint triggera importu
- [x] Serwis zapisu do RAW
- [x] Logika checksum/idempotencji
- [x] Testy (unit + integration)
- [x] Aktualizacja dokumentacji
- [ ] Review/merge

**Status:** DONE (dev scope)

**Powiązane test case’y:**
`TC-EXT-METRICS-IMPORT-001`, `TC-EXT-METRICS-IMPORT-002`, `TC-EXT-METRICS-ERROR-001`, `TC-EXT-METRICS-IDEMPOTENCY-001`, `TC-EXT-METRICS-MAPPING-001`

## [TASK-6] Widok danych RAW po NIP z czytelnym stanem braku danych

**Cel biznesowy:**
Użytkownik po wpisaniu NIP widzi dane RAW albo jasny komunikat o braku danych.

**Zakres:**
- Ujednolicenie flow wyszukiwania po NIP w UI i API.
- Stan `success`: tabela z rekordami.
- Stan `empty`: komunikat `Brak danych RAW dla podanego NIP.`.
- Stan `validation_error`: komunikat walidacyjny.

**Kryteria akceptacji (AC):**
- [x] Dla poprawnego NIP i rekordów tabela jest wyświetlana.
- [x] Dla poprawnego NIP bez rekordów wyświetlany jest komunikat o braku danych.
- [x] Dla niepoprawnego NIP użytkownik otrzymuje komunikat walidacyjny.
- [x] UI nie pokazuje jednocześnie tabeli i komunikatu o braku danych.
- [x] Dodane testy API i UI dla scenariusza dane/brak danych.

**Definition of Done (DoD):**
- [x] Doprecyzowana obsługa stanów w frontendzie
- [x] Spójna odpowiedź API dla pustej listy
- [x] Testy backendowe (`GET /api/raw-records`)
- [x] Testy UI dla danych i pustego wyniku
- [x] Aktualizacja dokumentacji i backlogu
- [ ] Review/merge

**Status:** DONE (dev scope)

**Powiązane test case’y:**
`TC-API-RAW-BY-NIP-003`, `TC-UI-RAW-BY-NIP-003`, `TC-UI-RAW-BY-NIP-004`

# [TASK-7] Ręczne pobranie danych z API finansowego + status + podgląd RAW

**Cel biznesowy:**
Użytkownik po kliknięciu przycisku uruchamia import danych finansowych i widzi status operacji oraz dane RAW.

**Zakres:**
- Przycisk w UI do triggera `POST /api/external/metrics/import`.
- Obsługa stanów: `loading`, `success`, `error`.
- Prezentacja statusu i metryk (`batch_id`, `inserted`, `skipped_duplicates`, `errors`).
- Po sukcesie automatyczne odświeżenie tabeli `raw_records` dla NIP.

**Kryteria akceptacji (AC):**
- [x] Kliknięcie przycisku uruchamia import.
- [x] Użytkownik widzi status wykonania (`loading/success/error`).
- [x] Po sukcesie widoczna jest informacja o pobraniu danych i metryki importu.
- [x] Po sukcesie widoczne są aktualne dane RAW dla NIP.
- [x] Po błędzie widoczny jest czytelny komunikat.
- [x] Dodane testy API i UI dla sukcesu i błędu.

**Definition of Done (DoD):**
- [x] Przycisk importu w frontendzie
- [x] Integracja UI z `POST /api/external/metrics/import`
- [x] Sekcja statusu importu i metryk
- [x] Automatyczne odświeżenie tabeli RAW po sukcesie
- [x] Testy backendowe endpointu importu
- [x] Testy UI (`success/error/loading`)
- [x] Aktualizacja dokumentacji i backlogu
- [ ] Review/merge

**Status:** DONE (dev scope)

**Powiązane test case’y:**
`TC-UI-EXT-IMPORT-001`, `TC-UI-EXT-IMPORT-002`, `TC-API-EXT-IMPORT-003`, `TC-UI-EXT-IMPORT-RAW-001`
