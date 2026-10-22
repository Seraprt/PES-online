# ADR 0001 — Monorepo layout

- Status: accepted
- Phase: 1

## Context

The platform spans a React SPA, a FastAPI backend, a Windows desktop app and
shared contracts. A single repository keeps contract changes atomic across all
consumers and lets one CI pipeline enforce architecture rules.

## Decision

Use one repository with `apps/` (deployables), `packages/` (shared libraries and
contracts), `infra/` (runtime configuration), `docs/` (architecture and ADRs)
and `tools/` (repository tooling). Each app owns its dependency manifest.
Shared code goes through `packages/contracts` or `packages/shared_py`.

## Consequences

- One PR can change API, contract and clients together.
- CI must run per-app jobs, not one global test command.
- Boundaries are enforced by review and by `tools/check_architecture.py`.
- Deployments remain per-app on Render.