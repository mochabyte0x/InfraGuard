---
layout: default
title: Phishing.club
parent: Phishing Frameworks
grand_parent: Frameworks
nav_order: 4
---

# Phishing.club

Advanced phishing platform with credential capture, OAuth flow support, and campaign management. InfraGuard integrates via webhook for real-time campaign events.

## Config

```yaml
domains:
  phish.example.com:
    upstream: "${PHISHINGCLUB_UPSTREAM}"
    profile_type: "phishing_club"

    campaign_token:
      enabled: true
      token_param: "t"
      tokens:
        - "${CAMPAIGN_TOKEN_Q1}"
      score_on_missing: 0.8

    drop_action:
      type: "redirect"
      target: "https://example.com"

phishingclub:
  enabled: true
  webhook_path: "/wb/pc"
  webhook_secret: "${PHISHINGCLUB_WEBHOOK_SECRET}"
  whitelist_on_click: false
  event_result_label: "allow"
```

See `config/examples/phishing-club.yaml`.

## Webhook Integration

Configure phishing.club to POST to `https://phish.example.com/wb/pc`. Set the webhook secret in phishing.club admin UI.

InfraGuard validates `X-Signature: sha256=<hex>`, records the event to the tracking DB, and dispatches alerts via plugins.

## Event Scores

| Event | Score | Alert |
|---|---|---|
| `credentials_submitted` | 1.0 | High-value |
| `oauth_token_captured` | 1.0 | High-value |
| `device_code_captured` | 1.0 | High-value |
| `mfa_submitted` | 1.0 | High-value |
| `link_clicked` | 0.5 | Standard |
| `email_opened` | 0.5 | Standard |

## `whitelist_on_click`

When `true`, clicking IP is automatically promoted to the C2 dynamic whitelist — once phished, beacon is trusted without waiting for N checkins.
