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
