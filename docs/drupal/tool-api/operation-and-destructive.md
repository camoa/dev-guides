---
description: "Choose the ToolOperation case and the destructive flag on #[Tool], and know which callers read them"
tldr: "Set operation by the tool's worst side effect: Write or Trigger for anything that modifies state, plus destructive: TRUE for deletes. Gotcha: both are metadata; Tool API enforces neither, so enforce safety in access and code."
drupal_version: "^10.5 || ^11"
---

# Operation and Destructive

## When to Use

> Use this when filling in `operation` and `destructive` on `#[Tool]`. Both are declarations that callers read; Tool API enforces neither.
>
> **Version:** applies to `drupal/tool` 1.0.0-beta11 (beta; no security advisory coverage). Paths are under `modules/contrib/tool/`.

## ToolOperation Cases

`ToolOperation` is a string-backed enum (tool 1.0.0-beta11 `src/Tool/ToolOperation.php`). Meanings are the enum's own `getDescription()` text, shortened.

| Case | Value | Use for | `isModifying()` | `isIdempotent()` |
|---|---|---|---|---|
| `Explain` | `explain` | Structure, schema or definitions, not data | FALSE | TRUE |
| `Read` | `read` | Fetching existing data or resources without changing them | FALSE | TRUE |
| `Transform` | `transform` | Deriving a result from input without persisting | FALSE | TRUE |
| `Trigger` | `trigger` | Starting a process: queue worker, cron, webhook | TRUE | FALSE |
| `Write` | `write` | Creating, updating or deleting stored entities or config | TRUE | FALSE |

```php
// tool 1.0.0-beta11 src/Tool/ToolOperation.php
public function isIdempotent(): bool {
  return match ($this) {
    self::Explain, self::Read, self::Transform => TRUE,
    self::Trigger, self::Write => FALSE,
  };
}
```

The module's docs table lists `Transform` as not idempotent (tool 1.0.0-beta11 `docs/developers/creating-a-tool.md`). The code says idempotent, citing [#3582962](https://git.drupalcode.org/project/tool/-/work_items/3582962). Trust the code.

## Decision

| If the tool... | Set... | Why |
|---|---|---|
| Changes stored data | `operation: ToolOperation::Write` | Callers treat it as modifying and not idempotent |
| Starts a process but does not store data itself | `ToolOperation::Trigger` | Same modifying signal, different intent |
| Deletes or cannot be undone | Add `destructive: TRUE` | MCP clients get a destructive hint; callers may confirm |
| Only computes from its input | `ToolOperation::Transform` | Marked non-modifying and idempotent |

## What Consumes These Values

Nothing in Tool API blocks a `Read` tool from writing, and nothing prompts for `destructive: TRUE`. The module's docs say "Callers use it to prompt for confirmation" (tool 1.0.0-beta11 `docs/developers/creating-a-tool.md`); no caller in Tool API, Tool Belt or the MCP bridge prompts. Consumers found in code:

- Drush `tool:list --operation=` filters by operation; `tool:info` and JSON output show `destructive` (tool 1.0.0-beta11 `src/Drush/Commands/ToolListCommand.php`, `src/Drush/Commands/ToolOutputTrait.php`).
- The MCP bridge maps `operation` and `destructive` to MCP tool hints; [Tool API Bridge](../mcp-server/tool-api-bridge.md) owns the mapping.
- `eca_tool` appends "This tool is destructive" to the ECA action description (eca_tool 1.0.0-beta1 `src/Plugin/Action/ToolDeriver.php`).
- `tool_ai_connector` reads neither (tool 1.0.0-beta11 `modules/tool_ai_connector/src/Plugin/AiFunctionCall/Derivative/ToolPluginDeriver.php`).

## Common Mistakes

- Labelling a tool `Read` because it "mostly reads" → an MCP client may then auto-run it without confirmation; label by the worst side effect
- Relying on `destructive: TRUE` as a safety net → it is metadata only; enforce safety in access and in the tool
- Leaving `operation` out → the attribute requires it; `ToolDefinition::getOperation()` falls back to `Transform` only for definitions built without the attribute

## See Also

- [Defining a Tool](defining-a-tool.md) → the rest of the attribute
- [Tool API Bridge](../mcp-server/tool-api-bridge.md) → how the hints reach MCP clients
- Reference: `modules/contrib/tool/src/Tool/ToolOperation.php`, `modules/contrib/tool/src/Tool/ToolDefinition.php`
