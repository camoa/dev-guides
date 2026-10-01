---
description: "Pick an OAuth grant, create the Consumer, and connect Claude Code or another MCP client to an OAuth-protected Drupal /mcp endpoint"
tldr: "Use authorization code with PKCE for interactive clients and client credentials for unattended agents; the Consumer is the OAuth client. Gotcha: an admin-role token user keeps every permission despite scopes."
drupal_version: "^11"
---

# OAuth Client Connection

**Version:** simple_oauth 6.1.1, consumers 8.x-1.24, simple_oauth_21 v1.13.1, mcp_server_oauth 1.0.0-alpha1.

## When to Use

> Use this to pick a grant type, create the OAuth client (a Consumer), and connect Claude Code or another MCP client to an OAuth-protected `/mcp`.

## Decision

| Grant | Acting Drupal user | Effective permissions | Fits |
|---|---|---|---|
| Authorization code + PKCE | The user who approved in the browser (token `auth_user_id`) | User's role permissions ∩ scope permissions | Interactive clients such as Claude Code |
| Client credentials | The consumer's **User** field (`user_id`) | Scope permissions only | Unattended agents, CI |

**Acting user.** From simple_oauth 6.1.1 `src/Authentication/TokenAuthUser.php`:

```php
$this->consumer = $token->get('client')->entity;
if (!$this->subject = $token->get('auth_user_id')->entity) {
  $this->subject = $this->consumer->get('user_id')->entity;
}
```

A token with no user, from a consumer with no **User**, is rejected as `invalidClient`. The **User** field is simple_oauth's `user_id`, not the consumer's owner.

**Permission narrowing.** This is the one mechanism. `DecoratedUserRolesAccessPolicy` builds permission items from the subject's roles. Then `Oauth2AccessPolicy::alterPermissions()` replaces each item's permissions:

```php
$permissions = $token->get('auth_user_id')->isEmpty() ? $allowed_permissions : array_intersect($item->getPermissions(), $allowed_permissions);
```

`$allowed_permissions` is the union of the token's scope permissions. The item's `isAdmin` flag is carried over unchanged, so a subject with an admin role keeps every permission. Never use an admin account as a token's user.

## Create the client (Consumer)

Create it at `/admin/config/services/consumer/add` (permission `administer consumer entities`). simple_oauth 6.1.1 adds the OAuth fields in `simple_oauth_entity_base_field_info()`:

| Field | Label | Default | Set it to |
|---|---|---|---|
| `client_id` | Client ID | none (consumers) | A unique ID the client will send |
| `secret` | Secret | none, stored hashed | A secret for confidential clients only |
| `grant_types` | Grant types | required | `authorization_code` + `refresh_token`, or `client_credentials` |
| `confidential` | Is Confidential? | TRUE | FALSE for a public client such as a CLI using PKCE |
| `pkce` | Use PKCE? | FALSE | TRUE for authorization-code clients |
| `redirect` | Redirect URIs | none | The client's exact callback URL; required when `authorization_code` is enabled. For Claude Code: `http://localhost:PORT/callback` |
| `user_id` | User | none | A dedicated, non-admin user (client credentials only) |
| `scopes` | Scopes | none | Client-credentials scopes; limits what the client may get |
| `authorization_code_scopes` | Authorization code scopes | none | Default scopes for the code flow |
| `access_token_expiration` | Access token expiration time | 300 | Seconds |
| `refresh_token_expiration` | Refresh token expiration time | 1209600 | Seconds |
| `automatic_authorization` | Automatic authorization | FALSE | Leave off so a user approves |
| `remember_approval` | Remember previous approval | TRUE | Your choice |

**Dynamic client registration (DCR, RFC 7591).** `POST /oauth/register` (simple_oauth_21 v1.13.1 `ClientRegistrationService::createConsumer()`) creates a consumer with:

- grant types from the request, else config `default_grant_types` (`authorization_code`, `refresh_token`);
- `confidential` FALSE only when the client sends `token_endpoint_auth_method: none`;
- no `user_id`, no `scopes`, and `pkce` at its default FALSE.

A self-registered client can act only through a user who approves it in the browser. Review registered consumers and tick **Use PKCE?** on them.

## Pattern

**Interactive (authorization code).** Add the server, then authenticate with `/mcp` inside Claude Code. From the Claude Code docs:

```bash
claude mcp add --transport http drupal https://example.com/mcp
# then, inside Claude Code:
/mcp
```

**Pre-created public consumer** (`confidential` FALSE, PKCE on, redirect `http://localhost:8080/callback`). Claude Code docs: "If the server uses a public OAuth client with no secret, use only `--client-id`":

```bash
claude mcp add --transport http \
  --client-id your-client-id --callback-port 8080 \
  drupal https://example.com/mcp
```

For a confidential consumer, add `--client-secret`; Claude Code prompts for it with masked input.

**Unattended (client credentials).** Get a token from simple_oauth's `/oauth/token`, then pass it as a header (Claude Code docs syntax):

```bash
claude mcp add --transport http drupal https://example.com/mcp \
  --header "Authorization: Bearer <access-token>"
```

The default `access_token_expiration` is 300 seconds, so a pasted token stops working after five minutes. Raise it on the consumer or refresh the token yourself.

## Discovery chain

1. The client calls `/mcp` without a token. The route permission fails for anonymous, so the response is 401 with `WWW-Authenticate: Bearer realm="mcp_server"`.
2. The client reads `/.well-known/oauth-protected-resource` and `/.well-known/oauth-authorization-server`.
3. The client registers at `/oauth/register` or uses its configured client ID.
4. The user approves at `/oauth/authorize`; the client exchanges the code at `/oauth/token`.

What this stack advertises, against the MCP authorization spec (2026-07-28):

| Spec item | This stack | Source |
|---|---|---|
| 401 header `resource_metadata` and `scope` parameters | Not sent; the header is `Bearer realm="mcp_server"` | `McpExceptionSubscriber` |
| Protected resource metadata `resource` | The issuer (site base URL), not `/mcp` | simple_oauth_21 `ResourceMetadataService` |
| Client ID Metadata Documents (spec: SHOULD) | Not found in code; DCR is available | simple_oauth_21 |

No client was run against this stack. Whether Claude Code completes the flow end to end was not verified.

## Common Mistakes

- Setting a consumer's **User** to an account with an admin role. The admin flag survives scope narrowing.
- Using `--client-secret` with a public consumer. Public plus PKCE means `--client-id` and `--callback-port` only.
- Leaving **Use PKCE?** off on an authorization-code consumer.
- Forgetting a scope that carries `access mcp server`. The token authenticates but the route returns 403.
- Hard-coding a bearer token in a shared `.mcp.json`. Keep tokens out of version control; prefer the interactive flow.
- Leaving dynamic client registration open with no review. `/oauth/register` is public by design (RFC 7591).

## See Also

- [OAuth Setup](oauth-setup.md) | [OAuth Scopes per Tool](oauth-scopes-per-tool.md)
- [Authentication and the Acting User](authentication-and-the-acting-user.md)
- [JSON:API authentication patterns](../jsonapi/authentication-patterns.md) → for general Drupal API auth
- Reference: `modules/contrib/simple_oauth/simple_oauth.module`, `src/Authentication/TokenAuthUser.php`, `src/Access/Oauth2AccessPolicy.php`, `src/Access/DecoratedUserRolesAccessPolicy.php`, `src/Plugin/Oauth2Grant/AuthorizationCode.php`; `modules/contrib/consumers/src/Entity/Consumer.php`; `modules/contrib/simple_oauth_21/modules/simple_oauth_client_registration/src/Service/ClientRegistrationService.php`; https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization; https://code.claude.com/docs/en/mcp
