---
description: "Serve the Drupal MCP server over HTTP at /mcp: route, base path override, client flow, session locks, CORS and supported MCP protocol revisions"
tldr: "HTTP serves /mcp behind access mcp server with cookie auth only; override the path with mcp_server.base_path. Gotcha: GET returns 405, bearer tokens need OAuth, and the 2026-07-28 protocol revision header gets HTTP 400."
drupal_version: "^10 || ^11"
---

# HTTP Transport

**Version:** mcp_server 2.0.0-beta5 with mcp/sdk v0.7.1 or v0.8.1.

## When to Use

> Use HTTP when the client is remote or cannot run Drush. It needs a permission grant and, for remote clients, a token.

## Decision

| Client | Auth | Page |
|---|---|---|
| Browser on the same site, logged in | Core cookie auth | [Authentication and the Acting User](authentication-and-the-acting-user.md) |
| Remote client (Claude Code, CI agent) | OAuth bearer token | [OAuth Setup](oauth-setup.md) |
| A rule OAuth does not express (API key, IP) | Your own subscriber or middleware | [Custom Authorization Subscriber](custom-authorization-subscriber.md) |

## Pattern

From `mcp_server 2.0.0-beta5 mcp_server.routing.yml`:

```yaml
mcp_server.handle:
  path: '/mcp'
  defaults:
    _controller: '\Drupal\mcp_server\Controller\McpServerController::handle'
  requirements:
    _permission: 'access mcp server'
    _format: 'json'
  methods: [GET, POST, DELETE, OPTIONS]
  options:
    _auth: ['cookie']
    no_cache: TRUE
```

**Override the path** with the container parameter that `McpRouteSubscriber` applies. It must start with `/` and must not end with `/` (checked by `assert()` only):

```yaml
# sites/default/services.yml
parameters:
  mcp_server.base_path: '/agents/mcp'
```

**Client flow** (from the functional test): POST JSON-RPC `initialize` with `Content-Type: application/json`, read the `Mcp-Session-Id` response header, and send it on later requests. Use the bare URL (`https://example.com/mcp`); core reads format only from `?_format`, and `json` is the route's only format.

**Claude Code** (from the Claude Code docs):

```bash
claude mcp add --transport http drupal https://example.com/mcp
```

## How the endpoint behaves

| Behavior | Detail | Source |
|---|---|---|
| Server instance | Rebuilt per request with the current user (`mcp_server.server` is `shared: false`) | `mcp_server.services.yml` |
| Methods | The route accepts GET, but both SDK versions answer GET with 405 "Method Not Allowed"; there is no GET/SSE stream | SDK `StreamableHttpTransport.php` (v0.7.1 :364, v0.8.1 :439) |
| Session lock | One lock per `Mcp-Session-Id`; a second request waits on the lock, retries once, then gets 503 `MCP session lock timeout` with `Retry-After: 1` | `src/Controller/McpServerController.php:86-96` |
| Streaming | Non-seekable bodies become a `StreamedResponse`; the lock is released after the stream ends | same, :126-148 |
| Sessions | SharedTempStore, collection `mcp_sessions`; garbage-collected by cron. Lifetime is core's `tempstore.expire` container parameter (604800 s), site-wide, not per module | `src/Session/SharedTempStoreSessionStore.php`, core `core.services.yml` |
| Middleware | Only `ProtocolVersionMiddleware`, registered with no arguments; SDK CORS and DNS-rebinding middleware are omitted on purpose | `mcp_server.services.yml:97-103` |
| CORS | `McpCorsConfigPass` merges `GET, POST, DELETE, OPTIONS` and `content-type, mcp-protocol-version, mcp-session-id` into `cors.config`; it does not enable CORS and does not add `authorization` | `src/CompilerPass/McpCorsConfigPass.php` |
| Host checks | Left to Drupal's `trusted_host_patterns` | controller comment |

## Protocol versions

From the SDK's `src/Schema/Enum/ProtocolVersion.php`:

| SDK | Revisions known |
|---|---|
| v0.7.1 | `2024-11-05`, `2025-03-26`, `2025-06-18`, `2025-11-25` |
| v0.8.1 | the four above, plus `2026-07-28` |

mcp_server registers `ProtocolVersionMiddleware` without arguments. Its constructor then accepts only `ProtocolVersion::handshakeVersions()`, and a request with `MCP-Protocol-Version: 2026-07-28` gets HTTP 400 (SDK v0.8.1 `ProtocolVersionMiddleware.php:61-94`). Configure clients to use a handshake revision (`2025-11-25` or earlier).

## Common Mistakes

- Pointing a client at `/_mcp`. That was the 1.x path; 2.x serves `/mcp`.
- Expecting a bearer token to work on core alone. The route declares only `cookie`; core ships no token provider. Add [OAuth](oauth-setup.md).
- Expecting a GET event stream. Both SDK versions return 405 for GET.
- Expecting a browser client to send `Authorization` cross-origin. The CORS pass does not add `authorization` to the allowed headers; add it in your `cors.config` if a browser client needs it.
- Ignoring log volume. The controller logs "MCP request received" and "User is: <name>" at info level on every request.

## See Also

- [Authentication and the Acting User](authentication-and-the-acting-user.md)
- [OAuth Setup](oauth-setup.md) → for bearer tokens
- [Server Configuration and Extension Points](server-configuration-and-extension-points.md) → for transport middleware
- Reference: `modules/contrib/mcp_server/mcp_server.routing.yml`, `src/Routing/McpRouteSubscriber.php`, `src/Controller/McpServerController.php`; `vendor/mcp/sdk/src/Server/Transport/`; https://github.com/modelcontextprotocol/php-sdk
