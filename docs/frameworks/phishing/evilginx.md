---
layout: default
title: Evilginx
parent: Phishing Frameworks
grand_parent: Frameworks
nav_order: 2
---

# Evilginx

Two operating modes: with a phishlet file (path-aware filtering) or without (full passthrough with campaign token gating).

## Config

```yaml
domains:
  login.example.com:
    upstream: "${EVILGINX_UPSTREAM}"
    profile_type: "evilginx"
    # profile_path: "/config/wordpress.yaml"

    campaign_token:
      enabled: true
      token_param: "t"
      tokens:
        - "${CAMPAIGN_TOKEN_Q1}"
      score_on_missing: 0.9

    drop_action:
      type: "proxy"
      target: "https://login.microsoftonline.com"
```

See `config/examples/phishing-evilginx.yaml`.

## Drop Action: `proxy`

`proxy` type silently fetches the target and returns its content — analysts see a real Microsoft login page, not a redirect.

## Recommended Pipeline Settings

```yaml
pipeline:
  enable_replay_filter: false     # OAuth flows are multi-step
  enable_sandbox_filter: true     # blocks Safe Links, Defender ATP
  block_score_threshold: 0.65
```
