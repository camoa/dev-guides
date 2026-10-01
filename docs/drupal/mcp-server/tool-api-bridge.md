---
description: "Expose Drupal Tool API tools as MCP tools with mcp_server_tool_bridge: mcp_tool_config entities, wire names, annotation mapping, admin UI and call-time flow"
tldr: "Expose a Tool API tool over MCP by creating one mcp_tool_config; its wire name is tool_api__ plus the id. Gotcha: every enabled bridged tool is listed to every caller, access runs only at call time, and caches need a rebuild."
drupal_version: "^10.5 || ^11"
---

# Tool API Bridge

**Version:** mcp_server_tool_bridge 1.0.0-beta3 with mcp_server 2.0.0-beta5 and tool 1.0.0-beta11.

## When to Use

> Use the bridge to expose existing Tool API tools as MCP tools with no PHP. Each exposed tool is one config entity, so the exposure list exports with config. This page owns exposure, wire names and the annotation mapping. Tool authoring is in the [Tool API guide](../tool-api/defining-a-tool.md).

## Decision

| If a Tool API tool... | Then... |
|---|---|
| Should be callable by every user who reaches `/mcp` | Expose it; its own access rule still runs at call time |
| Should be invisible to some users | Do not expose it; every enabled bridged tool is listed to every caller |
| Deletes or changes live content | Expose only to dedicated accounts; set `destructive: TRUE` in the tool |

## Pattern

Exposure is opt-in per tool. One enabled `mcp_tool_config` becomes one MCP tool. From the bridge README:

```yaml
id: string               # machine name; becomes the MCP wire-name suffix
tool_id: string          # Tool API tool plugin ID
description: string|null # optional description override
status: boolean          # enabled
```

Config name: `mcp_server_tool_bridge.mcp_tool_config.<id>`. The bridge ships no `config/install`.

| Rule | Value | Source |
|---|---|---|
| Wire name | `tool_api__<id>` | `McpToolConfig::getMcpWireName()` |
| `id` pattern | `^[a-z0-9_]+$` | schema `Regex`, form validator |
| `id` max length | 54 chars, so the wire name stays within 64 | schema `Length`, form validator |
| Title sent to clients | The Tool API label | `McpToolConfigDeriver` |
| Description | Config override, else the Tool API description | same |
| Input schema | Tool API `ToolDefinitionSerializer::normalizeInputSchema()`: `additionalProperties: false` at the root; empty `properties` sent as `{}` | tool 1.0.0-beta11 |
| Output schema | `{type: object, properties: ...}`, or none when the tool declares no outputs | `McpToolConfigDeriver::buildOutputSchema()` |

## Annotation mapping

`McpToolConfigDeriver` sets the definition flags, and `McpServerFactory` passes them to the SDK `ToolAnnotations` as the MCP hints:

| MCP hint | Value | Source |
|---|---|---|
| `readOnlyHint` | `!operation->isModifying()` (Write and Trigger modify) | deriver :124 |
| `destructiveHint` | Tool API `destructive:` flag (default `FALSE`) | deriver :125 |
| `idempotentHint` | `operation->isIdempotent()` (Explain, Read, Transform) | deriver :126 |
| `openWorldHint` | Always `TRUE`; the base `ToolApi` plugin never sets it | `ToolDefinition::withDerivative()` |

Hints are advisory to the client. See [Operation and destructive (Tool API)](../tool-api/operation-and-destructive.md) for choosing them.

## Admin UI

All routes need `administer mcp tool configurations` (`restrict access: true`):

| Route | Path |
|---|---|
| `entity.mcp_tool_config.collection` | `/admin/config/services/mcp-server/tools` |
| `entity.mcp_tool_config.add_form` | `/admin/config/services/mcp-server/tools/add` |
| `entity.mcp_tool_config.edit_form` | `/admin/config/services/mcp-server/tools/{mcp_tool_config}/edit` |
| `entity.mcp_tool_config.delete_form` | `/admin/config/services/mcp-server/tools/{mcp_tool_config}/delete` |
| `mcp_server_tool_bridge.tool_autocomplete` | `/admin/config/services/mcp-server/tools/autocomplete` (GET) |

## Call-time flow

From `mcp_server_tool_bridge 1.0.0-beta3 src/Plugin/mcp_server/Tool/ToolApi.php`, `execute()`:

1. Create the Tool API tool with invoker `mcp_server` and `InvokerCapability::EntitiesAsHandles`. Entities cross the wire as handle strings, not IDs; see [Entity inputs and handles](../tool-api/entity-inputs-and-handles.md).
2. Set inputs only for declared names, and only when `isset($arguments[$name])`. A `null` value is dropped.
3. `validateInputs()` before access, so the client gets the violation text.
4. `$tool->access(NULL, TRUE)` as the acting user. On denial: `isError` with "Tool plugin access denied: <reason>".
5. `execute()`, then `getFormattedResult()`. Success puts outputs in `structuredContent`. The text content holds the message first, then a JSON copy of the outputs; with an empty message the JSON copy is the only block.
6. Input failures echo the input schema; access and runtime failures do not.

## Rebuild after a config change

Saving or deleting an `mcp_tool_config` invalidates the tag `mcp_server:discovery`. Tool plugin definitions, which hold the derivatives, are cached under `mcp_server:tools`. Neither module invalidates `mcp_server:tools`, and most bridge kernel tests call `clearCachedDefinitions()` after creating a config. Run `drush cache:rebuild` after adding, enabling or disabling a tool config. This is inferred from code, not run.

## Common Mistakes

- Expecting a denied bridged tool to be hidden. The `ToolApi` plugin keeps the default `checkAccess()` (allowed), so every enabled bridged tool's name, description and schema is listed to anyone who reaches `/mcp`. Access is checked at call time.
- Using an `id` over 54 chars. The wire name then exceeds 64 characters and the factory drops it with a log warning.
- Hand-importing an `id` with `-` or uppercase. The schema and form reject it, but the SDK `NameValidator` accepts it, so an imported config bypasses the rule and registers.
- Pointing `tool_id` at a tool that no longer exists. The deriver skips it silently.
- Passing an entity ID where the tool expects an entity. Pass the `handle:...` string Tool API produced.
- Copying `mcp_tool_config` YAML from `mcp_server` 1.x. The README says the entity provider moved to the bridge; remove old configs before enabling.

## See Also

- [Native Tool Plugins](native-tool-plugins.md)
- [OAuth Scopes per Tool](oauth-scopes-per-tool.md) → for scope policy on these configs
- [Calling a tool over MCP (Tool API)](../tool-api/calling-a-tool-over-mcp.md) | [Access control (Tool API)](../tool-api/access-control.md)
- Reference: `modules/contrib/mcp_server_tool_bridge/src/Entity/McpToolConfig.php`, `src/Plugin/Derivative/McpToolConfigDeriver.php`, `src/Plugin/mcp_server/Tool/ToolApi.php`, `config/schema/mcp_server_tool_bridge.schema.yml`, `mcp_server_tool_bridge.routing.yml`; `modules/contrib/tool/src/Normalizer/ToolDefinitionSerializer.php`
