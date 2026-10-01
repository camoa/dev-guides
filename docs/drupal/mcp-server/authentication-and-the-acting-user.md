---
description: "Which Drupal account an MCP call runs as on STDIO, cookie HTTP and OAuth, who should get access mcp server, and how each denial reaches the client"
tldr: "Every MCP call runs as one Drupal account: the STDIO argument, the cookie user, or the OAuth token user narrowed by scopes. Gotcha: never grant access mcp server to anonymous, and prompts have no access check."
drupal_version: "^10 || ^11"
---

# Authentication and the Acting User

**Version:** mcp_server 2.0.0-beta5; with OAuth, mcp_server_oauth 1.0.0-alpha1 and simple_oauth 6.1.1.

## When to Use

> Read this before granting any permission. Every tool, resource and prompt runs as one Drupal account, and this page shows how that account is chosen and who may reach `/mcp`.

## Decision

| Transport | Acting Drupal user | Who chooses it | Source |
|---|---|---|---|
| STDIO | The `account` argument (name, ID, or `0` for anonymous) | Whoever writes the client config | `McpServerCommands.php` |
| HTTP, core only | The user Drupal's `cookie` provider resolves, else anonymous | The browser session | `mcp_server.routing.yml` |
| HTTP + `mcp_server_oauth` | The token's user, with permissions narrowed by the token's scopes (admin accounts excepted; see [OAuth Client Connection](oauth-client-connection.md)) | The OAuth grant | [OAuth Client Connection](oauth-client-connection.md) owns the rules |

**Cookie auth is for same-site browser use. STDIO is local. Use OAuth for any remote client.**

**Who gets `access mcp server`.** Grant it to a dedicated role held by the accounts agents use. Never grant it to anonymous. On an OAuth site, the anonymous 401 is what starts a client's OAuth flow.

## Denial responses

`McpExceptionSubscriber` runs at priority 80 on route `mcp_server.handle`. It turns a route-permission denial into a JSON-RPC error body. From `mcp_server 2.0.0-beta5 src/EventSubscriber/McpExceptionSubscriber.php`:

| Who | HTTP | Header |
|---|---|---|
| Anonymous | 401 | `WWW-Authenticate: Bearer realm="mcp_server"` |
| Authenticated | 403 | `WWW-Authenticate: Bearer error="insufficient_scope"` |

Other denials surface differently:

| Denial | What the client gets | Source |
|---|---|---|
| Resource `checkAccess()` | JSON-RPC internal error -32603 "Error while reading resource" (both SDK versions) | SDK `ReadResourceHandler.php` |
| `McpAuthorizationDeniedException` from a `RequestEvent` listener, SDK v0.7.1 | HTTP 401 or 403 as above | SDK v0.7.1 `Protocol.php:183` dispatches outside its try blocks |
| Same, SDK v0.8.1 | JSON-RPC internal error -32603 "Internal server error." | SDK v0.8.1 `Protocol.php:202-219` |

## Where access is checked

| Layer | Check | When |
|---|---|---|
| Route (HTTP only) | `access mcp server` | Every request |
| Native `#[Tool]` plugin | `checkAccess($account)`, default allowed | When the server is built; denied tools are absent from `tools/list` |
| Bridged Tool API tool | Tool API `access()` | At call time; the tool is still listed |
| Resource | `checkAccess($uri, $account)` | Every read |
| Prompt | None | Never |

## Common Mistakes

- Granting `access mcp server` to anonymous because the client has no cookie. Use [OAuth](oauth-setup.md) instead.
- Assuming the 401 `Bearer` challenge means core accepts tokens. Core declares only `cookie`; the header exists for OAuth clients.
- Relying on `access mcp server prompts`. It is declared but no code checks it; see [Prompts](prompts.md).
- Using an account with an admin role as the acting user. Every tool then runs with every permission.

## See Also

- [STDIO Transport](stdio-transport.md) | [HTTP Transport](http-transport.md)
- [OAuth Client Connection](oauth-client-connection.md) → for token users and scope narrowing
- [Security Considerations](security-considerations.md)
- Reference: `modules/contrib/mcp_server/src/EventSubscriber/McpExceptionSubscriber.php`, `src/Exception/McpAuthorizationDeniedException.php`
