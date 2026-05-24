---
layout: default
title: CLI Reference
nav_order: 6
has_children: false
---

# CLI Reference

InfraGuard ships a Click-based CLI. All commands accept `-c / --config <path>` to specify the config file.

## Top-Level Commands

```
infraguard --help
infraguard --version

infraguard run         Start the redirector
infraguard config      Config management subcommands
infraguard token       Token management subcommands
infraguard api         Query the management API
infraguard profile     C2 profile utilities
```

---

## `infraguard run`

```bash
infraguard run --config config/config.yaml
infraguard run -c config/config.yaml --log-level DEBUG
```

| Flag | Default | Description |
|---|---|---|
| `-c / --config` | `config.yaml` | Path to config file |
| `--log-level` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `--reload` | off | Enable hot reload on config file change |

---

## `infraguard config`

All mutating commands write a `.bak` backup before modifying.

### `config show`

```bash
infraguard config show -c config.yaml
infraguard config show -c config.yaml --section pipeline
```

### `config set`

```bash
infraguard config set pipeline.block_score_threshold 0.65 -c config.yaml
infraguard config set logging.level DEBUG -c config.yaml
```

---

## `infraguard config domain`

```bash
infraguard config domain list -c config.yaml
infraguard config domain add phish.example.com -c config.yaml
infraguard config domain remove phish.example.com -c config.yaml
infraguard config domain set-upstream cdn.example.com https://10.0.0.1:443 -c config.yaml
infraguard config domain set-drop cdn.example.com redirect https://jquery.com -c config.yaml
infraguard config domain add-route cdn.example.com \
  --path "/assets/update.js" \
  --backend-type mythic_file \
  --backend-target "https://10.0.0.1:7443" \
  --require-beacon-ip --require-token \
  --rate-limit 1 3600 -c config.yaml
infraguard config domain remove-route cdn.example.com "/assets/update.js" -c config.yaml
infraguard config domain list-routes cdn.example.com -c config.yaml
```

---

## `infraguard config intel`

```bash
infraguard config intel show -c config.yaml
infraguard config intel block-country RU -c config.yaml
infraguard config intel unblock-country RU -c config.yaml
infraguard config intel block-asn 15169 -c config.yaml
infraguard config intel block-ip 1.2.3.4 -c config.yaml
```

---

## `infraguard config pipeline`

```bash
infraguard config pipeline show -c config.yaml
infraguard config pipeline enable sandbox_filter -c config.yaml
infraguard config pipeline disable replay_filter -c config.yaml
infraguard config pipeline set-threshold 0.65 -c config.yaml
infraguard config pipeline ja3 block e7d705a3286e19ea42f587b344ee6865 -c config.yaml
infraguard config pipeline ja3 unblock e7d705a3286e19ea42f587b344ee6865 -c config.yaml
infraguard config pipeline ja3 list -c config.yaml
```

---

## `infraguard token`

```bash
infraguard token list -c config.yaml
infraguard token revoke <token-hex> -c config.yaml
infraguard token issue 10.0.0.5 -c config.yaml
infraguard token generate --secret $HMAC_SECRET --ttl 604800
```

---

## `infraguard api`

```bash
infraguard api requests -c config.yaml
infraguard api requests --limit 50 --domain cdn.example.com -c config.yaml
infraguard api requests --blocked-only -c config.yaml
infraguard api whitelist -c config.yaml
infraguard api whitelist add 10.0.0.5 -c config.yaml
infraguard api blocklist add 1.2.3.4 -c config.yaml
infraguard api burns -c config.yaml
```

---

## `infraguard profile`

```bash
infraguard profile parse --type cobalt_strike profiles/my.profile
infraguard profile parse --type nighthawk profiles/nighthawk.json
infraguard profile validate --type cobalt_strike profiles/my.profile \
  --method GET --path "/jquery-3.7.1.min.js"
```
