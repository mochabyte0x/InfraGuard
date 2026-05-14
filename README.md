![InfraGuard Logo](/images/infraguard_logo.svg)

Red team infrastructure tracker and C2 redirector -- a modern alternative to [RedWarden](https://github.com/mgeeky/RedWarden).

InfraGuard sits between the internet and your C2 teamserver, validating every inbound request against your malleable C2 profile and blocking anything that doesn't conform. Scanners, bots, and blue team probes get redirected to a decoy site while legitimate beacon traffic passes through to your teamserver.

![Mythic Callbacks Xenon](/images/xenon_callback.png)
![InfraGuard Dashboard](/images/infraguard_dashboard.png)

## Architecture

![Architecture Diagram](/images/InfraGuard%20Infrastructure%20Diagram.drawio.png)

## Features

- **Multi-domain proxying** -- proxy multiple domains simultaneously, each with independent C2 profiles, upstreams, and rules
- **C2 profile validation** -- parse and enforce Cobalt Strike, Mythic, Brute Ratel C4, Sliver, Havoc, Nighthawk, and PoshC2 profiles as redirector rules
- **Multi-protocol listeners** -- HTTP/HTTPS, DNS, MQTT, and WebSocket listeners running simultaneously with shared IP intelligence and event tracking
- **Scoring-based filter pipeline** -- 10 filters (JA3, IP, bot, header, DNS, geo, profile, replay, enumeration, sandbox) each contribute a 0.0-1.0 score; configurable threshold determines block/allow
- **JA3 TLS fingerprint filtering** -- block Masscan, ZGrab2, Shodan, curl, Python requests, and Nmap at the TLS handshake layer before any HTTP data is exchanged; works via reverse-proxy header (nginx `ssl_fingerprint`, HAProxy native JA3) or custom asyncio protocol; optional allowlist mode enforces beacon JA3
- **Sandbox / headless browser detection** -- score-accumulation model across HTTP signals: HeadlessChrome UA, missing Accept-Language, Chrome without sec-ch-ua, Safe Links / msnbot scanner UAs, non-browser Accept ordering; blocks Microsoft Safe Links, Cuckoo, ANY.RUN, and VirusTotal URL scanners
- **Path enumeration detection** -- per-IP unique URI tracking in a sliding window; hard-blocks dirbuster/ffuf/gobuster before they map URI space; configurable block and suspect thresholds
- **DNS subdomain enumeration detection** -- tracks NXDOMAIN responses per client IP; immediately adds the source IP to the blocklist on threshold breach; blocks Amass, subfinder, dnsrecon at the DNS listener
- **Anti-bot / anti-crawling** -- 40+ known scanner/bot User-Agent patterns, header anomaly detection
- **IP intelligence** -- built-in CIDR blocklists for 19 security vendor ranges (Shodan, Censys, Rapid7, etc.), GeoIP filtering, reverse DNS keyword matching
- **Threat intel feeds** -- auto-update blocklists from public sources (abuse.ch, Emerging Threats, Spamhaus DROP, Binary Defense) with configurable refresh interval and disk caching
- **Rule ingestion** -- import IP blocklists and User-Agent patterns from existing `.htaccess` and `robots.txt` files
- **Dynamic IP blocking** -- block IPs outside whitelisted ranges; auto-whitelist IPs after N valid C2 requests
- **Whitelist enrichment** -- whitelisted CIDRs are auto-enriched with ASN, organization, country, and continent data on startup via GeoIP databases
- **Burn detection** -- Certificate Transparency log monitoring (crt.sh polling), domain reputation self-monitoring (URLhaus, OpenPhish, Google Safe Browsing), and cross-domain analyst detection (single IP accessing multiple operator domains); all fire burn alerts through existing webhook plugins
- **Content delivery routes** -- serve payloads, decoys, and static files at specific paths via PwnDrop, Mythic file store, local filesystem, or HTTP proxy backends; optional conditional delivery (real content to targets, decoys to scanners)
- **Mythic file staging** -- `mythic_file` backend proxies Mythic's `/direct/download/{uuid}` at clean URLs; fixed UUID (URL aliasing) or proxy mode (UUID from path); access control provided entirely by InfraGuard's filter stack
- **One-time payload tokens** -- tokens issued automatically when a beacon is dynamically whitelisted; atomic single-use SQLite enforcement prevents URL replay by analysts or sandboxes; configurable TTL and max-use count
- **Per-route rate limiting** -- sliding-window per-IP download rate limiter on content routes; exceeding the limit serves the configured scanner decoy or 429
- **Delivery guards** -- environment keying for content routes: require beacon IP (dynamic whitelist), UA allowlist (regex), required header values (implant-specific headers), forbidden headers (Via, X-Forwarded-For, CF-Worker); failed checks serve domain drop action, not a raw 403
- **Phishing campaign tokens** -- gate phishing pages behind per-campaign tokens embedded in email links; static token list or HMAC-signed self-validating tokens with configurable TTL; analysts who find the URL via CT logs or threat feeds cannot load the page
- **Replay protection** -- reject duplicate requests by content hash; hashes persisted to SQLite so protection survives restarts
- **Drop actions** -- redirect, TCP reset, proxy to decoy site, or tarpit (slow-drip response to waste scanner time)
- **Web dashboard** -- real-time SPA with login page, live request feed, domain stats, top blocked IPs, authenticated WebSocket event streaming, and inline block/whitelist/unblock actions
- **Command Post** -- multi-instance aggregation dashboard that merges stats, requests, and live events from multiple InfraGuard nodes into a single view
- **Terminal UI** -- Textual-based TUI with login screen, live API polling, color-coded request log
- **SIEM integration** -- built-in plugins for Elasticsearch, Wazuh, and Syslog (CEF/JSON) with batched forwarding
- **Webhook alerts** -- built-in plugins for Discord (embeds), Slack (Block Kit), and generic webhook (Rocket.Chat, Mattermost, Teams); burn detection alerts route through the same plugin system
- **Plugin system** -- event-driven architecture with `on_event` hooks, per-plugin config, event filtering (only_blocked, min_score, domain include/exclude)
- **Backend config generation** -- generate Nginx, Caddy, or Apache configs with full operator customization (TLS, IP filtering, header checks, aliases, custom headers)
- **Edge proxies** -- lightweight Cloudflare Worker and AWS Lambda for domain fronting through CDN infrastructure, edge country blocking, and host rewriting
- **Docker deployment** -- Dockerfile + docker-compose with optional Let's Encrypt, GeoIP downloader, and PwnDrop payload server
- **GeoIP support** -- all three GeoLite2 databases (City, ASN, Country) with Docker auto-download; whitelisted CIDRs auto-enriched on startup
- **Self-signed TLS fallback** -- auto-generates certificates when configured paths don't exist
- **Environment variable support** -- `.env` file auto-loaded; `${VAR}` syntax works in all config values and keys
- **Configurable health endpoint** -- change the health check path to avoid fingerprinting
- **Structured logging** -- JSON-formatted structured logs via structlog
- **Tracking & persistence** -- SQLite with WAL mode for request logging, statistics, node registry, replay hashes, and payload tokens

## Installation Guide

Check out the [Wiki Page](https://github.com/Whispergate/InfraGuard/wiki/03.-Installation) for installation

## CLI Reference

```
infraguard --version                                Show version
infraguard --help                                   Show help

infraguard run -c config.yaml                       Start the reverse proxy
infraguard run -c config.yaml --port 8443           Override listen port
infraguard run -c config.yaml --host 0.0.0.0        Override bind address

infraguard dashboard -c config.yaml                 Start the web dashboard
infraguard dashboard -c config.yaml --port 9090     Override dashboard port

infraguard tui                                      Launch TUI with login screen
infraguard tui --url http://host:8080 --token TOK   Auto-connect to dashboard
infraguard tui -c config.yaml                       Read URL/token from config

infraguard command-post -c command-post.yaml         Start multi-instance dashboard
infraguard command-post --instance name:url:token    Add instance via CLI (repeatable)

infraguard profile parse <file>                     Parse and display a C2 profile
infraguard profile parse <file> --format json        Output as JSON
infraguard profile parse <file> --type brute_ratel   Force profile type
infraguard profile convert <file> -o out.json        Convert profile to JSON

# Supported --type values: auto, cobalt_strike, mythic, brute_ratel, sliver, havoc, nighthawk, poshc2
# Auto-detection: .profile = CS, .toml = Havoc, .yaml = PoshC2, .json = auto-detect by keys

infraguard ingest <files...>                         Ingest .htaccess/robots.txt rules
infraguard ingest <files...> --format blocklist      Output as IP blocklist
infraguard ingest <files...> --format json           Output as JSON
infraguard ingest <files...> -o banned_ips.txt       Write blocklist to file

infraguard generate nginx -c config.yaml             Generate Nginx config
infraguard generate caddy -c config.yaml             Generate Caddyfile
infraguard generate apache -c config.yaml            Generate Apache VirtualHost

infraguard init -o config.yaml                       Generate starter config
infraguard validate -c config.yaml                   Validate config file
```

### Generator options

The `generate` command accepts additional flags for operator customization:

| Flag | Description |
|---|---|
| `--listen-port PORT` | Override listen port (default: from config) |
| `--ssl-cert PATH` | Override SSL certificate path |
| `--ssl-key PATH` | Override SSL key path |
| `--redirect-url URL` | Override redirect URL for blocked requests |
| `--default-action redirect\|404` | Action for non-matching requests |
| `--no-ip-filter` | Omit IP allow/deny blocks |
| `--no-header-check` | Omit header validation rules |
| `--alias DOMAIN:ALIAS` | Add server name alias (repeatable) |
| `--header NAME:VALUE` | Add custom response header (repeatable) |

## Command Post (Multi-Instance Dashboard)

When running multiple InfraGuard instances across different VPSes or cloud providers, the Command Post aggregates stats, requests, and live events from all nodes into a single dashboard.

```
┌─────────────────────────────┐
│    Command Post Dashboard   │
│    http://localhost:9090    │
└──────────┬──────────────────┘
           │ parallel fetch
     ┌─────┼──────┬──────────┐
     ▼     ▼      ▼          ▼
   IG-1   IG-2   IG-3   ... IG-N
```

![InfraGuard Command Post](/images/infraguard_command_post.png)

### Quick start

```bash
# Via config file
infraguard command-post -c config/command-post.yaml

# Via CLI args
infraguard command-post \
  --instance "prod:https://ig1.example.com:8080:TOKEN1" \
  --instance "staging:https://ig2.example.com:8080:TOKEN2" \
  --port 9090

# Via Docker
docker compose --profile command-post up -d command-post
```

### Configuration

Create `config/command-post.yaml`:

```yaml
instances:
  - name: "prod-cs"
    url: "https://ig1.example.com:8080"
    token: "${IG_PROD_TOKEN}"
  - name: "prod-mythic"
    url: "https://ig2.example.com:8080"
    token: "${IG_MYTHIC_TOKEN}"
  - name: "staging"
    url: "https://ig3.example.com:8080"
    token: "${IG_STAGING_TOKEN}"

port: 9090
# auth_token: "${COMMAND_POST_TOKEN}"
```

### What it shows

- **Merged stats** -- total requests, allowed, blocked summed across all instances
- **Instance health bar** -- green/red status for each connected node
- **Interleaved request log** -- requests from all instances sorted by timestamp, each tagged with its instance name
- **Merged top blocked IPs** -- aggregated across all instances
- **Per-domain stats** -- domains from all instances with recalculated block rates
- **Live event feed** -- multiplexed WebSocket events from all nodes
- **Block/whitelist actions** -- fan out to all instances or a specific one

### API endpoints

| Endpoint | Method | Description |
|---|---|---|
| `/api/instances` | GET | List all instances with health status |
| `/api/stats` | GET | Merged stats from all instances |
| `/api/requests` | GET | Interleaved request log from all instances |
| `/api/intel/whitelist` | POST | Whitelist an IP on all instances |
| `/api/intel/blocklist` | POST | Block an IP on all instances |
| `/api/intel/blocklist` | DELETE | Unblock an IP on all instances |
| `/ws/events` | WS | Multiplexed live events from all instances |

## Docker Deployment

### Quick start

```bash
cp .env.example .env
# Edit .env with your domain, teamserver, and token
docker compose up -d
```

This starts two services:
- **proxy** -- the redirector on ports 443 and 80
- **dashboard** -- the web UI on port 8080

### With Let's Encrypt

```bash
# Set in .env:
#   INFRAGUARD_LETSENCRYPT=true
#   INFRAGUARD_DOMAIN=cdn.example.com
#   INFRAGUARD_DOMAIN_EMAIL=operator@example.com

# Obtain the initial certificate
docker compose --profile letsencrypt up certbot

# Start the proxy (will use the LE cert)
docker compose up -d proxy dashboard

# Start auto-renewal (checks every 12 hours)
docker compose --profile letsencrypt up -d certbot-renew
```

Requirements for Let's Encrypt:
- Port 80 must be reachable from the internet
- `INFRAGUARD_DOMAIN` must resolve to this host's public IP
- `INFRAGUARD_DOMAIN_EMAIL` must be a valid email address

### With GeoIP databases

```bash
# Download all three GeoLite2 databases (City, ASN, Country)
docker compose --profile geoip up geoip-update

# Then start normally - databases are mounted at /app/geoip/
docker compose up -d proxy dashboard
```

### With PwnDrop (payload delivery)

```bash
# Start PwnDrop alongside the proxy
docker compose --profile pwndrop up -d pwndrop

# Access PwnDrop admin UI at https://localhost:8443
# InfraGuard reaches it internally at http://pwndrop:80
```

Then configure content routes in your config to proxy payload paths to PwnDrop:

```yaml
domains:
  cdn.example.com:
    content_routes:
      - path: "/downloads/*"
        backend:
          type: "pwndrop"
          target: "http://pwndrop:80"
          auth_token: "${PWNDROP_TOKEN}"
```

### Scaling

```bash
# Run multiple redirector nodes
docker compose up -d --scale proxy-node=3
```

Uncomment the `proxy-node` service in `docker-compose.yml` to enable.

### Volumes

| Volume | Purpose |
|---|---|
| `./config` | Configuration files (mounted read-only) |
| `./examples` | C2 profiles (mounted read-only) |
| `./rules` | Ingested blocklists and rule source files (mounted read-only) |
| `./data` | SQLite database (persisted) |
| `certs` | TLS certificates (shared between proxy and certbot) |
| `geoip` | GeoLite2 databases (populated by `geoip-update` service) |
| `pwndrop-data` | PwnDrop uploaded files and database |

## Architecture

```
infraguard/
    __init__.py              Package init
    __main__.py              python -m infraguard entry
    main.py                  Click CLI
    config/                  YAML config loading, .env support, Pydantic validation
    core/                    ASGI proxy engine (app, proxy, router, TLS, drop actions, content delivery)
    profiles/                C2 profile parsers (Cobalt Strike, Mythic, Brute Ratel, Sliver, Havoc, Nighthawk, PoshC2)
    pipeline/                Request validation filters (JA3, IP, bot, header, DNS, geo, profile, replay, enumeration, sandbox)
    intel/                   IP intelligence (blocklists, GeoIP, rDNS, feeds, rule ingestion)
    tracking/                SQLite persistence (request logging, stats, node registry)
    plugins/                 Plugin system (protocol, loader, builtins)
    ui/
        api/                 REST API + WebSocket (Starlette)
        web/                 SPA dashboard (HTML/JS/CSS)
        tui/                 Terminal UI (Textual) with login screen
        command_post/        Multi-instance aggregation dashboard
    listeners/               Protocol listeners (HTTP, DNS, MQTT, WebSocket)
    backends/                Config generators (Nginx, Caddy, Apache)
    models/                  Shared types and event models
```

## Comparison with RedWarden

| Feature | RedWarden | InfraGuard |
|---|---|---|
| Architecture | Single ~99KB file | Modular package |
| Profile parsing | Regex state machine | Structured parser with full block/transform support |
| C2 support | Cobalt Strike only | Cobalt Strike, Mythic, Brute Ratel C4, Sliver, Havoc, Nighthawk, PoshC2 |
| Protocols | HTTP only | HTTP, DNS, MQTT, WebSocket |
| Filter model | Binary pass/fail | Scoring-based (0.0-1.0 threshold), 10-filter chain |
| TLS fingerprinting | None | JA3 blocking (Masscan, ZGrab2, Shodan, curl, Python requests, Nmap) |
| Sandbox detection | None | Headless browser / Safe Links / sandbox UA and header scoring |
| Enumeration detection | None | Path enumeration + DNS NXDOMAIN tracking with auto-block |
| Burn detection | None | CT log monitoring, domain reputation (URLhaus/OpenPhish/GSB), cross-domain analyst detection |
| Payload delivery | None | PwnDrop, Mythic file store, filesystem, HTTP proxy with conditional delivery |
| Payload protection | None | One-time tokens, per-route rate limiting, delivery guards (environment keying) |
| Phishing protection | None | Campaign token validation (static list or HMAC-signed) |
| Operator UI | None | Web dashboard + Terminal UI + multi-instance Command Post |
| Config generation | None | Nginx, Caddy, Apache with full customization |
| Rule ingestion | None | .htaccess + robots.txt parser |
| Threat intel feeds | None | Auto-update from 5 public sources |
| Plugin system | Basic 4-method interface | Event-driven with on_event hooks + per-plugin config |
| SIEM integration | None | Elasticsearch, Wazuh, Syslog (CEF/JSON) |
| Webhook alerts | None | Discord, Slack, generic webhook (burn alerts route through same plugins) |
| Whitelist intelligence | None | Auto-enrich CIDRs with ASN/org/country on startup |
| Anti-replay | SQLite hash | Persistent SQLite with in-memory L1 cache, survives restarts |
| Drop actions | redirect, reset, proxy | redirect, reset, proxy, tarpit |
| TLS management | Manual only | Auto self-signed + Let's Encrypt integration |
| Edge deployment | None | Cloudflare Worker + AWS Lambda edge proxies with domain fronting |
| Deployment | Manual | Docker Compose with health checks |
| Logging | Custom colored output | Structured JSON (structlog) |
| Async | Tornado callbacks | Native async/await (ASGI + uvicorn) |

## Contributions

- Mgeeky - Original Idea ([RedWarden](https://github.com/mgeeky/RedWarden))
- curi0usJack - [.htaccess rules](https://gist.github.com/curi0usJack/971385e8334e189d93a6cb4671238b10)
- Profiles
  - threatexpress - [jquery-c2.3.14.profile](https://github.com/threatexpress/malleable-c2/blob/master/jquery-c2.3.14.profile)
  - InfinityCurve - [Havoc Profile](/examples/kaine.toml)
- C2 Frameworks
  - [Cobalt Strike](https://www.cobaltstrike.com/) - Malleable C2 profile support
  - [Mythic](https://github.com/its-a-feature/Mythic) - HTTPX profile support + file staging
  - [Brute Ratel C4](https://bruteratel.com/) - Server config profile support
  - [Sliver](https://github.com/BishopFox/sliver) - HTTP C2 profile support
  - [Havoc](https://www.infinitycurve.org/) - TOML profile support
  - [Nighthawk](https://nighthawkc2.io/) - JSON listener config support
  - [PoshC2](https://github.com/nettitude/PoshC2) - YAML config support

If you would like to contribute to the project, then please create a new branch with the version name and specify the same version name in the pull request. E.g. branch=v1.2.3 | [v1.2.3] Added blah item.

## License

BSD 2-Clause License. See [LICENSE](LICENSE) for details.

Copyright (c) 2026, Whispergate
