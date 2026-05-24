---
layout: default
title: Installation
parent: Getting Started
nav_order: 1
---

# Installation

## Requirements

- Python 3.11+
- Docker + Docker Compose (recommended)
- A valid TLS certificate

## Docker (Recommended)

```bash
git clone https://github.com/Whispergate/InfraGuard
cd InfraGuard
cp config/examples/c2-cobalt-strike.yaml config/config.yaml
# Edit config/config.yaml
docker compose up -d
```

## pip / virtualenv

```bash
git clone https://github.com/Whispergate/InfraGuard
cd InfraGuard
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e .
infraguard --help
```

## Environment Variables

InfraGuard uses env-var interpolation in YAML configs (`${VAR}`):

```bash
export INFRAGUARD_TLS_CERT=/certs/fullchain.pem
export INFRAGUARD_TLS_KEY=/certs/privkey.pem
export INFRAGUARD_DB_PATH=/data/infraguard.db
export CS_UPSTREAM=https://10.10.10.10:443
```

## TLS Certificates

```yaml
listeners:
  - protocol: "https"
    bind: "0.0.0.0"
    port: 443
    tls:
      cert: "${INFRAGUARD_TLS_CERT}"
      key: "${INFRAGUARD_TLS_KEY}"
```

## Verify

```bash
infraguard --version
infraguard config show --config config/config.yaml
```
