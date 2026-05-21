---
description: Orchestration REST endpoint reference — services catalog, service execute, webhook register/unregister, and poll
tldr: "Five REST endpoints, all requiring Basic Auth + `use orchestration connect`. Service UUIDs use double colon (`provider::id`). Unknown service IDs return HTTP 500, not 404. Sending both `timestamp` and `id` to the poll endpoint silently uses `timestamp`. Always send `Content-Type: application/json`."
drupal_version: "11.x"
---

# Orchestration API Reference

## When to Use

> Reference this when implementing a client against the Orchestration endpoints or debugging API calls from an external platform.

## Decision

| Scenario | Endpoint |
|---|---|
| List available services | `GET /orchestration/services` |
| Execute a service | `POST /orchestration/service/execute` |
| Register a platform webhook | `POST /orchestration/webhook/register` |
| Remove a platform webhook | `POST /orchestration/webhook/unregister` |
| Pull accumulated event data | `POST /orchestration/poll` |

## Pattern

**Authentication:** All endpoints require `basic_auth` or `cookie` session. User must have `use orchestration connect` permission.

**GET `/orchestration/services`** — Returns sorted array of all services:

```json
[
  {
    "id": "eca::my_tool_wildcard",
    "label": "Send welcome email",
    "description": "Sends a welcome email to a given user.",
    "config": [
      {
        "key": "user_id",
        "label": "User ID",
        "required": true,
        "type": "string",
        "editable": true,
        "default_value": "",
        "weight": 0,
        "options": []
      }
    ]
  }
]
```

**POST `/orchestration/service/execute`:**

```json
{
  "id": "eca::my_tool_wildcard",
  "config": { "user_id": "42" }
}
```

Response: service-defined result (array or string). On exception: HTTP 500 with `{"error": "exception message"}`. Unknown `id`: HTTP 500 (no 404).

**POST `/orchestration/webhook/register`:**

```json
{ "id": "my_webhook", "webHookUrl": "https://platform.example.com/webhook/abc" }
```

Response: HTTP 200, echoes submitted JSON. Stored with `remote: true`, `method: POST`, `timeout: 30`, `verify: true`, `auth_method: none`.

**POST `/orchestration/webhook/unregister`:**

```json
{ "id": "my_webhook" }
```

**POST `/orchestration/poll`** — provide `timestamp` OR `id`, not both (`timestamp` wins if both present):

```json
{"name": "my_eca_wildcard", "timestamp": 1748000000}
```

Response (timestamp mode): `[{"timestamp": int, "data": any}]`
Response (ID mode): `[{"id": string, "data": any}]`
Response (neither): HTTP 400 `{"error": "No timestamp or id provided."}`

**Admin routes (UI only, not API):**

| Path | Purpose |
|---|---|
| `/admin/config/workflow/orchestration` | Module overview |
| `/admin/config/workflow/orchestration/webhooks` | List all webhooks |
| `/admin/config/workflow/orchestration/webhook/add` | Add webhook form |

## Common Mistakes

- **Wrong**: Using single colon in `id` (e.g., `eca:my_service`) → **Right**: UUID format is `provider_id::service_id` (double colon)
- **Wrong**: Sending both `timestamp` and `id` to poll → **Right**: `timestamp` silently wins; no error is raised
- **Wrong**: Expecting a 404 for an unknown service → **Right**: The response is HTTP 500 with an error message
- **Wrong**: Omitting `Content-Type: application/json` → **Right**: The controller uses `json_decode($this->request->getContent())`; form-encoded body yields `null` config

## See Also

- [Authentication and Permissions](authentication-and-permissions.md)
- [Webhooks and Outbound Events](webhooks-and-outbound-events.md)
- Reference: `src/Controller/Connect.php`, `orchestration.routing.yml`, `docs/develop/api.md`
