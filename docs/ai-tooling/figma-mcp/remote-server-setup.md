---
description: Set up the Figma MCP remote server in Claude Code, VS Code, Cursor, or Windsurf — no desktop app required
---

# Remote Server Setup

### When to Use
Starting point for most developers. No Figma desktop app required. Works on all plans and seat types. Use this when setting up Claude Code, VS Code, Cursor, or Windsurf.

### Steps

1. **Add the server to your client**

   **Claude Code (terminal):**
   ```bash
   # Project-scoped (default)
   claude mcp add --transport http figma https://mcp.figma.com/mcp

   # User-scoped (available across all projects)
   claude mcp add --transport http --scope user figma https://mcp.figma.com/mcp
   ```

   **VS Code (`mcp.json`):**
   ```json
   {
     "servers": {
       "figma": {
         "url": "https://mcp.figma.com/mcp",
         "type": "http"
       }
     }
   }
   ```
   Access via: `⌘ Shift P` → `MCP: Open User Configuration` (global) or `MCP: Open Workspace Folder MCP Configuration` (project).

   **Cursor:**
   Navigate to `Settings → Cursor Settings → MCP tab → Add new global MCP server`. Use the same JSON structure as VS Code, or use the Figma deep link from the Figma developer docs.

   **Windsurf / other clients:**
   Use the standard `mcpServers` format pointing to `https://mcp.figma.com/mcp` with type `http`.

2. **Authenticate**

   **Claude Code:** Start a new session → type `/mcp` → select `figma` → choose `Authenticate` → click `Allow Access` in the browser popup.

   **VS Code:** Click `Start` above the MCP server name → click `Allow Access`.

   **Cursor:** Click `Connect` next to Figma → `Open` → grant access permissions.

3. **Verify the connection**

   ```bash
   # Claude Code
   /mcp   # should show figma as connected

   # Any client — ask the agent:
   "Who am I in Figma?"   # calls whoami, returns your email and seat type
   ```

4. **Provide design context via link**

   Copy a frame or layer link from Figma (`Right-click → Copy link to selection` or `Copy link to frame`). Paste the link into your prompt — the MCP server extracts the node ID automatically.

### Decision Points
| At this step... | If... | Then... |
|---|---|---|
| Choosing scope in Claude Code | Need Figma in all projects | Add `--scope user` flag |
| Authentication fails | Switching Figma accounts | Sign out of Figma in browser, re-authenticate |
| Getting 403 on file access | File not shared with your account | Request view access from file owner |

### Common Mistakes
- Running the old Claude Code SSE command (`--transport sse`) — the current command uses `--transport http`
- Forgetting to start a new Claude Code session after adding the server — the server loads at session start
- Sharing a page link instead of a frame/layer link — use `Copy link to selection` to get a node-specific link

### See Also
- [Figma MCP Overview](figma-mcp-overview.md) | [Desktop Server Setup](desktop-server-setup.md)
- Reference: https://developers.figma.com/docs/figma-mcp-server/remote-server-installation/
