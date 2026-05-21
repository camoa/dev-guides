---
description: Orchestration module internal architecture — layers, key classes, service discovery, and bidirectional communication
tldr: "Orchestration has three layers: the Connect controller (REST endpoints), ServicesProviderManager (collects tagged providers), and the Webhooks service. Providers register as Symfony services tagged `orchestration_services_provider` — no plugin annotation system. Service UUID format is `provider_id::service_id` (double colon)."
drupal_version: "11.x"
---

# Architecture

## When to Use

> Read this when you need to understand how the module's components fit together before writing code or configuring submodules.

## Decision

| Question | Answer |
|---|---|
| How are providers discovered? | Symfony service collector tag: `orchestration_services_provider` — no plugin manager, no annotation scanning |
| What is the service UUID format? | `{provider_id}::{service_id}` — double colon, from `Service::uuid()` |
| Where are webhooks stored? | Drupal's `KeyValue` store, `orchestration` collection |
| Is the poll API stable? | No — `PollEventBase` and subclasses are marked `@internal` |

## Pattern

```
External Platform (Activepieces, etc.)
        |  HTTP (Basic Auth)
        v
  Orchestration Core
  ├── Connect controller  ← REST endpoints (/orchestration/*)
  ├── ServicesProviderManager  ← collects all registered providers
  └── Webhooks service  ← KeyValue store + outbound HTTP dispatch
        |
        v
  Services Providers (one per submodule)
  ├── orchestration_eca       → ECA models (Tool event subscribers)
  ├── orchestration_ai_agents → AI Agent entities
  ├── orchestration_ai_function → AI FunctionCall plugins
  └── orchestration_tool      → Tool API plugins
```

**Provider registration** (Symfony service collector pattern):

```yaml
# orchestration.services.yml
orchestration.services_manager:
  class: Drupal\orchestration\ServicesProviderManager
  tags:
    - { name: 'service_collector', tag: 'orchestration_services_provider', call: 'addServicesProvider' }
```

**Key classes:**

| Class | Role |
|---|---|
| `Connect` | Handles all five REST routes; parses JSON bodies |
| `ServicesProviderManager` | Aggregates `getAll()` across providers; delegates `executeService()` to matching provider |
| `Webhooks` | Persists webhook config in KeyValue; dispatches outbound HTTP via Guzzle |
| `Service` | Value object: provider ref + id + label + description + `ServiceConfig` list; `JsonSerializable` |
| `ServiceConfig` | Value object: key, label, description, required, type, isEditable, defaultValue, weight, constraints |
| `ServicesProviderInterface` | Contract: `getId()`, `getAll()`, `execute()` |

**Bidirectional communication:**

- **Inbound** (external → Drupal): External platform calls `/orchestration/service/execute`; manager finds the matching provider and calls `execute()`
- **Outbound** (Drupal → external): ECA model fires `orchestration_dispatch_webhook` action → `Webhooks::dispatch()` POSTs to registered URL
- **Poll** (external pulls): `/orchestration/poll` dispatches a `PollEventTimestamp` or `PollEventId` Symfony event; ECA poll action plugins collect matching items

## Common Mistakes

- **Wrong**: Looking for a plugin annotation system → **Right**: Providers register as tagged Symfony services; no `@Plugin` annotation
- **Wrong**: Adding providers after the first `getAllServices()` call and expecting them to appear → **Right**: The manager caches `$services` on first call; re-registration requires a cache rebuild
- **Wrong**: Treating `PollEventBase` subclasses as stable API → **Right**: They are `@internal` and may change on minor versions

## See Also

- [Custom Services Provider](custom-services-provider.md)
- [Orchestration API Reference](orchestration-api-reference.md)
- Reference: `orchestration.services.yml`, `orchestration.routing.yml`
