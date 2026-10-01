---
description: "Browse Tool API definitions and run a tool by hand with the tool_explorer admin UI"
tldr: "Enable tool_explorer to browse tools at /admin/config/tool/explorer and run one from a form. Gotcha: the execute form skips validateInputs(), so invalid input reads as access denied, and it never shows outputs."
drupal_version: "^10.5 || ^11"
---

# Tool Explorer

## When to Use

> Use this to browse Tool API definitions or run a tool by hand in the admin UI. The `tool_explorer` submodule adds three routes under `/admin/config/tool/explorer`, with a menu link under Configuration > Development.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11 (beta; no security advisory coverage). Paths are under `modules/contrib/tool/`.

## Routes

| Route | Path | Permission |
|---|---|---|
| `tool_explorer.list` | `/admin/config/tool/explorer` | `view tool information+administer tool` (either) |
| `tool_explorer.view` | `/admin/config/tool/explorer/{plugin_id}` | `view tool information+administer tool` (either) |
| `tool_explorer.execute` | `/admin/config/tool/explorer/{plugin_id}/execute` | `administer tool` |

(tool 1.0.0-beta11 `modules/tool_explorer/tool_explorer.routing.yml`, `tool_explorer.links.menu.yml`, parent `system.admin_config_development`)

The view page also suggests a `tool.plugin.<id>` config schema when one is missing (tool 1.0.0-beta11 `docs/configuration.md`).

## What the Execute Form Does

From `ToolExecuteForm` and `ExecuteToolPluginForm`:

1. Creates the tool with **no invoker**.
2. Checks the tool's declared permission when building the form and again on submit.
3. Sets inputs from the form widgets.
4. Calls `access()` then `execute()`. It does **not** call `validateInputs()` first.
5. Shows the result message. It **never shows outputs**; the code says "We cannot currently print outputs because of security concerns."

## Common Mistakes

- Reading "You do not have access to execute this tool." as a permission problem → invalid input also fails `access()` here, because the form skips `validateInputs()`
- Looking for outputs in the UI → use `drush tool:run --json`
- Granting `administer tool` to editors so they can "see tools" → see [Installation and Submodules](installation-and-submodules.md)

## See Also

- [Installation and Submodules](installation-and-submodules.md) → the two permissions
- [Calling a Tool from Drush](calling-a-tool-from-drush.md) → to see outputs
- Reference: `modules/contrib/tool/modules/tool_explorer/`, `modules/contrib/tool/src/Form/ExecuteToolPluginForm.php`, `modules/contrib/tool/docs/usage/tool-explorer.md`
