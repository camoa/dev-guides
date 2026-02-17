---
description: Understand what the Figma MCP server does and which server type (remote vs desktop) to use for your workflow
---

# Figma MCP Overview

### When to Use
When you want AI agents to generate code directly from Figma designs — using structured layout data, design tokens, and component mappings rather than screenshots alone.

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Maximum compatibility, no desktop app | Remote server | Works on all plans, all seats, any editor |
| Selection-based workflow (select in Figma → generate) | Desktop server | Only desktop server can read active Figma selections |
| Lowest friction Claude Code setup | Claude Code plugin | One command install, bundled skills |
| Dev/Full seat on paid plan | Either | Desktop unlocks selection workflow; remote still provides link-based access |
| Starter plan or View/Collab seat | Remote only | Desktop server requires Dev or Full seat on paid plan |

### Pattern
The MCP server exposes 13 tools to AI agents. Agents call these tools automatically based on prompts, or you can trigger them explicitly:

```
# Remote endpoint
https://mcp.figma.com/mcp

# Desktop endpoint (Figma app running)
http://127.0.0.1:3845/mcp

# Verify who is authenticated (remote only)
Prompt: "Who am I in Figma?"  → calls whoami tool
```

### Common Mistakes
- Assuming the desktop server works without a paid Dev/Full seat — it requires one
- Using the desktop SSE endpoint (`/sse`) instead of the current HTTP endpoint (`/mcp`) — Figma updated this; use `/mcp` for both
- Expecting the remote server to read your active Figma selection — it cannot; it needs a link
- Treating MCP output as production-ready code without reviewing against design — treat it as a strong first draft

### See Also
- [Remote Server Setup](remote-server-setup.md) | [Desktop Server Setup](desktop-server-setup.md)
- Reference: https://developers.figma.com/docs/figma-mcp-server/
