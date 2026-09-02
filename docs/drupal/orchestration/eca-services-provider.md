---
description: Expose ECA models to external platforms via the orchestration_eca submodule — Tool event configuration, arguments YAML, poll events, and outbound webhook actions
tldr: "Use orchestration_eca to make ECA models callable from external platforms. The model must subscribe to the `eca_base.tool` event and define an `arguments` YAML field — those become the service's callable parameters. Service UUID format is `eca::{wildcard}`."
drupal_version: "11.x"
---

# ECA Services Provider

## When to Use

> Use this when you want external automation platforms to trigger ECA workflows from Drupal. This is the most common Orchestration integration pattern.

## How It Works

The `orchestration_eca` submodule registers a `ServicesProvider` tagged `orchestration_services_provider`. When `/orchestration/services` is called, this provider discovers all ECA models that subscribe to the `eca_base.tool` event and exposes each as a callable service.

An ECA model appears in the service catalog only if:
- It exists (not deleted) and is found in ECA's state data (`eca.subscribed`)
- It has at least one subscription to the `eca_base.tool` (Tool) event
- The Tool event configuration has an `arguments` field (YAML-encoded) — those become the `ServiceConfig` entries per callable parameter

**Service UUID format**: `eca::{wildcard}` where `{wildcard}` is the wildcard identifier from the ECA event subscription configuration.

## Pattern: ECA Model as Orchestration Service

Configure an ECA model to use the Tool event (`eca_base.tool`). In the event's configuration, set the **Arguments** field with YAML that defines callable parameters:

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
- **Omitting the `arguments` YAML in the Tool event config** — the service appears with no configuration fields; the external caller has no way to pass parameters
- **Dispatching webhooks from ECA without first registering the webhook** — `Webhooks::dispatch()` looks up the webhook config by ID from KeyValue storage and returns `null` silently if not found
- **Using `orchestration_add_item_to_poll_result_timestamp` inside a "Poll by ID" ECA model** — the action's `access()` check verifies the event type and returns forbidden if mismatched

## See Also

- [Webhooks and Outbound Events](webhooks-and-outbound-events.md) → for outbound webhook setup
- [Orchestration API Reference](orchestration-api-reference.md) → for the `/orchestration/poll` endpoint details
- Reference: `modules/eca/src/ServicesProvider.php`, `modules/eca/src/Plugin/ECA/Event/Poll.php`, `modules/eca/src/Plugin/Action/`
