---
layout: default
title: Sliver
parent: C2 Frameworks
grand_parent: Frameworks
nav_order: 4
---

# Sliver

InfraGuard parses Sliver's HTTP C2 config YAML to extract URI paths and headers.

## Config

```yaml
domains:
  api.example.com:
    upstream: "${SLIVER_UPSTREAM}"
    profile_path: "profiles/sliver-http.yaml"
    profile_type: "sliver"

    drop_action:
      type: "redirect"
      target: "https://api.example.com/docs"
```

See `config/examples/c2-sliver.yaml`.

## Recommended Pipeline Settings

```yaml
pipeline:
  filter_mode: "scoring"
  block_score_threshold: 0.65
  enable_profile_filter: true
  enable_replay_filter: true
  replay_persist: true
  enable_sandbox_filter: true
```
