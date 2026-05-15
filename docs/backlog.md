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
