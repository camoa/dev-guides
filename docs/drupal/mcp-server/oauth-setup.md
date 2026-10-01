---
description: "Put remote MCP clients on bearer tokens with mcp_server_oauth, simple_oauth and simple_oauth_21: what each module ships, the endpoints and the setup steps"
tldr: "Install mcp_server_oauth to add oauth2 to the /mcp route, then create keys, scopes and a PKCE consumer. Gotcha: a requested scope must carry access mcp server, and PKCE is required per consumer, not by the global setting."
drupal_version: "^11"
---

# OAuth Setup

**Version:** mcp_server_oauth 1.0.0-alpha1 (core `^11`), simple_oauth 6.1.1, simple_oauth_21 v1.13.1, consumers 8.x-1.24, mcp_server 2.0.0-beta5.

## When to Use

> Use this to put a remote MCP client on bearer tokens. `mcp_server_oauth` is the production auth path for HTTP. Cookie auth suits a same-site browser only, and STDIO is local only.

## What the module ships

From `mcp_server_oauth 1.0.0-alpha1 mcp_server_oauth.info.yml`:

```yaml
core_version_requirement: ^11
dependencies:
  - mcp_server:mcp_server (>=2.0)
  - simple_oauth:simple_oauth
  - simple_oauth_21:simple_oauth_server_metadata
  - simple_oauth_21:simple_oauth_client_registration
```

Its `composer.json` requires `drupal/mcp_server ^2`, `drupal/simple_oauth ^6` and `e0ipso/simple_oauth_21 ^1`. `e0ipso/simple_oauth_21` is on Packagist and GitHub, not drupal.org (v1.13.1, 2026-09-29). simple_oauth 6.1.1 depends on `consumers:consumers` and requires `drupal/consumers ^1.17`. An OAuth client **is** a Consumer entity. This page covers only the OAuth setup MCP needs. For general Drupal API auth, see [JSON:API authentication patterns](../jsonapi/authentication-patterns.md).

| Piece | What it does | Source |
|---|---|---|
| `RouteSubscriber` | Appends `oauth2` to the `_auth` option of route `mcp_server.handle` by route name, so `/mcp` (or your base path) accepts cookie **and** bearer | `src/Routing/RouteSubscriber.php` |
| `McpAuthorizeOAuthSubscriber` | Listens on `RequestEvent` for `CallToolRequest` | `src/EventSubscriber/McpAuthorizeOAuthSubscriber.php` |
| `OAuthScopeValidator` | Validates the bearer token with simple_oauth's resource server; returns scope names, or `[]` when there is no valid token | `src/Service/OAuthScopeValidator.php` |
| `ResourceMetadataSubscriber` | Adds tool scopes to `scopes_supported` in `/.well-known/oauth-protected-resource` | `src/EventSubscriber/ResourceMetadataSubscriber.php` |
| `MetadataCacheSubscriber` | Tags that response with `mcp_server:discovery` so tool-config saves invalidate it | `src/EventSubscriber/MetadataCacheSubscriber.php` |

Endpoints come from simple_oauth and simple_oauth_21 v1.13.1, not from `mcp_server_oauth`:

| Path | Method | Module |
|---|---|---|
| `/.well-known/oauth-authorization-server` (RFC 8414) | GET, public | simple_oauth_server_metadata |
| `/.well-known/oauth-protected-resource` (RFC 9728) | GET, public | simple_oauth_server_metadata |
| `/.well-known/openid-configuration` | GET, public | simple_oauth_server_metadata |
| `/oauth/register` (RFC 7591 dynamic client registration) | POST, public | simple_oauth_client_registration |
| `/oauth/authorize`, `/oauth/token` | public | simple_oauth |
| `/oauth/revoke`, `/oauth/introspect` | POST (introspect also GET) | simple_oauth_server_metadata |

## Steps

1. **Require.** From the project page. The module's `composer.json` pulls simple_oauth and simple_oauth_21. The module README shows only `composer require drupal/simple_oauth e0ipso/simple_oauth_21`, which omits the module itself.

   ```bash
   composer require 'drupal/mcp_server_oauth:^1.0@alpha'
   ```

2. **Enable** the bridge first, then OAuth. The policy lives on the bridge's `McpToolConfig`:

   ```bash
   drush pm:enable mcp_server_tool_bridge mcp_server_oauth
   drush cache:rebuild
   ```

3. **Generate signing keys** in simple_oauth settings at `/admin/config/people/simple_oauth` (the `generate_key` route sits under it). See the [simple_oauth project](https://www.drupal.org/project/simple_oauth) for key storage.

4. **Create OAuth scopes** at `/admin/config/people/simple_oauth/oauth2_scope/dynamic`. A scope's **name** is what tool configs list. Give the scope a granularity: `permission` (listed permissions) or `role` (that role's permissions plus `authenticated`'s).

5. **Put `access mcp server` in a scope.** The route permission still applies to bearer requests, and a token's permissions come from its scopes. At least one scope a client requests must carry `access mcp server`, as a permission scope or a role scope whose role holds it. How scopes narrow permissions is on [OAuth Client Connection](oauth-client-connection.md).

6. **Create the client** (a Consumer) or let the client register itself; see [OAuth Client Connection](oauth-client-connection.md). Require PKCE there with the consumer's **Use PKCE?** field.

7. **Set scopes on tools** (see [OAuth Scopes per Tool](oauth-scopes-per-tool.md)), then `drush cache:rebuild`.

## Decision Points

| If... | Then... |
|---|---|
| The site runs Drupal 10 | `mcp_server_oauth` needs core `^11`; write a [custom subscriber](custom-authorization-subscriber.md) or keep HTTP same-site only |
| You expose only native `#[Tool]` plugins | OAuth adds bearer auth to the route; gate each tool with `checkAccess()` and permissions |
| You want any client to self-register | Dynamic registration is enabled by dependency; review its settings at `/admin/config/services/simple-oauth/oauth-21/client-registration` |

## Common Mistakes

- Following the README's `/_mcp` wording. `RouteSubscriber` alters the route by name, so it applies to `/mcp` or your overridden base path.
- Listing a scope by label instead of name. The validator compares `oauth2_scope` entity **names** (`getScope()->getName()`).
- Expecting the `simple_oauth_pkce` "mandatory" setting to require PKCE. simple_oauth's `AuthorizationCode::getGrantType()` decides from the consumer's `pkce` field (`src/Plugin/Oauth2Grant/AuthorizationCode.php:90-94`). Tick **Use PKCE?** on each consumer.

## See Also

- [OAuth Scopes per Tool](oauth-scopes-per-tool.md) | [OAuth Client Connection](oauth-client-connection.md)
- [Authentication and the Acting User](authentication-and-the-acting-user.md)
- [JSON:API authentication patterns](../jsonapi/authentication-patterns.md)
- Reference: `modules/contrib/mcp_server_oauth/`; `modules/contrib/simple_oauth/simple_oauth.routing.yml`; `modules/contrib/simple_oauth_21/modules/simple_oauth_server_metadata/simple_oauth_server_metadata.routing.yml`; https://github.com/e0ipso/simple_oauth_21
