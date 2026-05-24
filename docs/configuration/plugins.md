---
layout: default
title: Plugins & Alerting
parent: Configuration
nav_order: 5
---

# Plugins & Alerting

```yaml
plugins:
  - infraguard.plugins.builtin.discord
  - infraguard.plugins.builtin.slack

plugin_settings:
  discord:
    enabled: true
    event_filter:
      only_blocked: false
      min_score: 0.5
    options:
      webhook_url: "${DISCORD_WEBHOOK_URL}"
      username: "InfraGuard"

  slack:
    enabled: true
    event_filter:
      only_blocked: true
      min_score: 0.7
    options:
      webhook_url: "${SLACK_WEBHOOK_URL}"
      channel: "#red-team-alerts"
```

## Built-in Plugins

| Plugin | Module |
|---|---|
| Discord | `infraguard.plugins.builtin.discord` |
| Slack | `infraguard.plugins.builtin.slack` |
| Syslog | `infraguard.plugins.builtin.syslog` |

## Syslog

```yaml
plugins:
  - infraguard.plugins.builtin.syslog

plugin_settings:
  syslog:
    enabled: true
    options:
      host: "siem.internal"
      port: 514
      protocol: "udp"
      facility: "local0"
```

## Event Filter

| Setting | Effect |
|---|---|
| `only_blocked: true` | Alert only on blocked requests |
| `only_blocked: false` + `min_score: 0.5` | Alert on blocked, suspected, phishing.club captures, burn indicators |

## Custom Plugins

```python
from infraguard.plugins.base import InfraGuardPlugin, RequestEvent

class MyPlugin(InfraGuardPlugin):
    async def on_event(self, event: RequestEvent) -> None:
        await self.send_somewhere(event)
```

Register:

```yaml
plugins:
  - mypackage.myplugin.MyPlugin
```
