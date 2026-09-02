---
description: AI Observability — production monitoring for AI provider calls via PSR-3 logger and OpenTelemetry
tldr: "Use `ai_observability` for production monitoring and audit trails. Use [AI Logging](ai-logging.md) only for local development debugging (it is deprecated)."
drupal_version: "11.x"
---

# AI Observability

## When to Use

> Use `ai_observability` for production monitoring and audit trails. Use [AI Logging](ai-logging.md) only for local development debugging (it is deprecated).

Production monitoring for AI provider calls. Logs to Drupal's PSR-3 logger and optionally to OpenTelemetry.

**Status:** Active (recommended for production)
**Dependencies:** `ai`; optionally `opentelemetry`, `opentelemetry_metrics`

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Production audit trail | `ai_observability` | PSR-3 logger → syslog/cloud; no DB overhead |
| Token usage metrics | `ai_observability` + OTel | Counter per provider/model/operation |
| Debug locally | `ai_logging` (deprecated) | Entity-based; easy to browse but DB-heavy |
| Distributed tracing | OpenTelemetry spans | Integrates with Jaeger, Tempo |

## Key Difference from AI Logging

| Feature | ai_observability | ai_logging |
|---------|-----------------|------------|
| Storage | Logger channel -> syslog/cloud | DB entity |
| Production use | Yes | No (deprecated) |
| Token tracking | Yes (via OTel metrics) | No |
| Status | Active | Deprecated |

## Config: `ai_observability.settings`

| Key | Default | Description |
|-----|---------|-------------|
| `logging_enabled` | `true` | Master switch |
| `log_event_types` | `[Pre, Post, PostStreaming]` | Which events |
| `log_input` | `false` | Include input (up to 1024 chars) |
| `log_output` | `false` | Include output (up to 1024 chars) |
| `log_tags` | `[]` | Filter by tags (empty = all) |
| `otel_enabled` | `false` | OpenTelemetry master switch |
| `otel_spans` | `true` | Export trace spans |
| `otel_metrics` | `true` | Export token usage metrics |
| `fallback_log_message_mode` | `minimal` | Controls log verbosity when OTel is unavailable: `minimal` (operation type + provider only) or `full` (includes input/output excerpts) |

## Conditional Service Registration

`AiObservabilityServiceProvider` conditionally registers OpenTelemetry-dependent services only when the `opentelemetry` module is installed. This avoids class-not-found errors when OTel is not present.

## AiObservabilityUtils

Static utility class providing helper methods:

- `truncateForLog($text, $maxLength)` -- Truncates text for log messages (default 1024 chars)
- `buildLogContext($event)` -- Extracts structured context (provider, model, operation type, tags) from an AI event for logging
- `formatTokenUsage($usage)` -- Formats token usage data for metrics export

## OpenTelemetry Metrics

Counter: `ai_token_usage_{key}` (e.g., `ai_token_usage_input`, `ai_token_usage_output`, `ai_token_usage_total`)
Attributes: `uid`, `provider`, `operation_type`, `model`

## Setup

1. Enable `ai_observability`
2. Navigate to `/admin/config/ai/observability`
3. Enable logging, optionally enable input/output
4. For production: pipe logs to cloud collector via syslog
5. For OTel: install `opentelemetry` module, configure collector (Jaeger, Tempo)

## Common Mistakes

- **Wrong**: Enabling `log_input: true` and `log_output: true` in production → **Right**: Logs may contain sensitive user data; enable only for debugging
- **Wrong**: Using `ai_logging` in production → **Right**: It stores entities in the DB — performance impact at scale; use `ai_observability` instead

## See Also

- [AI Logging](ai-logging.md)
- [Events System](events-system.md)
- Reference: `web/modules/contrib/ai/modules/ai_observability/`
