---
layout: default
title: Listeners & TLS
parent: Configuration
nav_order: 1
---

# Listeners & TLS

```yaml
listeners:
  - protocol: "https"        # https | http
    bind: "0.0.0.0"
    port: 443
    tls:
      cert: "${INFRAGUARD_TLS_CERT}"
      key: "${INFRAGUARD_TLS_KEY}"
    domains:
      - "cdn.example.com"
```

## Multiple Listeners

```yaml
listeners:
  - protocol: "https"
    bind: "0.0.0.0"
    port: 443
    tls:
      cert: "${C2_CERT}"
      key: "${C2_KEY}"
    domains:
      - "cdn.example.com"

  - protocol: "https"
    bind: "0.0.0.0"
    port: 8443
    tls:
      cert: "${PHISH_CERT}"
      key: "${PHISH_KEY}"
    domains:
      - "phish.example.com"
```

## HTTP (No TLS)

For lab use or when TLS is terminated upstream:

```yaml
listeners:
  - protocol: "http"
    bind: "127.0.0.1"
    port: 8080
    domains:
      - "localhost"
```

> **Warning:** Never run HTTP listeners on a public interface in production. TLS is required — HTTP exposes the C2 profile and all implant traffic in plaintext.

## Domain Routing

The `domains` list determines which hostnames InfraGuard accepts on that listener. Each domain must have a corresponding key in the top-level `domains:` map.
