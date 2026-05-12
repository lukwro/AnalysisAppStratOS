1. Główna zasada modelu

Podziel bazę na 4 warstwy:

1. Sources            — skąd przyszły dane
2. Raw data           — dane surowe, oryginalne
3. Core entities      — wspólne obiekty biznesowe
4. Processed data     — dane uporządkowane: metryki, ceny, trendy, sygnały

Czyli przepływ:

Źródło → Raw record → Przetwarzanie → Metryka / Cena / Trend / Sygnał
2. Minimalny schemat bazy

Na start widziałbym takie tabele:

source_apps
data_sources
raw_records

entities
entity_aliases
entity_relations

metrics
commodity_prices
financial_statements
trends
signals

processing_jobs
processing_errors

To jest rozsądny fundament.

3. Źródła danych
source_apps

To aplikacje/moduły, które wysyłają dane.

source_apps
-----------
id
name
type
description
status
api_key_hash
last_seen_at
created_at
updated_at

Przykłady:

Financial Analysis App
Commodity Prices Importer
Trend Scanner
Competitive Analysis App
Manual Upload
data_sources

To konkretne źródła danych, np. strona, API, raport, plik.

data_sources
------------
id
source_app_id
name
source_type
url
provider
trust_level
refresh_frequency
metadata_json
created_at
updated_at

Przykład:

name: London Metal Exchange
source_type: api
provider: LME
trust_level: high

Albo:

name: Annual Report PDF
source_type: document
provider: Company X
trust_level: high
4. Dane surowe
raw_records

To magazyn wszystkiego, co przyszło, bez wciskania na siłę w docelowy model.

raw_records
-----------
id
source_app_id
data_source_id
external_id
record_type
title
raw_content
raw_payload_json
content_type
language
source_url
file_path
checksum
collected_at
received_at
status
processing_status
metadata_json
created_at
updated_at

Przykładowe record_type:

financial_report
commodity_price_api_response
trend_article
market_news
csv_upload
pdf_document
manual_note

Najważniejsze: raw_records zostają jako audytowalny oryginał. Nie kasujesz ich po przetworzeniu.

5. Wspólne encje biznesowe

To jest serce systemu, bo różne dane muszą się do czegoś odnosić.

entities
entities
--------
id
entity_type
name
canonical_name
description
country_code
industry
metadata_json
created_at
updated_at

Przykładowe entity_type:

company
market
country
industry
commodity
currency
customer_segment
supplier
competitor
trend
product

Przykłady:

company: Apple Inc.
commodity: Aluminum
market: Germany
industry: Direct Sales
currency: EUR
trend: AI automation
entity_aliases

Żeby ogarnąć różne nazwy tej samej rzeczy.

entity_aliases
--------------
id
entity_id
alias
source
created_at

Przykład:

Entity: Aluminum
Aliases:
- Aluminium
- ALU
- LME Aluminum

Albo:

Entity: Microsoft
Aliases:
- Microsoft Corp.
- MSFT
- Microsoft Corporation

Bez tego będziesz mieć duplikaty. A duplikaty w danych strategicznych to cichy sabotaż.

entity_relations

Relacje między bytami.

entity_relations
----------------
id
from_entity_id
to_entity_id
relation_type
strength
valid_from
valid_to
metadata_json
created_at

Przykłady:

Company X operates_in Germany
Company X competes_with Company Y
Aluminum impacts Industry Manufacturing
Trend AI automation impacts Market Direct Sales
Supplier X supplies Raw Material Y
6. Dane finansowe

Tu masz dwa poziomy:

1. financial_statements — większe sprawozdania / raporty
2. metrics — konkretne liczby, np. revenue, EBITDA, margin
financial_statements
financial_statements
--------------------
id
entity_id
raw_record_id
statement_type
period_type
period_start
period_end
currency
reported_at
source_url
confidence_level
metadata_json
created_at

Przykłady statement_type:

income_statement
balance_sheet
cash_flow
annual_report
quarterly_report

Przykłady period_type:

monthly
quarterly
yearly
ttm
metrics

To uniwersalna tabela na liczby w czasie.

metrics
-------
id
entity_id
raw_record_id
metric_name
metric_category
period_start
period_end
value_numeric
value_text
unit
currency
source
confidence_level
metadata_json
created_at

Przykłady metric_name:

revenue
gross_margin
ebitda
net_profit
operating_cash_flow
debt
market_share
customer_count
average_order_value
churn_rate

Przykład rekordu:

entity: Company X
metric_name: revenue
period_start: 2025-01-01
period_end: 2025-12-31
value_numeric: 120000000
currency: EUR
confidence_level: high

Ta tabela może też przyjmować inne KPI, nie tylko finansowe. Dlatego jest bardzo przydatna.

7. Ceny surowców

Dla cen surowców zrobiłbym osobną tabelę, bo to są dane czasowe, często dzienne/godzinowe.

commodity_prices
commodity_prices
----------------
id
commodity_entity_id
raw_record_id
price_date
price_timestamp
price_open
price_high
price_low
price_close
price_average
price_value
currency
unit
market
exchange
source
confidence_level
metadata_json
created_at

Przykłady:

commodity: Aluminum
price_date: 2026-05-12
price_value: 2450
currency: USD
unit: tonne
exchange: LME

Albo:

commodity: Brent Oil
price_value: 83.40
currency: USD
unit: barrel
market: global

Jeśli na start masz tylko jedną cenę dzienną, wystarczy używać:

price_date
price_value
currency
unit

Resztę zostaw jako opcjonalne.

8. Trendy

Trend to nie jest zwykła liczba. Trend ma opis, kierunek, siłę, horyzont, obszary wpływu.

trends
trends
------
id
raw_record_id
title
description
trend_category
direction
strength
maturity_stage
time_horizon
geography
impact_level
confidence_level
source_summary
metadata_json
created_at
updated_at

Przykłady trend_category:

technology
geopolitics
regulation
consumer_behavior
economy
supply_chain
industry
environment

Przykłady direction:

increasing
decreasing
emerging
stable
declining
unclear

Przykłady maturity_stage:

weak_signal
emerging_trend
mainstream
declining

Przykład:

title: AI automation in sales operations
trend_category: technology
direction: increasing
strength: high
maturity_stage: emerging_trend
time_horizon: 1-3 years
impact_level: high
confidence_level: medium
9. Sygnały

Sygnał to konkretna obserwacja, która może mieć znaczenie strategiczne.

signals
signals
-------
id
raw_record_id
title
description
signal_type
impact_level
confidence_level
urgency_level
time_horizon
status
source_summary
metadata_json
created_at
updated_at

Przykłady signal_type:

price_change
competitor_move
regulatory_change
market_shift
supply_risk
financial_warning
technology_shift
customer_behavior_change
geopolitical_risk

Przykład:

title: Aluminum price increased 12% over 30 days
signal_type: price_change
impact_level: medium
confidence_level: high
urgency_level: medium
time_horizon: 0-3 months

Sygnały powinny być później linkowane do encji.

10. Powiązania rekordów z encjami

Ponieważ każdy rekord może dotyczyć wielu bytów, potrzebujesz tabeli łączącej.

record_entities
record_entities
---------------
id
record_type
record_id
entity_id
relation_type
confidence_level
created_at

Przykład:

record_type: trend
record_id: trend_123
entity: Direct Sales
relation_type: impacts

Albo:

record_type: commodity_price
record_id: price_456
entity: Aluminum
relation_type: price_of

W bardziej eleganckim modelu można zrobić osobne tabele linkujące, ale dla MVP taka tabela jest praktyczna.

11. Processing
processing_jobs
processing_jobs
---------------
id
raw_record_id
job_type
status
started_at
finished_at
processor_name
processor_version
input_hash
output_record_type
output_record_id
metadata_json
created_at

Przykłady job_type:

extract_text
extract_entities
classify_record
extract_financial_metrics
extract_commodity_price
detect_trend
summarize
processing_errors
processing_errors
-----------------
id
processing_job_id
raw_record_id
error_type
error_message
stack_trace
created_at

To będzie bardzo potrzebne. Przetwarzanie danych z różnych źródeł będzie się sypać. Nie „czy”, tylko „kiedy”.

12. Jak to wygląda logicznie
source_apps
     |
     v
data_sources
     |
     v
raw_records
     |
     v
processing_jobs
     |
     +------------------> metrics
     |
     +------------------> financial_statements
     |
     +------------------> commodity_prices
     |
     +------------------> trends
     |
     +------------------> signals

A obok:

entities
   ^
   |
record_entities
   |
   v
metrics / prices / trends / signals
13. Przykład: dane finansowe konkurenta
Raw record
raw_records
record_type: financial_report
title: Company X Annual Report 2025
content_type: application/pdf
file_path: s3://raw/company-x/annual-report-2025.pdf
source_url: https://company-x.com/reports/2025
Processed financial statement
financial_statements
entity_id: Company X
statement_type: annual_report
period_start: 2025-01-01
period_end: 2025-12-31
currency: EUR
raw_record_id: raw_001
Metrics
metrics
entity_id: Company X
metric_name: revenue
value_numeric: 120000000
currency: EUR
period_start: 2025-01-01
period_end: 2025-12-31
metrics
entity_id: Company X
metric_name: ebitda
value_numeric: 18000000
currency: EUR
period_start: 2025-01-01
period_end: 2025-12-31
14. Przykład: cena surowca
Raw record
raw_records
record_type: commodity_price_api_response
title: LME Aluminum Daily Price
raw_payload_json: { ...oryginalna odpowiedź API... }
Commodity price
commodity_prices
commodity_entity_id: Aluminum
price_date: 2026-05-12
price_value: 2450
currency: USD
unit: tonne
exchange: LME
raw_record_id: raw_002
Signal

Jeżeli cena wzrosła mocno:

signals
title: Aluminum price increased 12% over 30 days
signal_type: price_change
impact_level: medium
confidence_level: high
raw_record_id: raw_002

I link:

record_entities
record_type: signal
record_id: signal_001
entity_id: Aluminum
relation_type: related_to
15. Przykład: trend
Raw record
raw_records
record_type: trend_article
title: AI adoption in sales organizations accelerates
raw_content: treść artykułu
source_url: ...
Trend
trends
title: AI automation in sales operations
trend_category: technology
direction: increasing
strength: high
maturity_stage: emerging_trend
time_horizon: 1-3 years
impact_level: high
confidence_level: medium
raw_record_id: raw_003
Powiązanie z encjami
record_entities
record_type: trend
record_id: trend_001
entity_id: Direct Sales
relation_type: impacts
record_entities
record_type: trend
record_id: trend_001
entity_id: AI
relation_type: driven_by
16. Czy robić jedną tabelę processed_records?

Można, ale ja bym uważał.

Masz dwie opcje.

Opcja A — jedna tabela processed_records
processed_records
-----------------
id
raw_record_id
record_type
title
summary
payload_json
impact_level
confidence_level
created_at

Plus wszystko w JSON.

To jest szybkie na MVP, ale słabsze do analiz liczbowych.

Opcja B — osobne tabele dla głównych typów danych
metrics
commodity_prices
trends
signals
financial_statements

To jest lepsze, bo dane finansowe i ceny surowców będziesz chciał filtrować, liczyć i wykresować.

Moja rekomendacja:

Zrób osobne tabele dla danych liczbowych i analitycznych, a JSON zostaw jako uzupełnienie.

Czyli:

metrics              — uniwersalne liczby/KPI
commodity_prices     — ceny surowców w czasie
trends               — trendy jakościowe
signals              — sygnały strategiczne
raw_records          — oryginał wszystkiego
17. Minimalny wariant na start

Jeżeli chcesz najprostszy, sensowny start, to wystarczy:

source_apps
data_sources
raw_records
entities
entity_aliases
metrics
commodity_prices
trends
signals
record_entities
processing_jobs

To jest dobra v0.1.

18. Przykładowy model PostgreSQL — uproszczony
CREATE TABLE source_apps (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    type TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'active',
    api_key_hash TEXT,
    last_seen_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE data_sources (
    id UUID PRIMARY KEY,
    source_app_id UUID REFERENCES source_apps(id),
    name TEXT NOT NULL,
    source_type TEXT NOT NULL,
    url TEXT,
    provider TEXT,
    trust_level TEXT,
    refresh_frequency TEXT,
    metadata_json JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE raw_records (
    id UUID PRIMARY KEY,
    source_app_id UUID REFERENCES source_apps(id),
    data_source_id UUID REFERENCES data_sources(id),
    external_id TEXT,
    record_type TEXT NOT NULL,
    title TEXT,
    raw_content TEXT,
    raw_payload_json JSONB DEFAULT '{}',
    content_type TEXT,
    language TEXT,
    source_url TEXT,
    file_path TEXT,
    checksum TEXT,
    collected_at TIMESTAMP,
    received_at TIMESTAMP DEFAULT now(),
    status TEXT DEFAULT 'stored',
    processing_status TEXT DEFAULT 'pending',
    metadata_json JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE entities (
    id UUID PRIMARY KEY,
    entity_type TEXT NOT NULL,
    name TEXT NOT NULL,
    canonical_name TEXT,
    description TEXT,
    country_code TEXT,
    industry TEXT,
    metadata_json JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE entity_aliases (
    id UUID PRIMARY KEY,
    entity_id UUID REFERENCES entities(id),
    alias TEXT NOT NULL,
    source TEXT,
    created_at TIMESTAMP DEFAULT now()
);

Dalej:

CREATE TABLE metrics (
    id UUID PRIMARY KEY,
    entity_id UUID REFERENCES entities(id),
    raw_record_id UUID REFERENCES raw_records(id),
    metric_name TEXT NOT NULL,
    metric_category TEXT,
    period_start DATE,
    period_end DATE,
    value_numeric NUMERIC,
    value_text TEXT,
    unit TEXT,
    currency TEXT,
    confidence_level TEXT,
    metadata_json JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE commodity_prices (
    id UUID PRIMARY KEY,
    commodity_entity_id UUID REFERENCES entities(id),
    raw_record_id UUID REFERENCES raw_records(id),
    price_date DATE NOT NULL,
    price_timestamp TIMESTAMP,
    price_open NUMERIC,
    price_high NUMERIC,
    price_low NUMERIC,
    price_close NUMERIC,
    price_average NUMERIC,
    price_value NUMERIC,
    currency TEXT,
    unit TEXT,
    market TEXT,
    exchange TEXT,
    confidence_level TEXT,
    metadata_json JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE trends (
    id UUID PRIMARY KEY,
    raw_record_id UUID REFERENCES raw_records(id),
    title TEXT NOT NULL,
    description TEXT,
    trend_category TEXT,
    direction TEXT,
    strength TEXT,
    maturity_stage TEXT,
    time_horizon TEXT,
    geography TEXT,
    impact_level TEXT,
    confidence_level TEXT,
    source_summary TEXT,
    metadata_json JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

CREATE TABLE signals (
    id UUID PRIMARY KEY,
    raw_record_id UUID REFERENCES raw_records(id),
    title TEXT NOT NULL,
    description TEXT,
    signal_type TEXT,
    impact_level TEXT,
    confidence_level TEXT,
    urgency_level TEXT,
    time_horizon TEXT,
    status TEXT DEFAULT 'new',
    source_summary TEXT,
    metadata_json JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT now(),
    updated_at TIMESTAMP DEFAULT now()
);

I tabela łącząca:

CREATE TABLE record_entities (
    id UUID PRIMARY KEY,
    record_type TEXT NOT NULL,
    record_id UUID NOT NULL,
    entity_id UUID REFERENCES entities(id),
    relation_type TEXT,
    confidence_level TEXT,
    created_at TIMESTAMP DEFAULT now()
);
19. Ważna uwaga o record_entities

W SQL nie da się łatwo zrobić normalnego foreign key do różnych tabel naraz, jeśli masz:

record_type + record_id

Czyli record_id może wskazywać na metrics, trends, signals, itd.

Na MVP to jest akceptowalne.

Bardziej porządnie można zrobić osobne tabele:

metric_entities
trend_entities
signal_entities

Ale na start record_entities jest praktyczniejsze.

20. Co bym zrobił jako pierwsze

Najpierw zaimplementowałbym:

1. source_apps
2. data_sources
3. raw_records
4. entities
5. metrics
6. commodity_prices
7. trends
8. signals

I dopiero potem relacje, processing jobs, scoringi i dashboardy.

21. Najważniejsza decyzja projektowa

Dla Twojego przypadku rdzeniem bazy powinny być dwie rzeczy:

raw_records
entities

A dopiero wokół nich:

metrics
commodity_prices
trends
signals

Czyli:

raw_records = dowody
entities = czego to dotyczy
metrics/prices/trends/signals = co z tego wyciągnęliśmy