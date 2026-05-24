---
layout: default
title: Quickstart
parent: Getting Started
nav_order: 2
---

# Quickstart

## 1. Pick an Example Config

```bash
cp config/examples/c2-cobalt-strike.yaml config/config.yaml
```

All example configs live in `config/examples/`.

## 2. Set Required Env Vars

```bash
export INFRAGUARD_TLS_CERT=/path/to/cert.pem
export INFRAGUARD_TLS_KEY=/path/to/key.pem
export INFRAGUARD_DB_PATH=/tmp/infraguard.db
export CS_UPSTREAM=https://10.10.10.10:443
```

## 3. Point Your C2 Profile

```yaml
domains:
  cdn.example.com:
    upstream: "${CS_UPSTREAM}"
    profile_path: "profiles/my-campaign.profile"
    profile_type: "cobalt_strike"
```

## 4. Start InfraGuard

```bash
# Docker
docker compose up -d

# Direct
infraguard run --config config/config.yaml
```

## 5. Verify

```bash
curl -k https://localhost/up
docker compose logs -f infraguard
```

## What Happens on a Request

```
Incoming HTTPS request
        │
        ▼
TLS termination (InfraGuard cert)
        │
        ▼
Pipeline filters (IP → bot → geo → DNS → profile → sandbox → JA3 → replay → enumeration)
        │
        ├── score ≥ threshold ──► drop_action (redirect / serve decoy / 404)
        │
        └── score < threshold ──► proxy to upstream C2 / phishing backend
```
