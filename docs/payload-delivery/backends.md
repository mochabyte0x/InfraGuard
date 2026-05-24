---
layout: default
title: Backends
parent: Payload Delivery
nav_order: 2
---

# Payload Backends

## `mythic_file`

Fetches from Mythic's file store via `/direct/download/<uuid>`.

**Specific UUID:**
```yaml
backend:
  type: "mythic_file"
  target: "https://${MYTHIC_IP}:7443"
  file_id: "${MYTHIC_STAGE2_FILE_ID}"
  ssl_verify: false
```

**Dynamic UUID (omit `file_id`):**
```yaml
- path: "/dl/*"
  backend:
    type: "mythic_file"
    target: "https://${MYTHIC_IP}:7443"
    ssl_verify: false
```

`/dl/abc123` → Mythic `/direct/download/abc123`.

---

## `pwndrop`

```yaml
backend:
  type: "pwndrop"
  target: "${PWNDROP_UPSTREAM}"
  auth_token: "${PWNDROP_TOKEN}"
```

---

## `filesystem`

```yaml
backend:
  type: "filesystem"
  target: "/app/decoys"
```

`/assets/jquery.min.js` → `/app/decoys/assets/jquery.min.js`. Path traversal prevented.

Use without a guard stack for decoy content served to all visitors:

```yaml
- path: "/assets/*"
  backend:
    type: "filesystem"
    target: "/app/decoys"
  rate_limit:
    enabled: true
    max_downloads: 10
    window_seconds: 60
  track: false
```

---

## `http_proxy`

```yaml
backend:
  type: "http_proxy"
  target: "${REDFILE_UPSTREAM}"
  ssl_verify: false
```

Proxies request path and headers. Ideal for RedFile, nginx, or as the `conditional.scanner_backend`.
