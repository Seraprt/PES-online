
---

### File: `docs/phase-plan.md`

```markdown
# Phase Plan

Phases are sequential. Each phase ends with a gate. Do not begin the next phase
until the gate passes and the previous phase is approved.

| # | Phase | Deliverables | Gate |
|---|---|---|---|
| 1 | Project architecture | Monorepo, docs, compose, CI, conformance tool | `make verify` green |
| 2 | Backend foundation | FastAPI app factory, settings, logging, errors, health, contracts package | `/health` and `/health/ready` return 200; tests pass |
| 3 | Database | SQLAlchemy models, Alembic baseline, indexes, invariants | `alembic upgrade head` on empty DB; model tests pass |
| 4 | Authentication | Register, login, refresh, verify, reset, JWT, Argon2, rate limits | Full auth flow test; token rotation test |
| 5 | Windows companion | Detection, verification, backup, launch, pairing, WS client | Runs on Windows, pairs to API, launches PES |
| 6 | Online lobby | Web shell, lobby UI, presence, notifications, rooms read path | Lobby renders live presence; WS reconnect works |
| 7 | Friend system | Requests, accept/reject, remove, block, invites | Two-user integration test |
| 8 | Matchmaking | Queue, pairing, region/mode/ranked rules, room creation | Deterministic pairing test with fake clock |
| 9 | Friendly matches | Host settings, guest confirmation, result flow | End-to-end room lifecycle test |
| 10 | Tournaments | Formats, fixtures, two-leg, aggregate, penalties, admin tools | Bracket and round-robin fixtures verified |
| 11 | Squad builder | Patch player DB, XI/bench/formation/captain, limits, caps | Validation rejects illegal squads |
| 12 | PES integration | Launch handshake, signed commands, result ingestion | Companion launches game from lobby |
| 13 | Master League sync | Snapshot upload, career profile, timeline, backup policy | Snapshot integrity and restore test |
| 14 | Update manager | Content packs, compatibility, rollback, B2 distribution | Install/rollback test against B2 |
| 15 | Security | Rate limiting, anti-cheat prep, audit, input hardening | Security checklist signed off |
| 16 | Deployment | Render blueprint, migrations on deploy, backups, monitoring | Staging deploy reachable and healthy |

## Rules

1. One phase per pull request.
2. Every phase appends a `CHANGELOG.md` entry with the phase number.
3. Every phase includes setup commands, testing instructions and a commit message.
4. The architecture check runs in CI for every phase.
5. No phase may change a previously published API shape without an ADR.