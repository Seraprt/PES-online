# ADR 0003 — Realtime and match lifecycle

- Status: accepted
- Phase: 1

## Context

Lobby, matchmaking, rooms and tournaments need live updates, while the game
itself is launched locally by the companion app. The server must remain
authoritative and tolerate disconnects.

## Decision

- REST is the contract; WebSocket is a derived event stream.
- Every WS message uses a versioned envelope with per-channel monotonic `seq`.
- Room state changes increment `rooms.version` inside the same transaction that
  writes the change, then publish an event.
- Match results require host submission plus guest confirmation; otherwise the
  match becomes `disputed`.
- Companion launch is a signed, expiring command over the room channel, not a
  direct file manipulation by the server.

## Consequences

- Clients can recover full state with a REST GET after reconnect.
- Duplicate or reordered events are discarded by `seq`.
- Result disputes require an explicit resolution path (admin or tournament engine).