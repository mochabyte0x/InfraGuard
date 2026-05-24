---
layout: default
title: CuddlePhish
parent: Phishing Frameworks
grand_parent: Frameworks
nav_order: 3
---

# CuddlePhish

OAuth/device-code phishing framework. Captures MFA-protected tokens from Microsoft and Google accounts.

## Config

```yaml
domains:
  auth.example.com:
    upstream: "${CUDDLEPHISH_UPSTREAM}"
    profile_type: "cuddlephish"

    campaign_token:
      enabled: true
      token_param: "t"
      tokens:
        - "${CAMPAIGN_TOKEN}"
      score_on_missing: 0.9

    drop_action:
      type: "redirect"
      target: "https://login.microsoftonline.com"
```

See `config/examples/phishing-cuddlephish.yaml`.

## Recommended Pipeline Settings

```yaml
pipeline:
  enable_replay_filter: false     # OAuth flows are multi-step
  enable_sandbox_filter: true     # CRITICAL — blocks Safe Links, Defender ATP
  block_score_threshold: 0.65
```

`enable_sandbox_filter: true` is critical — Microsoft's sandbox exhausts device-code TTLs and flags URLs.
