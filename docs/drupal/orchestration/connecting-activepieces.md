---
description: Connect Drupal to Activepieces — the first and currently only built connector for the Orchestration module
tldr: "Activepieces is the only platform with a built Drupal connector (as of May 2026). It uses JSON:API for content CRUD and the Orchestration API for workflow/agent/tool invocation. Activepieces Cloud cannot reach a `localhost` Drupal site; use self-hosted Docker or ngrok for local development."
drupal_version: "11.x"
---

# Connecting Activepieces

## When to Use

> Follow this when setting up the Activepieces platform integration — the first and currently only built connector for Orchestration.

## What Activepieces Is

Activepieces is an open-source workflow automation platform comparable to Zapier or n8n. It connects external services via a visual workflow builder. The Drupal connector in Activepieces handles authentication and wraps both JSON:API (for content CRUD) and the Orchestration API (for workflow/agent/tool invocation).

**Deployment options**:
- **Activepieces Cloud** — hosted SaaS; cannot reach a `localhost` Drupal instance
- **Self-hosted Docker** — suitable for local development (DDEV-compatible); can reach a local Drupal site

## Setup Steps

**1. Enable required Drupal modules**

At minimum for JSON:API data access:
```bash
drush pm-enable jsonapi basic_auth -y
```

For the full Orchestration capability:
```bash
composer require drupal/orchestration drupal/ai drupal/ai_agents drupal/tool drupal/eca
drush pm-enable ai ai_agents tool eca eca_base \
  orchestration orchestration_ai_agents orchestration_ai_function \
  orchestration_tool orchestration_eca -y
drush cache-rebuild
```

For AI providers:
```bash
composer require drupal/ai_provider_anthropic drupal/ai_provider_openai
drush pm-enable ai_provider_anthropic ai_provider_openai -y
drush cache-rebuild
```

**2. Create a Drupal service account**

Create a user with `use orchestration connect` permission plus any content access permissions needed.

**3. Configure the Activepieces Drupal connector**

In Activepieces: add a new piece → search "Drupal" → configure connection with:
- Drupal site URL (must be publicly reachable for Activepieces Cloud)
- Service account username and password

**4. What the integration unlocks**

| Capability | How |
|---|---|
| Query Drupal content | JSON:API GET requests |
| Create/update/delete Drupal content | JSON:API CRUD |
| Trigger an ECA workflow | Orchestration `service/execute` with `eca::…` UUID |
| Invoke a Drupal AI Agent | Orchestration `service/execute` with `ai_agent::…` UUID |
| Receive Drupal events in Activepieces (push) | ECA fires `orchestration_dispatch_webhook` → Activepieces webhook trigger |
| Receive Drupal events in Activepieces (pull) | Activepieces polls `/orchestration/poll` periodically |

**5. Platform registers webhooks automatically**

When you add a webhook-based Drupal trigger in Activepieces, the platform calls `/orchestration/webhook/register` automatically. The webhook appears in the Drupal admin at `/admin/config/workflow/orchestration/webhooks` with no Edit link (it is `remote: true`).

## Other Platforms (n8n, Make, Zapier, etc.)

As of May 2026, no built connector exists for these platforms. You can integrate them manually using the raw Orchestration API endpoints (Basic Auth + JSON requests), but you must implement the connection logic yourself. The module's architecture is designed to support future platform-specific drivers.

## Common Mistakes

- **Pointing Activepieces Cloud at a `localhost` Drupal** — Cloud instances cannot reach non-public URLs; use Activepieces self-hosted or a tunnel (e.g., `ngrok`)
- **Forgetting that JSON:API is needed for content CRUD** — Orchestration does not replace JSON:API; Activepieces uses both APIs together
- **Expecting webhook delivery to work if Activepieces Cloud cannot reach your Drupal** — use poll mode for local development

## See Also

- [Authentication and Permissions](authentication-and-permissions.md) → for service account setup
- [Orchestration API Reference](orchestration-api-reference.md) → for the endpoints Activepieces calls
- Reference: https://dri.es/connecting-drupal-with-activepieces
