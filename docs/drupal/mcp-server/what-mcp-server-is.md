---
description: "What the Drupal mcp_server module family does: the MCP protocol runtime, the Tool API bridge, OAuth, the UI and examples projects, and which ones to install"
tldr: "mcp_server makes Drupal an MCP server but ships no tools, resources or prompts; add the bridge, OAuth or UI modules as needed. Gotcha: all are pre-release with no security advisory coverage, and the project page is out of date."
drupal_version: "^10 || ^11"
---

# What MCP Server Is

**Version:** mcp_server 2.0.0-beta5, mcp_server_tool_bridge 1.0.0-beta3, mcp_server_oauth 1.0.0-alpha1. All pre-release; none covered by security advisories.

## When to Use

> Read this first. It explains what each module in the `mcp_server` family does, so you install only what you need for Drupal to serve the Model Context Protocol.

## Decision

`mcp_server` makes a Drupal site an **MCP server**. An AI client (Claude Code, Claude Desktop, MCP Inspector) connects to Drupal and calls tools, reads resources and fetches prompts. Drupal is the server. The client is outside.

`mcp_server` is the protocol runtime only. It ships plugin types, the HTTP and STDIO transports, a prompt config entity and a session store. **It ships no tool, resource or resource-template plugins of its own.** `src/Plugin` holds only bases, interfaces and managers. A fresh install exposes nothing until you add a tool, resource or prompt.

| If you need... | Use... | Why |
|---|---|---|
| The MCP protocol, transports, plugin types | `mcp_server` | Required by every other module here |
| Existing Tool API (`drupal/tool`) tools as MCP tools | `mcp_server_tool_bridge` | One config entity per exposed tool; no PHP |
| A tool written directly against MCP | A `#[Tool]` plugin in your module | No Tool API dependency |
| Bearer-token auth and per-tool scopes over HTTP | `mcp_server_oauth` | Core is cookie-auth only |
| Prompt CRUD forms, resource plugin settings, server settings pages | `mcp_server_ui` | `mcp_server` has no admin UI |
| A pattern for content entities as resources | `mcp_server_examples` | Holds the only content-resource example; copy it, do not depend on it |

**Serving is not consuming.** The AI module guide's "no MCP tools on production" rows ([AI module security](../ai-module/security.md), [AI agents](../ai-module/ai-agents.md)) concern Drupal *calling* tools on outside MCP servers, where a remote tool description can inject instructions. This guide is about Drupal *serving* MCP, where the question is what an exposed tool lets a client do as a Drupal user.

## Common Mistakes

- Installing `mcp_server` and expecting tools to appear. It exposes nothing on its own; add a tool plugin, a bridge mapping, a resource provider or a prompt.
- Following the drupal.org project page. It describes config-entity tools, built-in OAuth and an `/_mcp` endpoint. In 2.0.0-beta5 the route is `/mcp`, auth is cookie-only, and tools-as-config and OAuth live in companion projects. Trust the code.
- Treating pre-release modules as covered. Every release feed says alpha and beta releases are not covered by security advisories.
- Confusing this stack with `drupal/mcp`, `mcp_tools`, `mo_mcp_server` or `mcp_client`. Those are separate projects and out of scope here.

## See Also

- [Installation and Setup](installation-and-setup.md) → for the commands
- [Tool API Bridge](tool-api-bridge.md) → for exposing Tool API tools
- [What Tool API Is](../tool-api/what-tool-api-is.md) → for the tool framework the bridge exposes
- Reference: `modules/contrib/mcp_server/README.md` (Scope section)
