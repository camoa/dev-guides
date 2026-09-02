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

## Architecture Overview

The module has three layers:

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
        |
        v
  Drupal internals (ECA engine, AI module, Tool plugin system)
```

**Key classes:**

| Class | Role |
|---|---|
| `Drupal\orchestration\Controller\Connect` | Handles all five REST routes; parses JSON bodies; dispatches to manager or webhooks |
| `Drupal\orchestration\ServicesProviderManager` | Collects all tagged services providers; aggregates `getAll()` across them; delegates `executeService()` to the matching provider |
| `Drupal\orchestration\Webhooks` | Persists webhook config in Drupal's `KeyValue` store (`orchestration` collection); dispatches outbound HTTP via Guzzle |
| `Drupal\orchestration\Service` | Value object: provider ref + id + label + description + sorted `ServiceConfig` list; `JsonSerializable` |
| `Drupal\orchestration\ServiceConfig` | Value object: key, label, description, required, type, isEditable, defaultValue, weight, constraints (options extracted from constraints) |
| `Drupal\orchestration\ServicesProviderInterface` | Contract all provider services must implement: `getId()`, `getAll()`, `execute()` |

**Service UUID format**: `Service::uuid()` returns `$provider->getId() . '::' . $this->id` (double colon). This double-colon string is what the API uses as the `id` field in request/response JSON.

**Services provider discovery** uses Symfony's service collector pattern — no plugin manager, no annotation scanning:

```yaml
# orchestration.services.yml
orchestration.services_manager:
  class: Drupal\orchestration\ServicesProviderManager
  tags:
    - { name: 'service_collector', tag: 'orchestration_services_provider', call: 'addServicesProvider' }
```

Any Drupal service tagged `orchestration_services_provider` is automatically collected via `addServicesProvider()`. Each submodule registers exactly one such tagged service.

**Bidirectional communication:**

- **Inbound** (external → Drupal): External platform calls `/orchestration/service/execute` with a service UUID and config. The manager finds the matching provider and calls its `execute()`.
- **Outbound** (Drupal → external): ECA model reacts to a Drupal event, triggers the "Dispatch webhook" ECA action, which calls `Webhooks::dispatch()` to POST to the registered remote URL.
- **Poll** (external pulls): For platforms that cannot receive webhooks, `/orchestration/poll` dispatches a `PollEventTimestamp` or `PollEventId` Symfony event into Drupal's event system; ECA's poll event/action plugins collect matching items and return them in the response.

## Common Mistakes

- **Assuming there is a plugin annotation system** — there is not; providers register as tagged Symfony services
- **Forgetting that `ServicesProviderManager::getAllServices()` is lazily built and then cached in a `$services` property on the manager instance** — if multiple providers are added after first call, the cache is stale
- **Treating `PollEventBase` and its subclasses as stable API** — they are marked `@internal` and may change without notice even on minor versions

## See Also

- [Custom Services Provider](custom-services-provider.md) → for the implementation pattern
- [Orchestration API Reference](orchestration-api-reference.md) → for the endpoint contracts
- Reference: `orchestration.services.yml`, `orchestration.routing.yml` (commit `a31a0a0`, 1.0.x branch)
