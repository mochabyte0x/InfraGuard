---
layout: default
title: Brute Ratel C4
parent: C2 Frameworks
grand_parent: Frameworks
nav_order: 3
---

# Brute Ratel C4

InfraGuard parses BRC4's listener configuration JSON to extract HTTP patterns and headers.

## Config

```yaml
domains:
  updates.example.com:
    upstream: "${BRC4_UPSTREAM}"
    profile_path: "profiles/brc4-listener.json"
    profile_type: "brute_ratel"

    drop_action:
      type: "redirect"
      target: "https://windowsupdate.microsoft.com"
```

See `config/examples/c2-brute-ratel.yaml`.

## Recommended Pipeline Settings

```yaml
pipeline:
  filter_mode: "strict"
  block_score_threshold: 0.6
  enable_profile_filter: true
  enable_sandbox_filter: true
  enumeration_unique_path_threshold: 5
```
