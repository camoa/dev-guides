---
description: "Install drupal/tool, choose the tool_explorer and tool_ai_connector submodules, and grant the two Tool API permissions"
tldr: "Require drupal/tool pinned to the beta, enable the base module, then only the submodules whose callers you need. Gotcha: the two permissions gate only Tool Explorer; each tool's own access rule gates execution."
drupal_version: "^10.5 || ^11"
---

# Installation and Submodules

## When to Use

> Follow this when adding Tool API to a site. Enable the base module, then only the submodules whose callers you need. This page owns the guidance on the module's two permissions.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11 (beta; no security advisory coverage). Paths are under `modules/contrib/tool/`.

## Steps

1. **Require the package.** Pin the beta; the API changes until rc1.

   ```bash
   composer require drupal/tool:1.0.0-beta11
   ```

2. **Enable the base module.** It depends only on core `serialization` (tool 1.0.0-beta11 `tool.info.yml`).

   ```bash
   drush pm:enable tool -y
   ```

3. **Enable submodules you need.**

   | Submodule | Machine name | Depends on | Purpose |
   |---|---|---|---|
   | Tool Explorer | `tool_explorer` | `tool` | Admin UI to browse and run tools |
   | Tool - AI Connector | `tool_ai_connector` | `tool`, `ai`, `serialization` | Exposes every tool as an AI module function call. Its info file says "(Experimental)" |

4. **Grant permissions with care.** `tool.permissions.yml` defines two permissions, both `restrict access: true`:

   ```yaml
   # tool 1.0.0-beta11 tool.permissions.yml
   administer tool:
     title: 'Administer tools'
   view tool information:
     title: 'View tool information'
   ```

   They gate only the Tool Explorer routes. They do not gate Drush, PHP, AI or MCP execution. Each tool's own access rule gates execution, in the Explorer too.

5. **Rebuild caches after adding or changing a tool.** The manager caches definitions in the `tool_plugins` cache key (tool 1.0.0-beta11 `src/Tool/ToolManager.php`).

   ```bash
   drush cr
   drush tool:list
   ```

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Choosing submodules | You only call tools from Drush or PHP | Enable `tool` only |
| Choosing submodules | Site builders need to inspect schemas | Enable `tool_explorer`; grant `view tool information` to auditors |
| Choosing submodules | An AI agent or chatbot must call tools | Enable `tool_ai_connector`; it exposes **every** tool, see [Calling a Tool from the AI Module](calling-a-tool-from-the-ai-module.md) |
| Choosing a catalog | You need common content and config tools | See [Tool Belt Catalog](tool-belt-catalog.md) |

## Common Mistakes

- Granting `administer tool` broadly → it lists every tool and gives the role a UI to run every tool its own permissions allow, destructive ones included; keep it on trusted roles and grant `view tool information` to people who only read
- Assuming `administer tool` controls who can run tools from Drush or AI → it does not; per-tool access does
- Enabling `tool_ai_connector` "to try it" on a production site → every registered tool becomes an AI function at once

## See Also

- [Tool Explorer](tool-explorer.md) → the admin UI routes
- [Access Control](access-control.md) → per-tool access
- Reference: `modules/contrib/tool/tool.info.yml`, `modules/contrib/tool/tool.permissions.yml`, `modules/contrib/tool/composer.json`, `modules/contrib/tool/docs/installation.md`, `modules/contrib/tool/docs/configuration.md`
