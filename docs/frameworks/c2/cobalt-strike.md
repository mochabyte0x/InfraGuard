---
layout: default
title: Cobalt Strike
parent: C2 Frameworks
grand_parent: Frameworks
nav_order: 1
---

# Cobalt Strike

InfraGuard parses Malleable C2 profiles to extract URI patterns, HTTP methods, required headers, and message locations.

## Config

```yaml
domains:
  cdn.example.com:
    upstream: "${CS_UPSTREAM}"
    profile_path: "profiles/jquery.profile"
    profile_type: "cobalt_strike"

    drop_action:
      type: "redirect"
      target: "https://jquery.com"
```

See `config/examples/c2-cobalt-strike.yaml`.

## Profile Parsing

InfraGuard extracts all URI patterns from `http-get`, `http-post`, and staging blocks. Required headers from `metadata`/`id` blocks are enforced — requests missing them fail profile validation.

## Recommended Pipeline Settings

```yaml
pipeline:
  filter_mode: "strict"
  block_score_threshold: 0.6
  enable_profile_filter: true
  enable_replay_filter: true
  replay_persist: true
  enable_sandbox_filter: true
  enable_enumeration_filter: true
  enumeration_unique_path_threshold: 5
```
