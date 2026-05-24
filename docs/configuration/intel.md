---
layout: default
title: Intel & Burn Detection
parent: Configuration
nav_order: 4
---

# Intel & Burn Detection

```yaml
intel:
  auto_block_scanners: true
  dynamic_whitelist_threshold: 3

  feeds:
    enabled: true
    refresh_interval_hours: 12

  ct_monitor:
    enabled: true
    interval_hours: 4.0
    monitored_domains:
      - "cdn.example.com"   # omit to auto-populate from domains block

  reputation_monitor:
    enabled: true
    interval_hours: 2.0
    check_urlhaus: true
    check_openphish: true
```

## Dynamic IP Whitelisting

Each valid C2 checkin increments the beacon IP's counter. At `dynamic_whitelist_threshold` checkins, the IP is promoted to the dynamic whitelist — skipping most pipeline scoring and becoming eligible for one-time payload tokens.

## Certificate Transparency Monitoring

Polls `crt.sh` for each monitored domain. New cert issuances fire a `BurnIndicator(severity="critical")` and dispatch an alert via configured plugins (Discord/Slack).

## Domain Reputation Monitoring

| Feed | Detects |
|---|---|
| URLhaus | Domains hosting malware |
| OpenPhish | Active phishing sites |

On a hit, `BurnIndicator` fires. InfraGuard continues operating — operator decides whether to burn the domain.

## CLI Intel Management

```bash
infraguard config intel block-country RU -c config.yaml
infraguard config intel unblock-country RU -c config.yaml
infraguard config intel block-asn 15169 -c config.yaml
infraguard config intel block-ip 1.2.3.4 -c config.yaml
```
