---
description: Orchestration REST endpoint reference — services catalog, service execute, webhook register/unregister, and poll
tldr: "Five REST endpoints, all requiring Basic Auth + `use orchestration connect`. Service UUIDs use double colon (`provider::id`). Unknown service IDs return HTTP 500, not 404. Sending both `timestamp` and `id` to the poll endpoint silently uses `timestamp`. Always send `Content-Type: application/json`."
drupal_version: "11.x"
---

# Orchestration API Reference

## When to Use

> Reference this when implementing a client against the Orchestration endpoints or debugging API calls from an external platform.

## Authentication

All endpoints require authentication. Accepted methods per routing YAML: `basic_auth` or `cookie` session. The authenticated user must have the `use orchestration connect` permission.

## Endpoints

### GET `/orchestration/services`

Returns the catalog of all available services across all enabled providers, sorted alphabetically by label.

**Response**: JSON array. Each item:

```json
{
  "id": "eca::my_tool_wildcard",
  "label": "Send welcome email",
  "description": "Sends a welcome email to a given user.",
  "config": [
    {
      "key": "user_id",
      "label": "User ID",
      "description": "The numeric user ID.",
      "required": true,
      "type": "string",
      "editable": true,
      "default_value": "",
      "weight": 0,
      "options": []
    }
  ]
}
```

Note: the `config` array is sorted by `weight`. The `options` array is populated from Symfony `Choice` constraints (format: `[{key: "value", name: "Label"}, ...]`).

### POST `/orchestration/service/execute`

Executes a service by UUID with provided config. The `id` must match a UUID returned by `/orchestration/services` exactly.

**Request body**:
```json
{
  "id": "eca::my_tool_wildcard",
  "config": {
    "user_id": "42"
  }
}
```

**Response**: Service-defined result (array or string). On exception: HTTP 500 with `{"error": "exception message"}`.

If `id` refers to a non-existent service, `ServicesProviderManager::executeService()` throws `\InvalidArgumentException` which the controller wraps as a 500 error response. There is no 404.

### POST `/orchestration/webhook/register`

Registers a webhook (typically called by the external platform during connection setup).

**Request body**:
```json
{
  "id": "unique_webhook_identifier",
  "webHookUrl": "https://platform.example.com/webhook/abc"
}
```

**Response**: HTTP 200, echoes the submitted JSON. Stored with `remote: true`, `method: POST`, `timeout: 30`, `verify: true`, `auth_method: none`.

### POST `/orchestration/webhook/unregister`

Removes a previously registered webhook.

**Request body**: `{"id": "unique_webhook_identifier"}`

**Response**: HTTP 200, echoes the submitted JSON. ID is sanitized with `Html::getId()` before delete.

### POST `/orchestration/poll`

Triggers a poll event into Drupal's event system. ECA models subscribed to the matching poll event add items to the poll result.

**Request body** — provide `timestamp` OR `id`, not both. If both are present, `timestamp` takes precedence:

```json
{"name": "my_eca_wildcard", "timestamp": 1748000000}
```
```json
{"name": "my_eca_wildcard", "id": "last_seen_item_id"}
```

**Response**:
- Timestamp mode: array of `{"timestamp": int, "data": any}`
- ID mode: array of `{"id": string, "data": any}`
- Neither provided: HTTP 400 with `{"error": "No timestamp or id provided."}`

## Admin Routes (UI only, not API)

| Route name | Path | Purpose |
|---|---|---|
| `orchestration.overview` | `/admin/config/workflow/orchestration` | Module overview |
| `orchestration.webhook.list` | `/admin/config/workflow/orchestration/webhooks` | List all webhooks |
| `orchestration.webhook.add` | `/admin/config/workflow/orchestration/webhook/add` | Add webhook form |
| `orchestration.webhook.edit` | `/admin/config/workflow/orchestration/webhook/{id}/edit` | Edit webhook form (local webhooks only) |

## Common Mistakes

- **Using a single colon in the `id` field instead of double colon** — the UUID format is `provider_id::service_id`; single colon will cause "Service not found" 500
- **Sending both `timestamp` and `id` in a poll request** — `timestamp` silently wins; no error is raised but behavior may not match intent
- **Sending an unknown service `id` to `execute` and expecting a 404** — the response is HTTP 500 with an error message
- **Omitting `Content-Type: application/json`** — the controller uses `json_decode($this->request->getContent())` which requires valid JSON in the body; form-encoded body yields `null` config

## See Also

- [Authentication and Permissions](authentication-and-permissions.md) → for permission and user setup
- [Webhooks and Outbound Events](webhooks-and-outbound-events.md) → for the register/unregister flow
- Reference: `src/Controller/Connect.php`, `orchestration.routing.yml`, `docs/develop/api.md`
