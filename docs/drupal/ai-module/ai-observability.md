---
description: AI Observability — production monitoring for AI provider calls via PSR-3 logger and OpenTelemetry
tldr: "Use `ai_observability` for production monitoring and audit trails. Use [AI Logging](ai-logging.md) only for local development debugging (it is deprecated)."
drupal_version: "11.x"
---

# AI Observability

## When to Use

> Use `ai_observability` for production monitoring and audit trails. Use [AI Logging](ai-logging.md) only for local development debugging (it is deprecated).

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Production audit trail | `ai_observability` | PSR-3 logger → syslog/cloud; no DB overhead |
| Token usage metrics | `ai_observability` + OTel | Counter per provider/model/operation |
| Debug locally | `ai_logging` (deprecated) | Entity-based; easy to browse but DB-heavy |
| Distributed tracing | OpenTelemetry spans | Integrates with Jaeger, Tempo |

## Config: `ai_observability.settings`

| Key | Default | Description |
|-----|---------|-------------|
| `logging_enabled` | `true` | Master switch |
| `log_event_types` | `[Pre, Post, PostStreaming]` | Which events to log |
| `log_input` | `false` | Include input (up to 1024 chars) |
| `log_output` | `false` | Include output (up to 1024 chars) |
| `log_tags` | `[]` | Filter by tags (empty = all) |
| `otel_enabled` | `false` | OpenTelemetry master switch |
| `otel_spans` | `true` | Export trace spans |
| `otel_metrics` | `true` | Export token usage metrics |
| `fallback_log_message_mode` | `minimal` | `minimal` (type + provider only) or `full` (with excerpts) |

## OpenTelemetry Metrics

Counter: `ai_token_usage_{key}` (e.g., `ai_token_usage_input`, `ai_token_usage_output`, `ai_token_usage_total`)
Attributes: `uid`, `provider`, `operation_type`, `model`

## Setup Steps

1. Enable `ai_observability`
2. Navigate to `/admin/config/ai/observability`
3. Enable logging; optionally enable input/output logging
4. For production: pipe logs to cloud collector via syslog
5. For OTel: install `opentelemetry` module, configure collector (Jaeger, Tempo)

## AiObservabilityUtils (Static Helpers)

| Method | Purpose |
|--------|---------|
| `truncateForLog($text, $maxLength)` | Truncates text for log messages (default 1024 chars) |
| `buildLogContext($event)` | Extracts structured context from AI event for logging |
| `formatTokenUsage($usage)` | Formats token usage for metrics export |

## Common Mistakes

- **Wrong**: Enabling `log_input: true` and `log_output: true` in production → **Right**: Logs may contain sensitive user data; enable only for debugging
- **Wrong**: Using `ai_logging` in production → **Right**: It stores entities in the DB — performance impact at scale; use `ai_observability` instead

## See Also

- [AI Logging](ai-logging.md)
- [Events System](events-system.md)
- Reference: `web/modules/contrib/ai/modules/ai_observability/`
