# Finance REST API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

A REST API for personal budget management: accounts, categories, transactions, and monthly summaries. Built with **FastAPI**, **SQLAlchemy 2.0**, and **SQLite** using Pydantic v2 schemas.

## Features

- **Accounts** — create/list/update/delete accounts with an initial balance and currency. Balance is **computed on the fly** from transactions (never stored, so it can't go stale).
- **Categories** — income / expense / adjustment categories. A seed-created system **«Correction»** category for adjustments is protected from being created, edited, or deleted by users.
- **Transactions** — full CRUD. Transactions link to an account and a category; the transaction type (income/expense/adjustment) is derived from the category — a single source of truth.
- **Data integrity guarantees:**
  - Money is stored as `Decimal` (`Numeric(10, 2)`) — no float rounding errors.
  - Zero-amount transactions are rejected.
  - Balance can never go negative (returns `400 Insufficient funds`).
  - `ON DELETE RESTRICT` foreign keys + `PRAGMA foreign_keys = ON` — referential integrity is enforced by the DB itself, with clean `409` errors surfaced by the API.
- **Reports** — income / expense totals and transaction count for a given month or all time, via `GET /reports/summary`.

## Tech Stack

| Layer      | Technology                  |
|------------|-----------------------------|
| Web        | FastAPI, Uvicorn            |
| Validation | Pydantic v2                 |
| ORM        | SQLAlchemy 2.0              |
| Database   | SQLite                      |

## Structure

```
finance_rest_api/
├── main.py              # app entry: create_all, seed, routers
├── database.py          # engine, session factory, FK pragma on connect
├── models.py            # ORM models: Account, Category, Transaction
├── schemas.py           # Pydantic schemas (Base/Create/Update/Response)
├── enums.py             # CategoryType: income / expense / adjustment
├── helpers.py           # balance computation, transaction delta, guards
├── seed.py              # system "Correction" category
└── routes/
    ├── accounts.py      # CRUD /accounts
    ├── categories.py    # CRUD /categories
    ├── transactions.py  # CRUD /transactions
    └── reports.py       # GET /reports/summary
```

## Getting Started

Requires Python 3.13+.

```bash
# 1. Create a virtual environment and install dependencies
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/macOS

pip install -r requirements.txt

# 2. Run the server
uvicorn main:app --reload
```

On startup the app creates the tables in `db/finance.db` and seeds the system category.

## Interactive docs

Open <http://127.0.0.1:8000/docs> — Swagger UI with every endpoint, request/response examples, and the ability to execute requests directly.

## API Overview

| Method | Endpoint                | Description                                  |
|--------|-------------------------|----------------------------------------------|
| POST   | `/accounts`             | Create an account (name, currency, initial_balance) |
| GET    | `/accounts`             | List accounts with computed balances         |
| GET    | `/accounts/{id}`        | Get one account with computed balance        |
| PATCH  | `/accounts/{id}`        | Partially update an account                  |
| PUT    | `/accounts/{id}`        | Replace an account                           |
| DELETE | `/accounts/{id}`        | Delete an account                            |
| POST   | `/categories`           | Create a category (income/expense)           |
| GET    | `/categories`           | List categories                              |
| GET    | `/categories/{id}`      | Get one category                             |
| PATCH  | `/categories/{id}`      | Partially update a category                  |
| PUT    | `/categories/{id}`      | Replace a category                           |
| DELETE | `/categories/{id}`      | Delete a category (409 if referenced)        |
| POST   | `/transactions`         | Create a transaction (account_id, category_id, amount, date) |
| GET    | `/transactions`         | List transactions                            |
| GET    | `/transactions/{id}`    | Get one transaction                          |
| PATCH  | `/transactions/{id}`    | Partially update a transaction               |
| PUT    | `/transactions/{id}`    | Replace a transaction                        |
| DELETE | `/transactions/{id}`    | Delete a transaction                         |
| GET    | `/reports/summary`      | Income/expense/net/count, filtered by `account_id`, `month=YYYY-MM`, `category_id` |

### Example: monthly report

```
GET /reports/summary?account_id=1&month=2026-09
```

```json
{
  "income": "1500.00",
  "expense": "830.50",
  "net": "669.50",
  "transactions_count": 12
}
```

`net` = `income - expense` over the selected slice. When filtered to a single expense category, `net` is negative — that is the category's net effect on the account.

## How balance works

Balance is never stored. It is recomputed on each read:

```
balance = account.initial_balance + Σ(transactions contribution)
```

where each transaction contributes `+amount` for income/adjustment and `-amount` for expense. This removes the risk of a stored counter drifting from the actual transaction history.

## Design notes

- **Type comes from the category, not the transaction.** Storing `transaction_type` on the transaction as well would create two sources of truth that can disagree.
- **Amount is always positive.** The direction of money movement is decided by the category (`expense` subtracts). Exception: `adjustment` carries its own sign.
- **RESTRICT, not CASCADE.** Financial history is never silently deleted.