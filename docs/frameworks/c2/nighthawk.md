---
layout: default
title: Nighthawk
parent: C2 Frameworks
grand_parent: Frameworks
nav_order: 6
---

# Nighthawk

InfraGuard parses Nighthawk's listener JSON to extract HTTP routes and implant metadata configuration.

## Config

```yaml
domains:
  telemetry.example.com:
    upstream: "${NIGHTHAWK_UPSTREAM}"
    profile_path: "profiles/nighthawk-listener.json"
    profile_type: "nighthawk"

    drop_action:
      type: "redirect"
      target: "https://telemetry.example.com"
```

See `config/examples/c2-nighthawk.yaml`.

## Recommended Pipeline Settings

```yaml
pipeline:
  filter_mode: "strict"
  block_score_threshold: 0.5
  enable_profile_filter: true
  enable_replay_filter: true
  replay_persist: true
  enumeration_unique_path_threshold: 3
```
