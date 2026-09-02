---
description: Install and enable the Orchestration module and its submodules, configure the service account, and verify the admin UI
tldr: "Require `drupal/orchestration`, enable `basic_auth` and `orchestration` core module, then enable only the submodules matching your use case. Create a dedicated service account user with the single `use orchestration connect` permission. Run `drush cache-rebuild` after enabling submodules."
drupal_version: "11.x"
---

# Installation and Setup

## When to Use

> Follow this when enabling the Orchestration module and its submodules for the first time.

## Steps

**1. Require the package**

```bash
composer require drupal/orchestration
```

**2. Enable the core module and whichever submodules match your use case**

The core module depends on `drupal:basic_auth` (core module, may need enabling on some setups):

```bash
drush pm-enable basic_auth orchestration -y
```

Enable submodules selectively — only what you need:

```bash
# For ECA workflow integration:
drush pm-enable eca eca_base orchestration_eca -y

# For AI Agents integration:
drush pm-enable ai ai_agents orchestration_ai_agents -y

# For AI Function Call plugins:
drush pm-enable ai orchestration_ai_function -y

# For Tool API plugins:
drush pm-enable tool orchestration_tool -y
```

For the full stack with all AI providers:

```bash
composer require drupal/ai drupal/ai_agents drupal/tool drupal/eca
drush pm-enable ai ai_agents tool eca eca_base \
  orchestration_ai_agents orchestration_ai_function orchestration_tool orchestration_eca -y
drush cache-rebuild
```

**3. Grant the "Use Orchestration" permission**

The single permission `use orchestration connect` gates all API endpoints and the admin UI. Assign it to a dedicated role used only by the integration service account — do not assign it to `authenticated` or `anonymous`.

**4. Create a dedicated service account user**

Create a Drupal user with only the `use orchestration connect` permission (plus any permissions needed by the services being invoked). Store credentials securely — they travel with every API call via Basic Auth.

**5. Verify the admin UI**

Navigate to **Administration → Configuration → Workflow → Orchestration** (`/admin/config/workflow/orchestration`). The **Webhooks** sub-page (`/admin/config/workflow/orchestration/webhooks`) lists registered webhooks.

**6. Enable JSON:API for content access** (separate from Orchestration)

External platforms use JSON:API for standard content CRUD. Orchestration handles behavior (workflow/agent/tool invocation), not data access.

```bash
drush pm-enable jsonapi -y
```

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Choosing submodules | You only need Activepieces to trigger ECA workflows | Enable only `orchestration_eca` |
| Choosing submodules | You want AI-powered automation | Enable `orchestration_ai_agents` AND an AI provider module (e.g., `drupal/ai_provider_anthropic`) |
| Choosing submodules | You use the `drupal/tool` plugin system | Enable `orchestration_tool` |
| Enabling AI providers | You need multiple LLMs | `composer require drupal/ai_provider_anthropic drupal/ai_provider_openai drupal/ai_provider_ollama` |

## Common Mistakes

- **Enabling all four submodules by default** — each adds services to the catalog; enable only what your platform integration will actually use
- **Using the admin user's credentials for the service account** — always create a dedicated user with minimal permissions
- **Not running `drush cache-rebuild` after enabling submodules** — the service collector tag discovery requires a fresh container build

## See Also

- [Authentication and Permissions](authentication-and-permissions.md) → for securing the service account
- [Connecting Activepieces](connecting-activepieces.md) → for the full platform integration setup
- Reference: `orchestration.info.yml`, `orchestration.permissions.yml`
