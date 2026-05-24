---
layout: home
title: Home
nav_order: 1
---

<div style="text-align:center; padding: 2rem 0 1.5rem;">
  <img src="/assets/images/infraguard_logo.svg" alt="InfraGuard" style="max-width:480px; width:100%;" />
</div>

Smart ASGI redirector for red team C2, phishing, and payload delivery infrastructure. Runs in front of any C2 or phishing server — validates inbound traffic, blocks scanners and sandboxes, and presents cover content to unwanted visitors.

> **Authorized use only.** InfraGuard is a red team tool. Deploy only in engagements and lab environments you are authorized to operate in.

## What InfraGuard Does

- **Redirects** — proxies legitimate beacon/target traffic to your C2 or phishing backend
- **Filters** — blocks scanners, sandboxes, analysts, and threat intel crawlers before they reach the backend
- **Covers** — serves believable decoy content to anyone who fails filtering
- **Tracks** — records every request with filter result and score for post-op review
- **Alerts** — dispatches real-time events to Discord, Slack, or syslog via plugins

## Supported Backends

| Category | Frameworks |
|---|---|
| C2 | Cobalt Strike, Mythic, Brute Ratel C4, Sliver, Havoc, Nighthawk, PoshC2 |
| Phishing | GoPhish, Evilginx, CuddlePhish, Phishing.club |
| Payload delivery | Mythic file store, PwnDrop, local filesystem, HTTP proxy (RedFile, nginx) |

## Quick Links

- [Installation](./getting-started/installation)
- [Quickstart](./getting-started/quickstart)
- [CLI Reference](./cli/)
- [Architecture](./architecture/overview)
