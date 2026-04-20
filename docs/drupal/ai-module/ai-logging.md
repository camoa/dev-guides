---
description: AI Logging — deprecated entity-based request logging for development debugging only
tldr: "**Status: DEPRECATED** — use [AI Observability](ai-observability.md) for production monitoring. `ai_logging` is development/debugging only and stores AI requests as `ai_log` entities in the database."
drupal_version: "11.x"
---

# AI Logging

## When to Use

> **Status: DEPRECATED** — use [AI Observability](ai-observability.md) for production monitoring. `ai_logging` is development/debugging only and stores AI requests as `ai_log` entities in the database.

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Production monitoring | `ai_observability` | PSR-3 logger; no DB overhead |
| Local debugging | `ai_logging` (caution) | Easy to browse but deprecated; DB-heavy |

## Config: `ai_logging.settings`

| Key | Default | Description |
|-----|---------|-------------|
| `prompt_logging` | `false` | Master switch |
| `prompt_logging_output` | -- | Also log responses |
| `prompt_logging_tags` | `''` | Include tags (comma-separated) |
| `prompt_logging_excluded_tags` | -- | Exclude tags |
| `prompt_logging_max_messages` | `1000` | Max stored logs |
| `prompt_logging_max_age` | `30` | Max age in days |

## Permission

- `view ai log` — required to view log entries

## Common Mistakes

- **Wrong**: Enabling `ai_logging` on production → **Right**: Stores entities in DB; performance impact at scale; use `ai_observability` instead
- **Wrong**: Relying on `ai_logging` for long-term → **Right**: Module is deprecated; migrate to `ai_observability`

## See Also

- [AI Observability](ai-observability.md) — use this instead
- Reference: `web/modules/contrib/ai/modules/ai_logging/`
