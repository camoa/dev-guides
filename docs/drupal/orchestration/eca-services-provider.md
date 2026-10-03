---
description: "Expose ECA models to external platforms via orchestration_eca (ECA 3.0.x only; ECA 3.1 route via Tool API) — Tool event, arguments YAML, poll events, outbound webhook actions"
tldr: "Use orchestration_eca 1.0.0 to expose ECA models as services; it works with ECA 3.0.x only (3.1 removed eca_base.tool, so no models appear). Model needs a Tool event with arguments YAML. UUID: eca::{wildcard}."
drupal_version: "11.x"
---

# ECA Services Provider

## When to Use

> Use this when you want external automation platforms to trigger ECA workflows from Drupal. This is the most common Orchestration integration pattern. `orchestration_eca` 1.0.0 works with ECA 3.0.x only; under ECA 3.1.x it finds no models.

## Version Compatibility

| ECA version | `orchestration_eca` 1.0.0 |
|---|---|
| 3.0.x | Works. `BaseEvents::TOOL` (`eca_base.tool`) and `Drupal\eca_base\Event\ToolEvent` exist |
| 3.1.x | Broken. ECA 3.1 removed both. The module enables without error, but `getAll()` finds no subscribed models, so no `eca::` services appear. `execute()` references a class that no longer exists |

Orchestration 1.0.0 (2025-10-12) is the latest release. The `1.0.x` branch (commit a31a0a0) has the same `ServicesProvider.php`, so it fails the same way. No fix has been released.

| If you... | Then... |
|---|---|
| Need external platforms to call ECA models through Orchestration today | Pin `drupal/eca` to `~3.0.0` |
| Run ECA 3.1 or later | Expose the ECA model as a Tool API tool with the separate `drupal/eca_tool` project (1.0.0-beta1) and its `eca_tool.tool` event. It derives Tool API plugins with IDs `eca:<wildcard>`, so the orchestration service UUID becomes `tool::eca:<wildcard>`. Call it through `orchestration_tool`. The route runs on two betas: eca_tool 1.0.0-beta1 and Tool API 1.0.0-beta11. See [Calling a Tool from ECA](../tool-api/calling-a-tool-from-eca.md) |

## How It Works

The `orchestration_eca` submodule registers a `ServicesProvider` tagged `orchestration_services_provider`. When `/orchestration/services` is called, this provider discovers all ECA models that subscribe to the `eca_base.tool` event and exposes each as a callable service.

An ECA model appears in the service catalog only if:
- It exists (not deleted) and is found in ECA's state data (`eca.subscribed`)
- It has at least one subscription to the `eca_base.tool` (Tool) event
- The Tool event configuration has an `arguments` field (YAML-encoded) — those become the `ServiceConfig` entries per callable parameter

**Service UUID format**: `eca::{wildcard}` where `{wildcard}` is the wildcard identifier from the ECA event subscription configuration.

## Pattern: ECA Model as Orchestration Service

On ECA 3.0.x, configure an ECA model to use the Tool event (`eca_base.tool`). In the event's configuration, set the **Arguments** field with YAML that defines callable parameters:

```yaml
# Arguments YAML in the ECA Tool event configuration:
user_id:
  label: 'User ID'
  description: 'The numeric user ID to send the email to.'
  required: true
message_template:
  label: 'Message template'
  description: 'Optional custom message template key.'
  required: false
```

When an external platform calls `/orchestration/service/execute`:

```json
{
  "id": "eca::my-tool-event-wildcard",
  "config": {
    "user_id": "42",
    "message_template": "welcome_v2"
  }
}
```

The `ServicesProvider::execute()` method:
1. Injects each config value into the ECA token service under its key name
2. Dispatches a `ToolEvent` with the wildcard into the Symfony event system
3. ECA catches it, matches the wildcard to the subscribed model, runs the model's actions
4. Returns the `ToolEvent`'s output, coerced to `array|string`

**Output coercion** (from source): If the output is an `EntityAdapter`, it extracts the entity. If it is a `DataTransferObject`, it calls `getValue()`. If it is an `EntityInterface`, it calls `toArray()`. If it is a `FieldItemListInterface`, it calls `getValue()`. Scalars become strings. `null` becomes the string `"undefined"`.

## ECA Plugins Added by orchestration_eca

**ECA Events** (external → Drupal push):

| Plugin | Event Name | Triggered when |
|---|---|---|
| `orchestration_poll:timestamp` | `orchestration_poll.timestamp` | `/orchestration/poll` receives a `timestamp` field |
| `orchestration_poll:id` | `orchestration_poll.id` | `/orchestration/poll` receives an `id` field |

Each poll event carries a `wildcard` that must match the poll request's `name` field. Available ECA tokens during these events:
- `[last_poll]` — the epoch timestamp from the poll request (timestamp mode only)
- `[last_id]` — the last ID from the poll request (ID mode only)

**ECA Actions** (Drupal → external push):

| Plugin ID | Action |
|---|---|
| `orchestration_dispatch_webhook` | Dispatches an outbound webhook with optional YAML/token data; stores response under a token name |
| `orchestration_add_item_to_poll_result_timestamp` | Appends `{timestamp, data}` item to current poll event output |
| `orchestration_add_item_to_poll_result_id` | Appends `{id, data}` item to current poll event output |

## Common Mistakes

- **Building an ECA model without a Tool event subscription and wondering why it does not appear in `/orchestration/services`** — the model must subscribe specifically to `eca_base.tool`
- **Updating ECA from 3.0.x to 3.1.x with `orchestration_eca` enabled** — every `eca::` service disappears from the catalog; pin ECA 3.0.x or move to the Tool API route
- **Omitting the `arguments` YAML in the Tool event config** — the service appears with no configuration fields; the external caller has no way to pass parameters
- **Dispatching webhooks from ECA without first registering the webhook** — `Webhooks::dispatch()` looks up the webhook config by ID from KeyValue storage and returns `null` silently if not found
- **Using `orchestration_add_item_to_poll_result_timestamp` inside a "Poll by ID" ECA model** — the action's `access()` check verifies the event type and returns forbidden if mismatched

## See Also

- [Webhooks and Outbound Events](webhooks-and-outbound-events.md) → for outbound webhook setup
- [Orchestration API Reference](orchestration-api-reference.md) → for the `/orchestration/poll` endpoint details
- [Calling a Tool from ECA](../tool-api/calling-a-tool-from-eca.md) → the ECA 3.1 route through `eca_tool`
- Reference: `modules/contrib/orchestration/modules/eca/src/ServicesProvider.php` (`eca_base.tool` lookup, `ToolEvent` dispatch), `modules/contrib/orchestration/modules/eca/src/Plugin/ECA/Event/Poll.php`, `modules/contrib/orchestration/modules/eca/src/Plugin/Action/`, `modules/contrib/eca/modules/base/src/BaseEvents.php`
