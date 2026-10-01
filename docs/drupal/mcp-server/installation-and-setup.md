---
description: "Install mcp_server and the Tool API bridge with Composer, check the resolved MCP SDK, enable the modules and grant the access mcp server permission"
tldr: "Require drupal/mcp_server and optionally the bridge, enable, rebuild caches and grant access mcp server for HTTP only. Gotcha: a fresh install serves nothing, and minimum-stability stable needs a beta stability flag."
drupal_version: "^10 || ^11"
---

# Installation and Setup

**Version:** mcp_server 2.0.0-beta5; mcp_server_tool_bridge 1.0.0-beta3; tool 1.0.0-beta11.

## When to Use

> Follow this to install `mcp_server`, optionally the Tool API bridge, and grant the endpoint permission. OAuth has its own page: [OAuth Setup](oauth-setup.md).

## Steps

1. **Require the packages.** The README shows only the first line.

   ```bash
   composer require drupal/mcp_server
   # Optional, to expose Tool API tools:
   composer require drupal/mcp_server_tool_bridge
   ```

   The bridge's `composer.json` requires `drupal/mcp_server ^2.0.0-beta5` and `drupal/tool ^1.0.0-beta8`. Composer enforces beta5. The bridge's `info.yml` minimum (`>=2.0.0-beta3`) is lower and is not the one that applies. All are pre-releases. If your root `composer.json` has `minimum-stability: stable`, add a stability flag (for example `drupal/mcp_server:^2.0@beta`).

2. **Check which MCP SDK resolved.** The constraint `^0.7.1 || ^0.8` allows either.

   ```bash
   composer show mcp/sdk
   ```

   Either version works for clients that use a handshake revision (`2024-11-05` to `2025-11-25`). No action is needed. Over HTTP, mcp_server 2.0.0-beta5 refuses the `2026-07-28` revision header; see [HTTP Transport](http-transport.md).

3. **Enable and rebuild.** From the `mcp_server` README:

   ```bash
   drush pm:enable mcp_server
   drush cache:rebuild
   ```

   Enabling the bridge also enables its dependencies. From `mcp_server_tool_bridge.info.yml`:

   ```yaml
   dependencies:
     - mcp_server:mcp_server (>=2.0.0-beta3)
     - tool:tool (>=1.0.0-beta8)
     - drupal:serialization
   ```

4. **Grant `access mcp server` only for HTTP.** From `mcp_server.permissions.yml`:

   ```yaml
   'access mcp server':
     title: 'Access MCP server'
     description: 'Allows access to the MCP server endpoint. Ships ungranted by default; grant to roles that should reach /mcp.'
     restrict access: true
   ```

   Who should get it is set on [Authentication and the Acting User](authentication-and-the-acting-user.md). The STDIO transport does not check this permission. It is a route requirement and Drush uses no route.

5. **Add something to serve.** Write a [native tool](native-tool-plugins.md), add a [bridge mapping](tool-api-bridge.md), enable a [resource provider](resources-and-resource-templates.md), or create a [prompt](prompts.md). Then rebuild caches.

## Decision Points

| At this step... | If... | Then... |
|---|---|---|
| Choosing modules | You already have Tool API tools | Add `mcp_server_tool_bridge` |
| Choosing modules | You need token auth over HTTP | Add `mcp_server_oauth`; it needs core `^11` |
| Choosing modules | You run Drupal 10 | `mcp_server` works on `^10`; the bridge needs Drupal 10.5+ (Tool API `^10.5 || ^11`); `mcp_server_oauth` does not work (`^11`) |
| Choosing transport | Only a local developer agent connects | Use STDIO; grant no HTTP permission |

## Common Mistakes

- Skipping `drush cache:rebuild` after adding a tool. Tool plugin definitions are cached under the tag `mcp_server:tools`.
- Using Drush 12. The README asks for Drush 13 or higher for STDIO.
- Expecting an admin UI. `mcp_server` has no settings form or admin routes; the UI is the `mcp_server_ui` project.
- Trusting the README's "requires only `php` and `mcp/sdk`". `composer.json` also requires `psr/simple-cache ^3.0`; Composer installs it.

## See Also

- [STDIO Transport](stdio-transport.md) | [HTTP Transport](http-transport.md)
- [OAuth Setup](oauth-setup.md) → for token auth
- [Installation and submodules (Tool API)](../tool-api/installation-and-submodules.md)
- Reference: `modules/contrib/mcp_server/composer.json`, `mcp_server.info.yml`, `mcp_server.permissions.yml`; `modules/contrib/mcp_server_tool_bridge/composer.json`; `modules/contrib/tool/tool.info.yml`
