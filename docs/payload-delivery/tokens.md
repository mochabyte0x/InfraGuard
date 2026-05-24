---
layout: default
title: One-Time Payload Tokens
parent: Payload Delivery
nav_order: 3
---

# One-Time Payload Tokens

Prevents replayed payload URLs. Beacon receives a single-use token when promoted to the dynamic whitelist. Must present it to download any route with `require_token: true`.

## Config

```yaml
payload_tokens:
  enabled: true
  default_ttl_seconds: 3600
  default_max_uses: 1
  token_header: "X-DL-Token"
  token_param: "_t"
  issuance_header: "X-Payload-Token"
```

Enable on a route:

```yaml
content_routes:
  - path: "/jquery-3.7.1.min.js"
    backend: ...
    require_token: true
```

## Flow

1. Beacon completes N valid C2 checkins (`dynamic_whitelist_threshold`)
2. IP promoted to dynamic whitelist
3. Token issued — returned in `X-Payload-Token` response header
4. Beacon presents token in `X-DL-Token` header (or `?_t=`) on payload download
5. Atomic `UPDATE ... WHERE used_count < max_uses` — rowcount 0 = already consumed → 403

## Atomic Consumption

```sql
UPDATE payload_tokens
SET used_count = used_count + 1
WHERE token = ?
  AND used_count < max_uses
  AND expires_at > unixepoch()
```

Single statement eliminates read-then-write race conditions.

## Multi-Stage Payloads

```yaml
payload_tokens:
  default_max_uses: 3    # stage1 + stage2 + config
```

## Debugging

```bash
sqlite3 /data/infraguard.db \
  "SELECT token, beacon_ip, used_count, datetime(expires_at,'unixepoch') FROM payload_tokens;"
```
