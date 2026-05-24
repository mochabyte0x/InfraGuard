---
layout: default
title: Pipeline Filters
parent: Configuration
nav_order: 3
---

# Pipeline Filters

```yaml
pipeline:
  filter_mode: "scoring"        # scoring | strict
  block_score_threshold: 0.7

  enable_ip_filter: true
  enable_bot_filter: true
  enable_header_filter: true
  enable_geo_filter: true
  enable_dns_filter: true
  enable_profile_filter: true
  enable_replay_filter: true
  replay_window_seconds: 86400
  replay_persist: true

  enable_enumeration_filter: true
  enumeration_unique_path_threshold: 20
  enumeration_unique_path_suspect_threshold: 8
  enumeration_window_seconds: 60

  enable_sandbox_filter: true
  enable_ja3_filter: true
  ja3_filter:
    ja3_header: "x-ja3"
    log_ja3: true
    block_unknown: false
    blocked_ja3:
      - "e7d705a3286e19ea42f587b344ee6865"   # Masscan
      - "c35b0c7bd583d49d5b0f17de25ecdf7a"   # ZGrab2
      - "6734f37431670b3ab4292b8f60f29984"   # Python requests
      - "b386946a5a44d1ddcc843bc75336dfce"   # curl
```

## Filter Modes

| Mode | Behavior |
|---|---|
| `scoring` | Accumulate scores; block when total ≥ threshold |
| `strict` | Any single BLOCK result immediately drops the request |

`scoring` — recommended for phishing. `strict` — recommended for C2.

## Filters

| Filter | What it checks |
|---|---|
| IP | Blocklist, threat intel feeds, Tor exits, cloud ranges |
| Bot | User-Agent string — headless, curl, wget, scanner UAs |
| Header | Missing Accept, unusual ordering, scanner headers |
| Geo | Country and ASN geofencing |
| DNS | Reverse DNS — cloud hosting, Tor PTR records |
| Profile | C2/phishing profile URI/method/header match |
| Sandbox | Headless browser signals (HeadlessChrome UA, missing Accept-Language, etc.) |
| JA3 | TLS fingerprint — blocks Masscan, curl, ZGrab2 at handshake |
| Replay | Dedup within window; SQLite-persisted when `replay_persist: true` |
| Enumeration | Per-IP unique path count — catches dirbuster/ffuf |

## CLI Pipeline Management

```bash
infraguard config pipeline enable sandbox_filter -c config.yaml
infraguard config pipeline disable replay_filter -c config.yaml
infraguard config pipeline set-threshold 0.65 -c config.yaml
infraguard config pipeline ja3 block e7d705a3286e19ea42f587b344ee6865 -c config.yaml
infraguard config pipeline ja3 list -c config.yaml
```
