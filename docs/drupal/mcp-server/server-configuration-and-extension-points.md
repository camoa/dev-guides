---
description: "Set mcp_server.settings (name, instructions, pagination), change the base path, and extend the server with hooks, transport middleware and event subscribers"
tldr: "Edit mcp_server.settings by config, not a form, and extend through the instructions hook, tool alter hook, tagged PSR-15 middleware or a RequestEvent subscriber. Gotcha: nothing reads the pending keys, and there is no session TTL setting."
drupal_version: "^10 || ^11"
---

# Server Configuration and Extension Points

**Version:** mcp_server 2.0.0-beta5.

## When to Use

> Use this to set the server name and instructions, change the base path, or extend the HTTP stack.

## Decision

| Key | Read by code | Effect |
|---|---|---|
| `server_name`, `server_version` | Yes | Server info in the handshake |
| `server_instructions` | Yes | Instructions string; empty omits it |
| `pagination_limit` | Yes | 1-1000. `0` or empty silently becomes 50; any other out-of-range value becomes 50 with a warning |
| `pending.*` | **No** | No code in `mcp_server` or the bridge reads these keys |

## Settings

`mcp_server` has no settings form. Edit `mcp_server.settings` with `drush config:set` or config import. Whole install file `config/install/mcp_server.settings.yml`:

```yaml
langcode: en
server_name: 'Drupal MCP Server'
server_version: '1.0.0'
server_instructions: ''
pagination_limit: 50
pending:
  poll_interval_ms: 300
  sampling_timeout: 25
  elicitation_timeout: 600
```

## Extension points

| Point | How | Source |
|---|---|---|
| Instructions | `hook_mcp_server_instructions_alter(?string &$instructions)` | `mcp_server.api.php` (the only documented hook) |
| Tool definitions | `hook_mcp_server_tool_alter()` via `alterInfo('mcp_server_tool')` | `src/Plugin/ToolPluginManager.php` |
| HTTP middleware | PSR-15 service tagged `mcp_server.transport_middleware` with `priority` (higher runs first) | `mcp_server.services.yml` |
| Per-call authorization | `Mcp\Event\RequestEvent` subscriber | [Custom Authorization Subscriber](custom-authorization-subscriber.md) |
| Base path | Container parameter `mcp_server.base_path` | `src/Routing/McpRouteSubscriber.php` |
| SDK attribute discovery | `McpServerFactory::addDiscovery($basePath, $scanDirs)` from a service provider `alter()` | `src/McpServerFactory.php` |
| Notifications | Plugin type exists, but the factory never reads it | `src/Plugin/NotificationProviderInterface.php` |

From `mcp_server.services.yml`, the one middleware core registers:

```yaml
mcp_server.middleware.protocol_version:
  class: Mcp\Server\Transport\Http\Middleware\ProtocolVersionMiddleware
  tags:
    - { name: mcp_server.transport_middleware, priority: 100 }
```

## Common Mistakes

- Looking for a session TTL setting. There is none in `mcp_server`, despite the README's "session TTL via Drupal config". Sessions use core's site-wide `tempstore.expire` container parameter (604800 s).
- Tuning `pending.*`. Nothing reads them.
- Adding the SDK's CORS or DNS-rebinding middleware. The controller comment says they duplicate Drupal's CORS headers and 403 every non-localhost Host.
- Writing a notification provider. The interface docblock says Phase 1 ships the contract only.

## See Also

- [HTTP Transport](http-transport.md)
- [Custom Authorization Subscriber](custom-authorization-subscriber.md)
- Reference: `modules/contrib/mcp_server/config/install/mcp_server.settings.yml`, `mcp_server.api.php`, `mcp_server.services.yml`, `src/McpServerFactory.php`; core `core.services.yml` (`tempstore.expire`)
