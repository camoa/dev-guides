---
description: Register and dispatch Orchestration webhooks — admin UI registration, API-based registration, ECA dispatch action, and poll-based alternative
tldr: "Webhooks are stored in Drupal's KeyValue store (`orchestration` collection). Register via admin UI (`remote: false`) or via `/orchestration/webhook/register` API (`remote: true`). Dispatch using the `orchestration_dispatch_webhook` ECA action. Failed deliveries are silently discarded in 1.0.0 — monitor at the receiving platform."
drupal_version: "11.x"
---

# Webhooks and Outbound Events

## When to Use

> Use this when Drupal needs to push data to an external platform — for example, notifying an automation platform when a node is published, a user registers, or any Drupal event fires.

## Decision

| Registration method | When to use |
|---|---|
| Admin UI (`/admin/config/workflow/orchestration/webhook/add`) | Manual setup; `remote: false`; editable in UI |
| API (`/orchestration/webhook/register`) | Platform-registered during connection setup; `remote: true`; no Edit link in UI |
| Poll endpoint | When the platform cannot receive webhooks (firewall restrictions, local development) |

## Pattern

**API registration:**

```json
POST /orchestration/webhook/register
Authorization: Basic base64(user:pass)
Content-Type: application/json

{
  "id": "my_platform_webhook",
  "webHookUrl": "https://automation-platform.example.com/webhook/abc123"
}
```

To remove: `POST /orchestration/webhook/unregister` with `{"id": "my_platform_webhook"}`.

**Webhook fields:**

| Field | Type | Default | Notes |
|---|---|---|---|
| `url` | string | — | Endpoint URL |
| `method` | string | `POST` | GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS |
| `timeout` | int | 30 | Seconds |
| `verify` | bool | `true` | Verify TLS certificate |
| `auth_method` | string | `none` | `none`, `basic`, or `bearer` |

**ECA dispatch pattern:**

1. ECA model observes a Drupal event (e.g., node publish)
2. Runs `orchestration_dispatch_webhook` action (select webhook, set token name and payload)
3. `Webhooks::dispatch()` POSTs to the registered URL; response stored under the token name

> **Warning (1.0.0):** `Webhooks::dispatch()` silently catches `GuzzleException` and `\JsonException` with a `// @todo Log this exception.` comment. Failed outbound webhook deliveries are invisible in Drupal logs. Monitor delivery at the receiving platform.

**Key storage detail:** The storage key is `Html::getId($data['id'])`. If the webhook ID contains special characters, the stored key differs from the raw string — use simple slugs for webhook IDs.

## Common Mistakes

- **Wrong**: Dispatching a webhook before registering it → **Right**: `Webhooks::dispatch()` returns `null` if the ID does not exist in KeyValue storage, with no error logged
- **Wrong**: Setting `verify: false` in production → **Right**: Acceptable only for local development with self-signed certificates
- **Wrong**: Using the same webhook ID from both UI and remote API registration → **Right**: Last write wins; they overwrite each other silently
- **Wrong**: Expecting Drupal to log failed webhook deliveries → **Right**: Monitor at the receiving platform; Drupal-side failure logging is not available in 1.0.0

## See Also

- [ECA Services Provider](eca-services-provider.md)
- [Authentication and Permissions](authentication-and-permissions.md)
- Reference: `src/Webhooks.php`, `src/Form/Webhook.php`, `src/Controller/Connect.php`
