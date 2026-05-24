---
layout: default
title: Architecture
nav_order: 7
has_children: false
---

# Architecture

## Infrastructure Diagram

<div style="text-align:center; margin: 1.5rem 0;">
  <img src="/assets/images/infrastructure-diagram.png" alt="InfraGuard Infrastructure Diagram" style="max-width:100%; border-radius:6px;" />
</div>

InfraGuard sits between the internet and your C2/phishing backends. IG Redirectors handle all inbound traffic — filtering, scoring, and proxying only legitimate requests to the Command Post or Decoy Server.

## Request Flow

```
Internet
   │
   ▼ HTTPS (443)
┌──────────────────────────────────────────────────────┐
│  InfraGuard                                          │
│                                                      │
│  TLS Termination                                     │
│       │                                              │
│       ▼                                              │
│  SNI/Host routing → Domain config lookup             │
│       │                                              │
│       ▼                                              │
│  Pipeline Filters (ordered, scored)                  │
│    ├── IPFilter                                      │
│    ├── BotFilter                                     │
│    ├── HeaderFilter                                  │
│    ├── GeoFilter                                     │
│    ├── DNSFilter                                     │
│    ├── ProfileFilter (C2/phishing profile match)     │
│    ├── SandboxFilter (headless browser detection)    │
│    ├── JA3Filter (TLS fingerprint)                   │
│    ├── ReplayFilter (dedup window)                   │
│    └── EnumerationFilter (path count per IP)         │
│       │                                              │
│       ├── score ≥ threshold                          │
│       │       └── drop_action (redirect/proxy/404)   │
│       │                                              │
│       └── score < threshold                          │
│               │                                      │
│               ▼                                      │
│         Content route match?                         │
│           ├── Yes → Guard stack → Backend            │
│           └── No  → Proxy to upstream C2/phishing    │
└──────────────────────────────────────────────────────┘
```

## Components

| Component | Path | Role |
|---|---|---|
| Listeners | `infraguard/listeners/` | TLS termination, one per `listeners[]` entry |
| Router | `infraguard/core/router.py` | Domain lookup, filter pipeline, proxy dispatch |
| Pipeline filters | `infraguard/pipeline/` | Scored filter chain |
| C2 profiles | `infraguard/profiles/` | Profile parsers → normalized `C2Profile` |
| Intel | `infraguard/intel/` | CT monitor, reputation, feed refresh |
| Tracking | `infraguard/tracking/` | SQLite — requests, tokens, replay, whitelist |
| Plugins | `infraguard/plugins/` | Discord, Slack, syslog event dispatch |
| Integrations | `infraguard/integrations/` | Inbound webhooks (phishing.club) |

## Database Schema

```sql
CREATE TABLE requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp INTEGER NOT NULL,
    ip TEXT NOT NULL,
    domain TEXT NOT NULL,
    method TEXT NOT NULL,
    path TEXT NOT NULL,
    score REAL NOT NULL,
    filter_result TEXT NOT NULL,
    filter_reason TEXT,
    user_agent TEXT,
    metadata TEXT
);

CREATE TABLE payload_tokens (
    token TEXT PRIMARY KEY,
    beacon_ip TEXT NOT NULL,
    route_path TEXT NOT NULL,
    issued_at INTEGER NOT NULL,
    expires_at INTEGER NOT NULL,
    max_uses INTEGER NOT NULL DEFAULT 1,
    used_count INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE replay_tokens (
    hash TEXT PRIMARY KEY,
    seen_at INTEGER NOT NULL
);
```

## Concurrency Model

Runs on asyncio. All filter evaluation and upstream proxying is async. SQLite writes use `aiosqlite`. Intel monitors run as `asyncio.Task` objects started in the ASGI lifespan.

## Hot Reload

Send `SIGHUP` to reload config without dropping connections. In-memory whitelist and SQLite DB are preserved. Filter state (replay window, rate limits) resets — acceptable since reloads are operator-initiated.

```bash
docker compose kill -s HUP infraguard
```
