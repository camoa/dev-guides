---
description: Register and dispatch Orchestration webhooks — admin UI registration, API-based registration, ECA dispatch action, and poll-based alternative
tldr: "Webhooks are stored in Drupal's KeyValue store (`orchestration` collection). Register via admin UI (`remote: false`) or via `/orchestration/webhook/register` API (`remote: true`). Dispatch using the `orchestration_dispatch_webhook` ECA action. Failed deliveries are silently discarded in 1.0.0 — monitor at the receiving platform."
drupal_version: "11.x"
---

# Webhooks and Outbound Events

## When to Use

> Use this when Drupal needs to push data to an external platform — for example, notifying an automation platform when a node is published, a user registers, or any other Drupal event fires.

## How Webhooks Work

Webhooks are stored in Drupal's `KeyValue` store under the `orchestration` collection (key: `webhooks`). Each webhook has:

| Field | Type | Notes |
|---|---|---|
| `name` | string | Human-readable label |
| `remote` | bool | `true` if registered by remote platform via API; `false` if created in admin UI |
| `url` | string | Endpoint URL |
| `method` | string | HTTP method: GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS |
| `timeout` | int | Seconds; default 30 |
| `verify` | bool | Verify TLS certificate; default `true` |
| `auth_method` | string | `none`, `basic`, or `bearer` |
| `auth_username` | string | Basic Auth username (when `auth_method = basic`) |
| `auth_password` | string | Basic Auth password (when `auth_method = basic`) |
| `auth_token` | string | Bearer token value (when `auth_method = bearer`) |
| `headers` | array | Custom headers as `['Header-Name' => 'value']` |

## Two Ways to Register Webhooks

**1. Via admin UI** (manual, `remote: false`):

Navigate to **Administration → Configuration → Workflow → Orchestration → Webhooks → Add webhook** (`/admin/config/workflow/orchestration/webhook/add`). The ID (storage key) is auto-derived from the `name` field via `Html::getId()`. Local webhooks show an "Edit" link in the webhook list; remote webhooks do not.

**2. Via API** (platform-registered, `remote: true`):

External platforms call `/orchestration/webhook/register`:

```json
POST /orchestration/webhook/register
Authorization: Basic base64(user:pass)
Content-Type: application/json

{
  "id": "my_platform_webhook",
  "webHookUrl": "https://automation-platform.example.com/webhook/abc123"
}
```

Response echoes the submitted JSON with HTTP 200. To remove: `POST /orchestration/webhook/unregister` with `{"id": "my_platform_webhook"}`.

The storage key for remote webhooks is `Html::getId($data['id'])` (applied at registration) and `Html::getId($data['id'])` again at unregistration. If the `id` string contains special characters, the storage key differs from the raw ID — keep remote webhook IDs as simple slugs.

## Dispatching Outbound Events with ECA

The typical pattern: ECA observes a Drupal entity event → runs the `orchestration_dispatch_webhook` action → `Webhooks::dispatch()` sends HTTP to the registered URL.

The `orchestration_dispatch_webhook` ECA action configuration:
- **Webhook** — select from registered webhooks (fetched via `Webhooks::getWebhooksForSelect()`)
- **Token name** — where to store the response body for use in subsequent ECA actions
- **Data** — payload, supports ECA token replacement; optionally interpret as YAML for structured data

`Webhooks::dispatch()` returns the response body as a string (decoded as YAML or JSON if possible, then stored under the token name), or `null` on connection failure or non-2xx response.

> **Note**: As of 1.0.0, `Webhooks::dispatch()` catches `GuzzleException` and `\JsonException` silently with a `// @todo Log this exception.` comment. Failed outbound webhooks are not logged. If webhook delivery reliability matters, add your own logging wrapper or monitor at the receiving platform.

## Poll-Based Alternative

For platforms that cannot receive webhooks (firewall restrictions, local development), use the poll endpoint. ECA models using `orchestration_add_item_to_poll_result_*` actions accumulate data; the platform calls `/orchestration/poll` periodically to retrieve it. See Orchestration API Reference for the endpoint details.

## Common Mistakes

- **Not registering a webhook before trying to dispatch it** — `Webhooks::dispatch()` returns `null` if the ID does not exist in KeyValue storage, with no error logged (as of 1.0.0)
- **Setting `verify: false` in production** — disabling TLS verification is acceptable only for local development with self-signed certificates
- **Using the same webhook ID from both the UI and a remote platform registration** — the last write wins; they overwrite each other silently
- **Expecting the `id` in the unregister call to match exactly what you registered when the ID contained special characters** — both register and unregister apply `Html::getId()`, so they are consistent; but the resulting storage key may differ from the raw string

## See Also

- [ECA Services Provider](eca-services-provider.md) → for the ECA action and event plugins
- [Authentication and Permissions](authentication-and-permissions.md) → for securing the service account used by `webhook/register`
- Reference: `src/Webhooks.php`, `src/Form/Webhook.php`, `src/Controller/Connect.php`
