---
description: "Drupal MCP Server (drupal/mcp_server) — serve tools, resources and prompts to MCP clients over STDIO or HTTP, bridge Tool API tools, and secure /mcp with OAuth"
tracks:
  - project: mcp_server
    channel: alpha
    reason: the guide documents the 2.0.x pre-release line (2.0.0-beta5)
    declared: "2.0.0-beta5"
    verified: 2026-10-01
  - project: mcp_server_tool_bridge
    channel: alpha
    reason: the guide documents the 1.0.x pre-release line (1.0.0-beta3)
    declared: "1.0.0-beta3"
    verified: 2026-10-01
  - project: mcp_server_oauth
    channel: alpha
    reason: the guide documents the 1.0.x pre-release line (1.0.0-alpha1)
    declared: "1.0.0-alpha1"
    verified: 2026-10-01
guide-meta:
  concepts:
    - MCP Server
    - Model Context Protocol
    - drupal/mcp_server
    - mcp_server_tool_bridge
    - mcp_server_oauth
    - mcp_server_ui
    - mcp_server_examples
    - drush mcp:server
    - STDIO transport
    - HTTP transport
    - /mcp endpoint
    - mcp_server.base_path
    - access mcp server
    - acting user
    - Mcp-Session-Id
    - MCP-Protocol-Version
    - mcp/sdk
    - "Drupal\\mcp_server\\Attribute\\Tool"
    - ToolPluginBase
    - mcp_tool_config
    - McpToolConfig
    - tool_api__ wire name
    - ResourceProvider
    - ResourceTemplateProvider
    - CacheableResourceContent
    - mcp_prompt_config
    - argument completion provider
    - mcp_server.settings
    - mcp_server.transport_middleware
    - hook_mcp_server_instructions_alter
    - hook_mcp_server_tool_alter
    - Mcp\Event\RequestEvent
    - McpAuthorizationDeniedException
    - OAuth scopes per tool
    - simple_oauth
    - simple_oauth_21
    - Consumer
    - PKCE
    - dynamic client registration
    - Claude Code MCP connection
  not:
    - Tool API tool plugins (Drupal\tool\Attribute\Tool — see drupal/tool-api)
    - Drupal calling outside MCP servers (consuming side — see drupal/ai-module)
    - drupal/mcp, mcp_tools, mo_mcp_server, mcp_client
    - General Drupal API authentication (see drupal/jsonapi)
  requires:
    - drupal/plugins
  complements:
    - drupal/tool-api
    - drupal/ai-module
    - drupal/jsonapi
  category: drupal
---

# MCP Server

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Decide whether this stack fits and which modules I need | [What MCP Server Is](what-mcp-server-is.md) | mcp_server makes Drupal an MCP server but ships no tools, resources or prompts; add the bridge, OAuth or UI modules as needed. Gotcha: all are pre-release with no security advisory coverage, and the project page is out of date. |
| Install and enable the modules | [Installation and Setup](installation-and-setup.md) | Require drupal/mcp_server and optionally the bridge, enable, rebuild caches and grant access mcp server for HTTP only. Gotcha: a fresh install serves nothing, and minimum-stability stable needs a beta stability flag. |
| Run a local agent over Drush (stdio) | [STDIO Transport](stdio-transport.md) | Use drush mcp:server with a required account argument when the client runs on the same machine. Gotcha: that account is the permission boundary, so never pass admin; an MCP client launching it without the argument never starts. |
| Expose the site over HTTP at /mcp | [HTTP Transport](http-transport.md) | HTTP serves /mcp behind access mcp server with cookie auth only; override the path with mcp_server.base_path. Gotcha: GET returns 405, bearer tokens need OAuth, and the 2026-07-28 protocol revision header gets HTTP 400. |
| Know which Drupal user a call runs as | [Authentication and the Acting User](authentication-and-the-acting-user.md) | Every MCP call runs as one Drupal account: the STDIO argument, the cookie user, or the OAuth token user narrowed by scopes. Gotcha: never grant access mcp server to anonymous, and prompts have no access check. |
| Set up OAuth2 token auth | [OAuth Setup](oauth-setup.md) | Install mcp_server_oauth to add oauth2 to the /mcp route, then create keys, scopes and a PKCE consumer. Gotcha: a requested scope must carry access mcp server, and PKCE is required per consumer, not by the global setting. |
| Configure OAuth scopes per tool | [OAuth Scopes per Tool](oauth-scopes-per-tool.md) | Set authentication_mode and scopes in a bridged tool's mcp_tool_config third-party settings. Gotcha: enforcement was not verified on a running site, native tools cannot carry a policy, and uninstall strips the settings. |
| Create an OAuth client and connect Claude Code | [OAuth Client Connection](oauth-client-connection.md) | Use authorization code with PKCE for interactive clients and client credentials for unattended agents; the Consumer is the OAuth client. Gotcha: an admin-role token user keeps every permission despite scopes. |
| Write my own authorization rule (API key, role, allowlist) | [Custom Authorization Subscriber](custom-authorization-subscriber.md) | Subscribe to Mcp RequestEvent and throw McpAuthorizationDeniedException with 401 or 403 for rules OAuth scopes cannot express. Gotcha: use the Mcp event, not Symfony's, and SDK v0.8.1 turns the denial into JSON-RPC -32603. |
| Write a native MCP tool plugin | [Native Tool Plugins](native-tool-plugins.md) | Write a native mcp_server Tool plugin extending ToolPluginBase when the operation is MCP-only. Gotcha: without a defaultConfiguration() returning enabled TRUE it registers nothing, and checkAccess() allows everyone by default. |
| Expose Tool API tools as MCP tools | [Tool API Bridge](tool-api-bridge.md) | Expose a Tool API tool over MCP by creating one mcp_tool_config; its wire name is tool_api__ plus the id. Gotcha: every enabled bridged tool is listed to every caller, access runs only at call time, and caches need a rebuild. |
| Serve read-only data as resources | [Resources and Resource Templates](resources-and-resource-templates.md) | Use resource providers for fixed URIs and resource template providers for parameterized URIs. Gotcha: a plugin registers only with an enabled config entry, and content caches permanently by default, so per-user content needs max-age 0. |
| Ship reusable prompts | [Prompts](prompts.md) | Ship reusable prompt templates as mcp_prompt_config entities with arguments and placeholder substitution. Gotcha: prompts have no access check and access mcp server prompts is never checked, so keep secrets out of prompt text. |
| Change server name, instructions, base path or middleware | [Server Configuration and Extension Points](server-configuration-and-extension-points.md) | Edit mcp_server.settings by config, not a form, and extend through the instructions hook, tool alter hook, tagged PSR-15 middleware or a RequestEvent subscriber. Gotcha: nothing reads the pending keys, and there is no session TTL setting. |
| Run the pre-launch checklist | [Security Considerations](security-considerations.md) | Run this checklist before exposing a site over MCP beyond local development: dedicated non-admin users, no anonymous endpoint access, OAuth with PKCE, minimal tools. Gotcha: the Drupal account, not the client, decides what an agent can do. |
| Fix a tool that does not appear or a 401/403 | [Troubleshooting](troubleshooting.md) | Match the symptom to its cause: a missing native tool lacks enabled TRUE, a missing bridged tool needs a cache rebuild, 401 and 403 trace to access mcp server or the token. Check watchdog before debugging the client. |
| Check sources and versions | [Sources & Maintenance Manifest](sources-maintenance.md) | Source references and maintenance manifest for the mcp server guides — web sources, code sources, and version history |
