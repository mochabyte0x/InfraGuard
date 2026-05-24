---
layout: default
title: Havoc
parent: C2 Frameworks
grand_parent: Frameworks
nav_order: 5
---

# Havoc

InfraGuard parses Havoc's listener YAML to extract HTTP patterns and headers for the Demon agent.

## Config

```yaml
domains:
  support.example.com:
    upstream: "${HAVOC_UPSTREAM}"
    profile_path: "profiles/havoc-listener.yaml"
    profile_type: "havoc"

    drop_action:
      type: "redirect"
      target: "https://support.example.com/help"
```

See `config/examples/c2-havoc.yaml`.

## Recommended Pipeline Settings

```yaml
pipeline:
  filter_mode: "scoring"
  block_score_threshold: 0.65
  enable_profile_filter: true
  enable_sandbox_filter: true
  enable_enumeration_filter: true
```
