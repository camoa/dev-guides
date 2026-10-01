---
description: "Source references and maintenance manifest for the mcp server guides — web sources, code sources, and version history"
---

# Sources & Maintenance

## Drupal Research Install

Not used. Code was read from release tags on git.drupalcode.org and GitHub, not from an installed site. Nothing was run.

## Web Sources

| Source | URL | Guide Sections | Last Verified |
|--------|-----|----------------|---------------|
| mcp_server project page | https://www.drupal.org/project/mcp_server | What MCP Server Is | 2026-10-01 |
| mcp_server release feed | https://updates.drupal.org/release-history/mcp_server/current | What MCP Server Is | 2026-10-01 |
| mcp_server source (tag 2.0.0-beta5) | https://git.drupalcode.org/project/mcp_server/-/tree/2.0.0-beta5 | all core sections | 2026-10-01 |
| mcp_server_tool_bridge project page | https://www.drupal.org/project/mcp_server_tool_bridge | Tool API Bridge | 2026-10-01 |
| mcp_server_tool_bridge release feed | https://updates.drupal.org/release-history/mcp_server_tool_bridge/current | Installation and Setup | 2026-10-01 |
| mcp_server_tool_bridge source (tag 1.0.0-beta3) | https://git.drupalcode.org/project/mcp_server_tool_bridge/-/tree/1.0.0-beta3 | Tool API Bridge | 2026-10-01 |
| mcp_server_oauth project page | https://www.drupal.org/project/mcp_server_oauth | OAuth Setup, OAuth Scopes per Tool | 2026-10-01 |
| mcp_server_oauth release feed | https://updates.drupal.org/release-history/mcp_server_oauth/current | OAuth Setup | 2026-10-01 |
| mcp_server_oauth source (tag 1.0.0-alpha1) | https://git.drupalcode.org/project/mcp_server_oauth/-/tree/1.0.0-alpha1 | OAuth Setup, OAuth Scopes per Tool, Custom Authorization Subscriber | 2026-10-01 |
| mcp_server_examples source (tag 1.0.0-beta1) | https://git.drupalcode.org/project/mcp_server_examples | Resources and Resource Templates | 2026-10-01 |
| mcp_server_ui project page | https://www.drupal.org/project/mcp_server_ui | What MCP Server Is, Prompts | 2026-10-01 |
| Tool API source (tag 1.0.0-beta11) | https://git.drupalcode.org/project/tool/-/tree/1.0.0-beta11 | Installation and Setup, Tool API Bridge | 2026-10-01 |
| simple_oauth project page | https://www.drupal.org/project/simple_oauth | OAuth Setup | 2026-10-01 |
| simple_oauth release feed | https://updates.drupal.org/release-history/simple_oauth/current | OAuth Setup | 2026-10-01 |
| simple_oauth source (tag 6.1.1) | https://git.drupalcode.org/project/simple_oauth/-/tree/6.1.1 | OAuth Setup, OAuth Client Connection | 2026-10-01 |
| consumers source (tag 8.x-1.24) | https://git.drupalcode.org/project/consumers/-/tree/8.x-1.24 | OAuth Client Connection | 2026-10-01 |
| simple_oauth_21 (v1.13.1) | https://github.com/e0ipso/simple_oauth_21/tree/v1.13.1 | OAuth Setup, OAuth Client Connection | 2026-10-01 |
| simple_oauth_21 on Packagist | https://repo.packagist.org/p2/e0ipso/simple_oauth_21.json | OAuth Setup | 2026-10-01 |
| MCP PHP SDK v0.8.1 (ProtocolVersion, ProtocolVersionMiddleware, StreamableHttpTransport, Protocol, ReadResourceHandler, NameValidator) | https://github.com/modelcontextprotocol/php-sdk/tree/v0.8.1 | HTTP Transport, Authentication and the Acting User, Custom Authorization Subscriber, Native Tool Plugins, Troubleshooting | 2026-10-01 |
| MCP PHP SDK v0.7.1 (same files) | https://github.com/modelcontextprotocol/php-sdk/tree/v0.7.1 | HTTP Transport, Authentication and the Acting User, Custom Authorization Subscriber | 2026-10-01 |
| mcp/sdk on Packagist | https://repo.packagist.org/p2/mcp/sdk.json | Installation and Setup | 2026-10-01 |
| MCP specification: Authorization (2026-07-28) | https://modelcontextprotocol.io/specification/2026-07-28/basic/authorization | STDIO Transport, OAuth Client Connection | 2026-10-01 |
| MCP specification versioning | https://modelcontextprotocol.io/specification/versioning | HTTP Transport | 2026-10-01 |
| MCP security best practices (2026-07-28) | https://modelcontextprotocol.io/docs/2026-07-28/tutorials/security/security_best_practices | Security Considerations | 2026-10-01 |
| Claude Code MCP docs | https://code.claude.com/docs/en/mcp | STDIO Transport, HTTP Transport, OAuth Client Connection | 2026-10-01 |
| OWASP API Security Top 10 | https://owasp.org/API-Security/ | Security Considerations | 2026-10-01 |
| AI module security (dev-guides) | ../ai-module/security.md | What MCP Server Is, Security Considerations | 2026-10-01 |
| AI agents (dev-guides) | ../ai-module/ai-agents.md | What MCP Server Is, Security Considerations | 2026-10-01 |
| JSON:API authentication patterns (dev-guides) | ../jsonapi/authentication-patterns.md | OAuth Setup, OAuth Client Connection | 2026-10-01 |
| Tool API guide (dev-guides) | ../tool-api/index.md | What MCP Server Is, Native Tool Plugins, Tool API Bridge, Custom Authorization Subscriber | 2026-10-01 |

## Code Sources

| Module | Relative Path | Guide Sections | Version |
|--------|---------------|----------------|---------|
| MCP Server | modules/contrib/mcp_server/ | all except OAuth sections | 2.0.0-beta5 |
| MCP Server Tool Bridge | modules/contrib/mcp_server_tool_bridge/ | Tool API Bridge, OAuth Scopes per Tool, Troubleshooting | 1.0.0-beta3 |
| MCP Server OAuth | modules/contrib/mcp_server_oauth/ | OAuth Setup, OAuth Scopes per Tool, Custom Authorization Subscriber | 1.0.0-alpha1 |
| MCP Server Examples | modules/contrib/mcp_server_examples/ | Resources and Resource Templates | 1.0.0-beta1 |
| Tool API | modules/contrib/tool/ | Installation and Setup, Tool API Bridge | 1.0.0-beta11 |
| Simple OAuth | modules/contrib/simple_oauth/ | OAuth Setup, OAuth Client Connection | 6.1.1 |
| Consumers | modules/contrib/consumers/ | OAuth Client Connection | 8.x-1.24 |
| Simple OAuth 2.1 | modules/contrib/simple_oauth_21/ | OAuth Setup, OAuth Client Connection | 1.13.1 |
| MCP PHP SDK | vendor/mcp/sdk/ | HTTP Transport, Authentication and the Acting User, Custom Authorization Subscriber, Native Tool Plugins | 0.7.1 / 0.8.1 |
| Drupal core (ConfigEntityBase, core.services.yml, NegotiationMiddleware) | core/ | OAuth Scopes per Tool, HTTP Transport, Server Configuration | 11.4 |

Core: `^10 || ^11` for `mcp_server`; Drupal 10.5+ for the bridge (Tool API); `^11` for `mcp_server_oauth`.
