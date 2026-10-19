# PES Online Evolution

A production-quality online platform built **around** PES 2017 PC with the PS 2026 Patch.
The original game remains the football engine. This repository is the control plane:
accounts, presence, lobby, matchmaking, rooms, tournaments, squads, Master League sync
and content updates.

## Stack

| Layer      | Technology                                                        |
|------------|-------------------------------------------------------------------|
| Frontend   | React, TypeScript, Vite, Tailwind CSS                             |
| Backend    | Python 3.12, FastAPI, SQLAlchemy 2 (async), PostgreSQL, WebSockets|
| Desktop    | Python, CustomTkinter, pywin32, watchdog                          |
| Storage    | Backblaze B2                                                      |
| Deployment | Render (API + static site + managed Postgres), B2 for assets      |

## Repository layout

- `apps/api` — FastAPI service (REST + `/ws`).
- `apps/web` — React SPA.
- `apps/companion` — Windows companion app.
- `packages/contracts` — OpenAPI contract and generated clients.
- `packages/shared_py` — shared Python primitives.
- `infra` — Docker, Render, operational scripts.
- `docs` — architecture, API surface, domain model, ADRs, phase plan.
- `tools` — repository conformance tooling.

## Quickstart (development)

```bash
git clone <repo-url> pes-online-evolution
cd pes-online-evolution
make env            # creates .env from .env.example
make up             # starts PostgreSQL 16
make verify         # architecture check + compose validation"# PES-online" 
