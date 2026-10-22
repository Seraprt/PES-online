# System Architecture — PES Online Evolution

## 1. Context

PES 2017 PC with the PS 2026 Patch is the football engine and is not modified by
the platform. Everything in this repository is a control plane around it:
identity, presence, social graph, lobby, matchmaking, rooms, tournaments,
squads, Master League history and content updates.

Hard constraints:

- The server never simulates a match and never patches the game binary.
- Match results are only accepted through an explicit, auditable flow.
- Master League save files are never mutated without a backup.
- Every realtime feature must degrade gracefully to REST when the socket drops.

## 2. Components

```mermaid
flowchart LR
    Player([Player]) --> Web[Web SPA<br/>React + Vite]
    Player --> Companion[Windows Companion<br/>CustomTkinter]
    Web -->|REST over HTTPS| API[FastAPI API]
    Web <-->|WSS /ws| API
    Companion <-->|WSS /ws with device token| API
    API --> PG[(PostgreSQL 16)]
    API --> B2[(Backblaze B2)]
    Companion -->|detect / verify / backup / launch| PES[PES 2017 + PS 2026 Patch]
    Companion -->|career snapshot upload| API
    Admin([Tournament admin]) --> Web