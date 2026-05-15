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
