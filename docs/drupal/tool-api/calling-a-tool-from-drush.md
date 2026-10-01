---
description: "Find, inspect and run Tool API tools with drush tool:list, tool:search, tool:info and tool:run"
tldr: "Use tool:list, tool:search and tool:info to inspect tools, and tool:run with --input and --json to run one. Gotcha: tool:run runs as anonymous unless you pass --uid, and the drush invoker cannot pass entity inputs."
drupal_version: "^10.5 || ^11"
---

# Calling a Tool from Drush

## When to Use

> Use this to find, inspect or run Tool API tools from the command line, or to let a local agent drive them. Tool API ships four Drush commands; `tool:run` runs as anonymous unless you pass `--uid`.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11 (beta; no security advisory coverage). Paths are under `modules/contrib/tool/`.

## Commands

| Command | Aliases | Arguments and options (from the `#[Command]` attributes) |
|---|---|---|
| `tool:list` | `tools`, `tlist` | `--format=table\|markdown\|json` (default table), `--operation=explain\|read\|transform\|trigger\|write`, `--unmet=show\|hide\|only` (default show) |
| `tool:search` | `tsearch` | `keywords` (space-separated), `--match=or\|and` (default or), `--format`, `--operation`, `--unmet` |
| `tool:info` | `tinfo` | `tool_id`, `--format=table\|markdown\|json` |
| `tool:run` | `trun` | `tool_id`, `--input` (repeatable; JSON object or `key=value`), `--json`, `--uid` |

(tool 1.0.0-beta11 `src/Drush/Commands/`)

```bash
drush tool:list --operation=read --format=json
drush tool:search "entity save" --match=and
drush tool:info tool_belt:entity_list --format=json
drush tool:run tool_belt:entity_list --uid=2 --input='{"entity_type_id":"node"}' --json
```

These lines follow the declared options and inputs; they were not executed when this page was written.

## What Each Returns

- **`tool:list` / `tool:search` JSON:** a list of `{id, label, description, operation, destructive, provider, requirements: {met, message}}`. Search matches substrings of the lowercase ID, label and description. Neither filters by the caller's permissions.
- **`tool:info` JSON:** the summary plus `permission`, `inputs` (type, label, description, required, multiple, locked), `outputs`, `input_schema` (full JSON Schema, locked inputs included) and `output_schema`. Table output adds a constraints column, a warning for unknown permission names, and a usage example. Unknown tool: exit 1. Unmet requirements: still exit 0.
- **`tool:run --json` success or tool failure:** `{"success": bool, "message": "...", "outputs": {...}}`. `outputs` is whatever `getFormattedResult()` carries, on failure too. Entities print as `{entity_type, id, uuid, label}` only.
- **`tool:run --json` command error:** `{"success": false, "error": "...", "error_type": "..."}` with `error_type` one of `tool_not_found`, `invalid_option`, `user_not_found`, `user_blocked`, `invalid_input`, `access_denied`, `execution_failed` (tool 1.0.0-beta11 `src/Drush/RunErrorType.php`). Exit code 1 on any failure.

## tool:run Sequence

From `ToolRunCommand::runTool()` and `executeTool()`:

1. Tool exists, options parse (`--uid` must be a non-negative integer).
2. Load the user. No `--uid` or `--uid=0` means `AnonymousUserSession`. Missing or blocked users stop here.
3. Switch to that account.
4. `ToolManager::checkPermission()` on the definition, **before** creating the tool.
5. Create the tool with the `drush` invoker (the caller identity; see [Calling a Tool from PHP](calling-a-tool-from-php.md)). It has no capabilities.
6. `setInputValue()` for each `--input` name. An undeclared name throws and reports `invalid_input`.
7. `validateInputs()`, then `access()`, then `execute()`.
8. Print `getFormattedResult()` values.

## Common Mistakes

- Running write tools without `--uid` → access denied; the message adds "Ran as anonymous (uid 0); pass --uid=<id> to run as a user."
- Using `--uid=1` by habit → superuser bypasses permission checks; use a role-scoped account to test the real rule
- Passing an entity input from Drush → the `drush` invoker cannot supply entities; see [Entity Inputs and Handles](entity-inputs-and-handles.md)
- Treating `tool:list` as "tools this account can run" → it lists every tool; check `permission` in `tool:info`
- Parsing table output in scripts → use `--format=json` and `--json`; branch on `error_type`

## See Also

- [Access Control](access-control.md) → why `--uid` matters
- [checkRequirements](checkrequirements.md) → the `Requirements` column
- Reference: `modules/contrib/tool/src/Drush/Commands/ToolRunCommand.php`, `modules/contrib/tool/src/Drush/Commands/ToolInfoCommand.php`, `modules/contrib/tool/src/Drush/Commands/ToolOutputTrait.php`, `modules/contrib/tool/docs/usage/drush.md`
