---
description: "Pre-launch security checklist for serving a Drupal site over MCP: acting user, endpoint permission, OAuth, tool exposure, resources, prompts and pinned versions"
tldr: "Run this checklist before exposing a site over MCP beyond local development: dedicated non-admin users, no anonymous endpoint access, OAuth with PKCE, minimal tools. Gotcha: the Drupal account, not the client, decides what an agent can do."
drupal_version: "^10 || ^11"
---

# Security Considerations

**Version:** mcp_server 2.0.0-beta5, mcp_server_tool_bridge 1.0.0-beta3, mcp_server_oauth 1.0.0-alpha1. All pre-release; none covered by security advisories.

## When to Use

> Run this checklist before exposing a site over MCP beyond local development. An MCP client can do anything its tools allow, as the acting Drupal user. Each item links to the page that owns the rule.

## Decision

| Risk | Rule | Owning page |
|---|---|---|
| Overprivileged acting user | A dedicated, minimal account per agent; never an admin account | [Authentication and the Acting User](authentication-and-the-acting-user.md) |
| Endpoint reachable by anyone | `access mcp server` on a dedicated role only; never anonymous | [Authentication and the Acting User](authentication-and-the-acting-user.md) |
| Remote client on cookie auth | Use OAuth for remote clients | [OAuth Setup](oauth-setup.md) |
| Native tool open to all | Override `checkAccess()` | [Native Tool Plugins](native-tool-plugins.md) |
| Too many tools exposed | Expose only the tools agents need; bridged tools are listed to every caller | [Tool API Bridge](tool-api-bridge.md) |
| Destructive actions | Hints are advisory; keep delete tools away from unattended agents | [Native Tool Plugins](native-tool-plugins.md), [Tool API Bridge](tool-api-bridge.md) |
| Per-user resource content | Set max-age 0 | [Resources and Resource Templates](resources-and-resource-templates.md) |
| Prompt text | No secrets; prompts have no access check | [Prompts](prompts.md) |
| Pre-release software | Pin versions; re-check after each upgrade | [What MCP Server Is](what-mcp-server-is.md) |

## Production checklist

- [ ] HTTPS enforced for `/mcp` and `/oauth/*`
- [ ] `access mcp server` not granted to anonymous
- [ ] OAuth used for every remote client; consumers use PKCE
- [ ] Each agent has a dedicated, non-admin Drupal user
- [ ] Every native tool overrides `defaultConfiguration()` and `checkAccess()`
- [ ] Only needed bridged tools are enabled
- [ ] Destructive tools reviewed and limited
- [ ] Per-user resource content uses max-age 0
- [ ] Prompts hold no secrets
- [ ] Dynamic client registration settings and registered consumers reviewed
- [ ] Versions pinned in `composer.json`

## Common Mistakes

- Treating `access mcp server` as low-stakes. It is `restrict access: true` for a reason.
- Applying the AI module's consuming-side warning ([AI module security](../ai-module/security.md), [AI agents](../ai-module/ai-agents.md)) and stopping there. Serving needs its own review.
- Assuming a read-only agent because the client is "just Claude". The Drupal account decides what it can do.

## See Also

- [Troubleshooting](troubleshooting.md)
- OWASP API Security Top 10: https://owasp.org/API-Security/
- MCP security best practices: https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices
