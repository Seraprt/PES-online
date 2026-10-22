# Domain Model

Conceptual model for Phase 3. Field lists are the contract; migrations must
match them. All identifiers are UUIDv4 unless stated otherwise.

## Entities

### Identity and social

| Entity | Key fields | Notes |
|---|---|---|
| `users` | id, email (unique, citext), username (unique), password_hash, email_verified_at, status, created_at, updated_at, deleted_at | status: active, suspended, deleted |
| `user_profiles` | user_id PK/FK, display_name, avatar_url, region, favorite_club_id, bio, last_seen_at | online status is derived, not stored |
| `refresh_tokens` | id, user_id, token_hash, user_agent, ip, expires_at, revoked_at | hash only, never the raw token |
| `email_tokens` | id, user_id, purpose, token_hash, expires_at, consumed_at | purpose: verify_email, reset_password |
| `friend_requests` | id, requester_id, addressee_id, status, message, created_at, responded_at | at most one pending per ordered pair |
| `friendships` | user_id, friend_id, created_at | canonical ordering `user_id < friend_id`, composite PK |
| `blocks` | blocker_id, blocked_id, created_at | composite PK; overrides friendship |

### Competition

| Entity | Key fields | Notes |
|---|---|---|
| `clubs` | id, patch_club_id, name, league, country, overall | imported from PS 2026 patch data |
| `players` | id, patch_player_id, name, club_id, position, overall, nationality, attributes (jsonb) | patch player database |
| `squads` | id, owner_id, name, formation, mode, rating, is_active, created_at | mode: club, custom |
| `squad_players` | squad_id, player_id, slot, is_captain, is_bench, position_order | composite PK |
| `rooms` | id, code, host_id, guest_id, mode, visibility, status, settings (jsonb), tournament_fixture_id, version, created_at, expires_at | `version` increments on every state change |
| `matches` | id, room_id, tournament_fixture_id, home_user_id, away_user_id, home_score, away_score, status, competition_type, played_at | status: pending, confirmed, disputed, voided |
| `match_events` | id, match_id, type, payload (jsonb), created_at | append-only |
| `tournaments` | id, name, format, visibility, max_participants, rules (jsonb), status, created_by, starts_at | format: knockout, round_robin, group_stage |
| `tournament_participants` | tournament_id, user_id, seed, squad_id, status, registered_at | composite PK |
| `tournament_fixtures` | id, tournament_id, round, leg, home_user_id, away_user_id, home_score, away_score, aggregate, status, room_id, scheduled_at | two-leg supported via `leg` |

### Platform

| Entity | Key fields | Notes |
|---|---|---|
| `notifications` | id, user_id, type, payload (jsonb), read_at, created_at | fan-out target for WS |
| `career_profiles` | user_id PK/FK, current_club_id, season, league_position, trophies (jsonb), synced_at | one row per user |
| `career_snapshots` | id, user_id, season, payload (jsonb), sha256, size_bytes, storage_key, created_at | append-only |
| `content_packs` | id, kind, version, manifest (jsonb), storage_key, sha256, compatibility (jsonb), status, released_at | kind: transfers, boots, kits, faces, stadiums |
| `installations` | id, user_id, device_id, pes_path, patch_version, sider_version, content_pack_versions (jsonb), verified_at | one per device |
| `device_pairings` | id, user_id, device_fingerprint, name, token_hash, paired_at, last_seen_at | companion auth |
| `audit_logs` | id, actor_id, action, target_type, target_id, metadata (jsonb), created_at | append-only |

## Relationships

```mermaid
erDiagram
    users ||--|| user_profiles : has
    users ||--o{ refresh_tokens : owns
    users ||--o{ friend_requests : sends
    users ||--o{ blocks : blocks
    users ||--o{ squads : owns
    users ||--o{ rooms : hosts
    users ||--o{ matches : plays
    users ||--|| career_profiles : has
    users ||--o{ career_snapshots : uploads
    users ||--o{ device_pairings : pairs
    users ||--o{ installations : registers
    clubs ||--o{ players : contains
    clubs ||--o{ squads : selected_by
    squads ||--o{ squad_players : contains
    players ||--o{ squad_players : listed_in
    rooms ||--o| matches : produces
    tournaments ||--o{ tournament_participants : has
    tournaments ||--o{ tournament_fixtures : schedules
    tournament_fixtures ||--o| rooms : played_in
    matches ||--o{ match_events : records
    content_packs ||--o{ installations : installed_on