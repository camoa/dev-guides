---
description: Connect Drupal to Activepieces — the first and currently only built connector for the Orchestration module
tldr: "Activepieces is the only platform with a built Drupal connector (as of May 2026). It uses JSON:API for content CRUD and the Orchestration API for workflow/agent/tool invocation. Activepieces Cloud cannot reach a `localhost` Drupal site; use self-hosted Docker or ngrok for local development."
drupal_version: "11.x"
---

# Connecting Activepieces

## When to Use

> Follow this when setting up the Activepieces platform integration — the first and currently only built connector for Orchestration.

## Decision

| Situation | Action |
|---|---|
| Activepieces Cloud + local Drupal | Use self-hosted Activepieces Docker or a tunnel (ngrok) — Cloud cannot reach `localhost` |
| n8n / Make / Zapier | No built connector as of May 2026; implement against raw Orchestration API endpoints manually |
| Need content CRUD in Activepieces | Enable JSON:API (`drush pm-enable jsonapi -y`) — Orchestration does not replace it |

## Pattern

**Step 1: Enable required Drupal modules**

```bash
# Minimum for JSON:API data access:
drush pm-enable jsonapi basic_auth -y

# Full Orchestration capability:
composer require drupal/orchestration drupal/ai drupal/ai_agents drupal/tool drupal/eca
drush pm-enable ai ai_agents tool eca eca_base \
  orchestration orchestration_ai_agents orchestration_ai_function \
  orchestration_tool orchestration_eca -y
drush cache-rebuild

# AI providers (optional):
composer require drupal/ai_provider_anthropic drupal/ai_provider_openai
drush pm-enable ai_provider_anthropic ai_provider_openai -y && drush cache-rebuild
```

**Step 2:** Create a Drupal service account with `use orchestration connect` permission.

**Step 3:** In Activepieces → add a new piece → search "Drupal" → configure with Drupal site URL, service account username and password.

**What the integration unlocks:**

| Capability | How |
|---|---|
| Query Drupal content | JSON:API GET requests |
| Create/update/delete Drupal content | JSON:API CRUD |
| Trigger an ECA workflow | Orchestration `service/execute` with `eca::…` UUID |
| Invoke a Drupal AI Agent | Orchestration `service/execute` with `ai_agent::…` UUID |
| Receive Drupal events (push) | ECA fires `orchestration_dispatch_webhook` → Activepieces webhook trigger |
| Receive Drupal events (pull) | Activepieces polls `/orchestration/poll` periodically |

**Webhook auto-registration:** When you add a webhook trigger in Activepieces, the platform automatically calls `/orchestration/webhook/register`. The webhook appears in Drupal admin at `/admin/config/workflow/orchestration/webhooks` with no Edit link (`remote: true`).

## Common Mistakes

- **Wrong**: Pointing Activepieces Cloud at a `localhost` Drupal → **Right**: Cloud instances cannot reach non-public URLs; use Activepieces self-hosted or a tunnel
- **Wrong**: Forgetting JSON:API for content CRUD → **Right**: Activepieces uses both APIs; Orchestration handles behavior only
- **Wrong**: Expecting webhook delivery to work if Activepieces Cloud cannot reach your Drupal → **Right**: Use poll mode for local development

## See Also

- [Authentication and Permissions](authentication-and-permissions.md)
- [Orchestration API Reference](orchestration-api-reference.md)
- Reference: https://dri.es/connecting-drupal-with-activepieces
