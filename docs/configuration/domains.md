---
layout: default
title: Domains & Upstream
parent: Configuration
nav_order: 2
---

# Domains & Upstream

```yaml
domains:
  cdn.example.com:
    upstream: "${CS_UPSTREAM}"
    profile_path: "profiles/my.profile"
    profile_type: "cobalt_strike"

    drop_action:
      type: "redirect"          # redirect | proxy | static | 404
      target: "https://jquery.com"

    allowed_paths:
      - "/jquery-3.7.1.min.js"
      - "/cdn-cgi/*"
      - "~^/[a-z]{8}$"          # regex (prefix with ~)

    content_routes: []           # payload delivery routes
```

## `profile_type` Values

| Value | Parser | Profile file required |
|---|---|---|
| `cobalt_strike` | Malleable C2 | Yes — `.profile` |
| `mythic` | Mythic HTTPX | Yes — `.json` |
| `brute_ratel` | BRC4 config JSON | Yes — `.json` |
| `sliver` | Sliver HTTP config | Yes — `.yaml` |
| `havoc` | Havoc listener YAML | Yes — `.yaml` |
| `nighthawk` | Nighthawk listener JSON | Yes — `.json` |
| `poshc2` | PoshC2 config YAML | Yes — `.yaml` |
| `gophish` | Built-in GoPhish patterns | No |
| `evilginx` | Optional phishlet YAML | Optional |
| `cuddlephish` | Built-in OAuth patterns | No |
| `phishing_club` | Built-in passthrough | No |
| `passthrough` | No profile filtering | No |

## `drop_action` Types

| Type | Behavior |
|---|---|
| `redirect` | HTTP 302 to `target` URL |
| `proxy` | Silently proxy to `target` (mimics the cover site) |
| `static` | Serve a static HTML file at `target` path |
| `404` | Return 404 with no body |

## Campaign Token (Phishing Domains)

```yaml
campaign_token:
  enabled: true
  token_param: "t"
  tokens:
    - "${CAMPAIGN_TOKEN_Q1}"
  # hmac_secret: "${CAMPAIGN_HMAC_SECRET}"
  # hmac_ttl_seconds: 604800
  score_on_missing: 0.8
```
