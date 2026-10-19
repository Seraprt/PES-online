
---

### File: `CHANGELOG.md`

```markdown
# Changelog

All notable changes to PES Online Evolution are documented here.
The format follows Keep a Changelog; the project uses semantic versioning.
Every phase must append exactly one entry.

## [0.1.0] — Phase 1: Project Architecture

### Added
- Monorepo layout for `apps/api`, `apps/web`, `apps/companion`,
  `packages/contracts`, `packages/shared_py`, `infra`, `docs`, `tools`.
- System architecture document covering components, trust boundaries,
  match lifecycle, realtime protocol, storage and deployment.
- API surface reservation for authentication, users, friends, matchmaking,
  rooms, matches, tournaments, squads, career, updates, notifications,
  devices and the realtime channel.
- Domain model with entity list, relationships and invariants.
- Phase plan for all 16 phases with definition-of-done gates.
- Architecture Decision Records 0001–0004.
- PostgreSQL 16 development service via Docker Compose with healthcheck.
- Environment template `.env.example` with every required configuration key.
- `tools/check_architecture.py` conformance checker (structure, env keys,
  compose service, placeholder markers, Makefile targets).
- GitHub Actions CI running the architecture check and compose validation.
- Developer Makefile with help, env, up, down, logs, reset-db, psql,
  check, compose-config and verify targets.

### Notes
- No application code from Phase 2 onward has been generated yet.
- Phase 2 (Backend Foundation) starts only after Phase 1 is tested.