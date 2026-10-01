---
description: "Configure a per-tool OAuth scope policy on bridged MCP tools through mcp_tool_config third-party settings in mcp_server_oauth"
tldr: "Set authentication_mode and scopes in a bridged tool's mcp_tool_config third-party settings. Gotcha: enforcement was not verified on a running site, native tools cannot carry a policy, and uninstall strips the settings."
drupal_version: "^11"
---

# OAuth Scopes per Tool

**Version:** mcp_server_oauth 1.0.0-alpha1 with mcp_server_tool_bridge 1.0.0-beta3 and mcp_server 2.0.0-beta5.

## When to Use

> Use this to configure which OAuth scopes a bridged tool's policy lists, through the tool's `mcp_tool_config` third-party settings. Enforcement at this version was not verified on a running site.

## Decision

| If you need... | Configure... | Page |
|---|---|---|
| Who may reach `/mcp` at all | `access mcp server` inside a scope | [OAuth Setup](oauth-setup.md) |
| Who may run a bridged tool | The Tool API tool's `permission:` or `checkAccess()` | [Access control (Tool API)](../tool-api/access-control.md) |
| A per-tool scope policy | `third_party_settings.mcp_server_oauth` on the tool config (this page) | — |
| A rule scopes cannot express | A custom subscriber or middleware | [Custom Authorization Subscriber](custom-authorization-subscriber.md) |

## Pattern

From `mcp_server_oauth 1.0.0-alpha1 config/schema/mcp_server_oauth.schema.yml`:

```yaml
mcp_server_tool_bridge.mcp_tool_config.*.third_party.mcp_server_oauth:
  type: mapping
  mapping:
    authentication_mode:
      type: string
    scopes:
      type: sequence
      sequence:
        type: string
```

An exported tool config with a policy (derived from the schema and the module's entity builder):

```yaml
# mcp_server_tool_bridge.mcp_tool_config.content_read.yml
id: content_read
tool_id: 'example_module:read_node'
description: null
status: true
third_party_settings:
  mcp_server_oauth:
    authentication_mode: required
    scopes:
      - 'content:read'
```

`authentication_mode` is `disabled` (default) or `required`. Scopes are AND logic (`array_diff` in `OAuthScopeValidator::validateScopes()`): all listed scopes must be on the token. Enforcement at this version was not verified on a running site.

## Denial outcome

When the subscriber denies a call, it throws `McpAuthorizationDeniedException('authentication_required', 401)` if the token has no scopes (missing, invalid, revoked, or a token with zero scopes), else `('insufficient_scope', 403)`. On SDK v0.7.1 the client receives that HTTP status. On SDK v0.8.1 it receives JSON-RPC internal error -32603; see [Authentication and the Acting User](authentication-and-the-acting-user.md).

## UI

Editing a tool at `/admin/config/services/mcp-server/tools/{id}/edit` shows an **OAuth2 Authorization** details element (`mcp_server_oauth.module` form alters). The **Required scopes** options come only from scopes already set on enabled tool configs (`OAuthScopeDiscoveryService::getScopesSupported()`). On a fresh site the list is empty, so set the first scope through config import.

## Common Mistakes

- Treating a scope policy as the only gate. Keep `access mcp server` and Tool API permissions narrow as well.
- Expecting native `#[Tool]` plugins to carry a scope policy. The settings live on `mcp_tool_config`, which only bridged tools have.
- Uninstalling `mcp_server_oauth` and expecting the policy to come back on re-enable. Each tool config depends on the module, and core's `ConfigEntityBase::onDependencyRemoval()` strips its `third_party_settings` on uninstall. Re-enabling restores nothing unless you re-import an earlier export. The module README says the settings stay dormant; the code removes them.

## See Also

- [OAuth Setup](oauth-setup.md) | [OAuth Client Connection](oauth-client-connection.md)
- [Tool API Bridge](tool-api-bridge.md) → for `McpToolConfig`
- Reference: `modules/contrib/mcp_server_oauth/config/schema/mcp_server_oauth.schema.yml`, `src/Service/OAuthScopeValidator.php`, `mcp_server_oauth.module`; core `lib/Drupal/Core/Config/Entity/ConfigEntityBase.php`
