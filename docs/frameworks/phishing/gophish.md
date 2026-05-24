---
layout: default
title: GoPhish
parent: Phishing Frameworks
grand_parent: Frameworks
nav_order: 1
---

# GoPhish

No profile file required — InfraGuard uses built-in GoPhish path patterns (`/track/*`, `/report`, `/static/*`, `/`).

## Config

```yaml
domains:
  phish.example.com:
    upstream: "${GOPHISH_UPSTREAM}"
    profile_type: "gophish"

    campaign_token:
      enabled: true
      token_param: "t"
      tokens:
        - "${CAMPAIGN_TOKEN_Q1}"
        - "${CAMPAIGN_TOKEN_Q2}"
      score_on_missing: 0.8

    drop_action:
      type: "redirect"
      target: "https://example.com"
```

See `config/examples/phishing-gophish.yaml`.

## Campaign Tokens

Embed in GoPhish email template URL:

```
https://phish.example.com/?t={{.Token}}&rid={{.RId}}
```

## Recommended Pipeline Settings

```yaml
pipeline:
  filter_mode: "scoring"
  block_score_threshold: 0.7
  enable_replay_filter: false    # targets click once — replay breaks this
  enable_sandbox_filter: true    # blocks Safe Links
  enumeration_unique_path_threshold: 15
```
