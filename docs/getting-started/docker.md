---
layout: default
title: Docker Compose
parent: Getting Started
nav_order: 3
---

# Docker Compose

## Minimal `docker-compose.yml`

```yaml
services:
  infraguard:
    image: ghcr.io/whispergate/infraguard:latest
    restart: unless-stopped
    ports:
      - "443:443"
    volumes:
      - ./config:/config:ro
      - ./certs:/certs:ro
      - infraguard-data:/data
    env_file: .env
    environment:
      INFRAGUARD_CONFIG: /config/config.yaml

volumes:
  infraguard-data:
```

## `.env` File

```bash
INFRAGUARD_TLS_CERT=/certs/fullchain.pem
INFRAGUARD_TLS_KEY=/certs/privkey.pem
INFRAGUARD_DB_PATH=/data/infraguard.db
CS_UPSTREAM=https://10.0.0.1:443
MYTHIC_IP=10.0.0.2
DISCORD_WEBHOOK_URL=https://discord.com/api/webhooks/...
```

## Hot Reload

```bash
docker compose kill -s HUP infraguard
```

Config reloads without dropping connections. DB and whitelist preserved.

## API Port

```yaml
ports:
  - "443:443"
  - "127.0.0.1:8080:8080"   # management API — do NOT expose publicly
```
