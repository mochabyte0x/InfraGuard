---
layout: default
title: PoshC2
parent: C2 Frameworks
grand_parent: Frameworks
nav_order: 7
---

# PoshC2

InfraGuard parses PoshC2's YAML config to extract GET/POST request patterns and User-Agent.

## Config

```yaml
domains:
  office.example.com:
    upstream: "${POSHC2_UPSTREAM}"
    profile_path: "profiles/poshc2-config.yaml"
    profile_type: "poshc2"

    drop_action:
      type: "redirect"
      target: "https://office.com"
```

See `config/examples/c2-poshc2.yaml`.

## Recommended Pipeline Settings

```yaml
pipeline:
  filter_mode: "scoring"
  block_score_threshold: 0.65
  enable_profile_filter: true
  enable_bot_filter: true
  enable_sandbox_filter: true
```
