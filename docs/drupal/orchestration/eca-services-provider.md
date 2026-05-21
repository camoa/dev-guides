---
description: Expose ECA models to external platforms via the orchestration_eca submodule — Tool event configuration, arguments YAML, poll events, and outbound webhook actions
tldr: "Use orchestration_eca to make ECA models callable from external platforms. The model must subscribe to the `eca_base.tool` event and define an `arguments` YAML field — those become the service's callable parameters. Service UUID format is `eca::{wildcard}`."
drupal_version: "11.x"
---

# ECA Services Provider

## When to Use

> Use this when you want external automation platforms to trigger ECA workflows from Drupal. This is the most common Orchestration integration pattern.

## Decision

An ECA model appears in the Orchestration service catalog only when:

- It subscribes to the `eca_base.tool` (Tool) event
- The Tool event configuration has an `arguments` field (YAML-encoded) — those become the callable `ServiceConfig` parameters

| Scenario | Solution |
|---|---|
| External platform should call an ECA model | Add Tool event to the model; configure `arguments` YAML |
| External platform should receive data from Drupal events | Register a webhook; use `orchestration_dispatch_webhook` ECA action |
| Platform cannot receive webhooks (firewall) | Use `/orchestration/poll` with `orchestration_add_item_to_poll_result_*` actions |

## Pattern

**Arguments YAML in the ECA Tool event configuration:**

```yaml
user_id:
  label: 'User ID'
  description: 'The numeric user ID to send the email to.'
  required: true
message_template:
  label: 'Message template'
  description: 'Optional custom message template key.'
  required: false
```

**External platform executes the service:**

```json
POST /orchestration/service/execute
{
  "id": "eca::my-tool-event-wildcard",
  "config": {
    "user_id": "42",
    "message_template": "welcome_v2"
  }
}
```

**ECA plugins added by `orchestration_eca`:**

| Type | Plugin | Purpose |
|---|---|---|
| Event | `orchestration_poll:timestamp` | Fires when `/orchestration/poll` receives a `timestamp` field |
| Event | `orchestration_poll:id` | Fires when `/orchestration/poll` receives an `id` field |
| Action | `orchestration_dispatch_webhook` | Dispatches outbound webhook with optional YAML/token data |
| Action | `orchestration_add_item_to_poll_result_timestamp` | Appends `{timestamp, data}` item to poll result |
| Action | `orchestration_add_item_to_poll_result_id` | Appends `{id, data}` item to poll result |

**Poll ECA tokens:**
- `[last_poll]` — epoch timestamp from the poll request (timestamp mode)
- `[last_id]` — last ID from the poll request (ID mode)

## Common Mistakes

- **Wrong**: Building an ECA model without a Tool event subscription → **Right**: The model must subscribe specifically to `eca_base.tool` to appear in `/orchestration/services`
- **Wrong**: Omitting the `arguments` YAML in the Tool event config → **Right**: Without it, the service appears with no configuration fields; external callers cannot pass parameters
- **Wrong**: Dispatching webhooks from ECA before registering them → **Right**: `Webhooks::dispatch()` returns `null` silently if the webhook ID is not in KeyValue storage
- **Wrong**: Using `orchestration_add_item_to_poll_result_timestamp` inside a "Poll by ID" model → **Right**: The action's `access()` check verifies the event type and returns forbidden if mismatched

## See Also

- [Webhooks and Outbound Events](webhooks-and-outbound-events.md)
- [Orchestration API Reference](orchestration-api-reference.md)
- Reference: `modules/eca/src/ServicesProvider.php`, `modules/eca/src/Plugin/ECA/Event/Poll.php`
