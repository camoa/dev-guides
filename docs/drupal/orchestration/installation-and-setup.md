---
description: Install and enable the Orchestration module and its submodules, configure the service account, and verify the admin UI
tldr: "Require `drupal/orchestration`, enable `basic_auth` and `orchestration` core module, then enable only the submodules matching your use case. Create a dedicated service account user with the single `use orchestration connect` permission. Run `drush cache-rebuild` after enabling submodules."
drupal_version: "11.x"
---

# Installation and Setup

## When to Use

> Follow this when enabling the Orchestration module and its submodules for the first time.

## Decision

| At this step... | If... | Then... |
|---|---|---|
| Choosing submodules | You only need Activepieces to trigger ECA workflows | Enable only `orchestration_eca` |
| Choosing submodules | You want AI-powered automation | Enable `orchestration_ai_agents` AND an AI provider module |
| Choosing submodules | You use the `drupal/tool` plugin system | Enable `orchestration_tool` |
| Enabling AI providers | You need multiple LLMs | `composer require drupal/ai_provider_anthropic drupal/ai_provider_openai` |

## Pattern

```bash
# Step 1: Require the package
composer require drupal/orchestration

# Step 2a: Minimum — enable core module + basic_auth
drush pm-enable basic_auth orchestration -y

# Step 2b: Enable only the submodules you need
drush pm-enable eca eca_base orchestration_eca -y          # ECA workflows
drush pm-enable ai ai_agents orchestration_ai_agents -y    # AI Agents
drush pm-enable ai orchestration_ai_function -y             # AI FunctionCall plugins
drush pm-enable tool orchestration_tool -y                  # Tool API plugins

# Step 3: Full stack with all AI providers
composer require drupal/ai drupal/ai_agents drupal/tool drupal/eca
drush pm-enable ai ai_agents tool eca eca_base \
  orchestration_ai_agents orchestration_ai_function orchestration_tool orchestration_eca -y
drush cache-rebuild
```

**Service account setup:**

1. Create a Drupal user (e.g., "orchestration-service")
2. Create a dedicated role (e.g., "Orchestration Client")
3. Assign permission `use orchestration connect` to that role
4. Assign the role to the service account user
5. Grant only the additional permissions strictly needed by the services being invoked

**Verify:**

- Admin UI: `/admin/config/workflow/orchestration`
- Webhooks sub-page: `/admin/config/workflow/orchestration/webhooks`

## Common Mistakes

- **Wrong**: Enabling all four submodules by default → **Right**: Each adds services to the catalog; enable only what your integration needs
- **Wrong**: Using the admin user's credentials for the service account → **Right**: Create a dedicated user with minimal permissions
- **Wrong**: Skipping `drush cache-rebuild` after enabling submodules → **Right**: The service collector tag discovery requires a fresh container build

## See Also

- [Authentication and Permissions](authentication-and-permissions.md)
- [Connecting Activepieces](connecting-activepieces.md)
- Reference: `orchestration.info.yml`, `orchestration.permissions.yml`
