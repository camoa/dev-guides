---
description: "Run Tool API tools as ECA actions, and ECA models as tools, with the separate drupal/eca_tool project"
tldr: "Install drupal/eca_tool to run tools as ECA actions (eca_tool:<tool_id>) and to expose ECA models as tools through its Tool event. Gotcha: it needs core 11.3 or later, and its Tool event defaults to a destructive write."
drupal_version: "^11.3"
---

# Calling a Tool from ECA

## When to Use

> Use this when an ECA model must run a Tool API tool, or a tool must run an ECA model. The integration lives in the separate `drupal/eca_tool` project, not in Tool API.
>
> **Version:** applies to `eca_tool` 1.0.0-beta1 (beta; no security advisory coverage), core `^11.3 || ^12`, ECA `^3.0`, `drupal/tool ^1.0`.

## Release Facts

| Fact | Source |
|---|---|
| Release 1.0.0-beta1, 2026-09-22; branch `1.0.x`; not covered by security advisories | `updates.drupal.org` release feed for `eca_tool` |
| `core_version_requirement`: `^11.3 \|\| ^12` | Same feed |
| `composer.json` requires `php >=8.1`, `drupal/eca ^3.0`, `drupal/tool ^1.0` | `eca_tool` `composer.json` |

## Behaviour (from eca_tool 1.0.0-beta1 source)

- **Tools become ECA actions.** Action plugin `eca_tool` with a deriver keyed by tool ID, so action IDs are `eca_tool:<tool_id>`, labelled `Tool: <label>`. Tools with ID `eca` or `eca:*` are skipped to prevent a model calling itself. Destructive tools get "This tool is destructive" appended to the description (`src/Plugin/Action/Tool.php`, `src/Plugin/Action/ToolDeriver.php`).
- **Outputs become tokens.** Each output gets a `tool_output_<output>` setting naming the receiving ECA token, defaulting to the output name. On success, each declared output goes only to its own token, as the raw `getOutputValue()` value, not the formatted one. The token in `result_token_name` (default `tool_result`) holds only a status record: `success`, `message`, `failure_category` and `hints` (`recordResult()`).
- **Execution order.** The action's `execute()` calls `validateInputs()`, then `access(NULL, TRUE)`, then the tool's `execute()`.
- **Requirements.** `checkRequirements()` runs only in the action configuration form, as a warning (`buildRequirementsElement()`).
- **ECA models become tools.** Event plugin `eca_tool` (`src/Plugin/ECA/Event/EcaToolEvent.php`) dispatches its own event `eca_tool.tool` (`src/ToolEvents.php`); it is not ECA's `eca_base.tool`, which ECA 3.1 no longer has. Event configuration defaults: `description`, `arguments` (YAML), `outputs` (YAML), `operation` = `write`, `destructive` = `TRUE`, `permission` = empty.

README only, not read in code: the tool ID shape `eca:<model_id>::<event_id>`, and that running an ECA tool needs the `execute eca tools` permission unless the event's `permission` names another.

## Decision

| If you need... | Use... |
|---|---|
| ECA to call a tool | `eca_tool` (core 11.3 or later only) |
| A tool built in the ECA modeller, callable by AI or MCP | An `eca_tool` Tool event; set `operation` and `destructive` deliberately, since the defaults are `write` and `TRUE` |
| External platforms to call an ECA model | [ECA Services Provider](../orchestration/eca-services-provider.md) |

## Common Mistakes

- Installing `eca_tool` on Drupal 10 or 11.2 → its release requires core `^11.3 || ^12`
- Expecting Tool API to ship ECA plugins → it ships none
- Building on ECA's `eca_base.tool` event with ECA 3.1 → it was removed; use `eca_tool`'s Tool event
- Leaving a read-only ECA tool at the default `operation: write`, `destructive: TRUE` → callers treat it as a destructive write

## See Also

- [Tool API vs FunctionCall, MCP and ECA Tools](which-tool-this-guide-means.md) → terminology
- Reference: https://www.drupal.org/project/eca_tool, https://git.drupalcode.org/project/eca_tool (tag `1.0.0-beta1`)
