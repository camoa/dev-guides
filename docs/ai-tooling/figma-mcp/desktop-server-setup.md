---
description: Set up the Figma MCP desktop server for selection-based workflow — requires Dev or Full seat on a paid plan
---

# Desktop Server Setup

### When to Use
When you want selection-based workflow: select frames in Figma, then prompt your agent to implement your current selection — no link copying needed. Requires Dev or Full seat on a paid Figma plan.

### Steps

1. **Enable the desktop MCP server in Figma**
   - Open Figma desktop app (update to latest version)
   - Open or create a Design file
   - Toggle to Dev Mode (`Shift D`)
   - In the inspect panel's MCP server section, click `Enable desktop MCP server`
   - Confirmation message appears when active
   - The server runs at `http://127.0.0.1:3845/mcp`

2. **Configure image handling (optional)**
   In the inspect panel MCP server section, choose:
   - `Local server` — serves images via localhost links
   - `Download assets` — extracts assets directly to your project directory (recommended for code generation)
   - `Placeholders` — deprecated, avoid

3. **Connect your editor**

   **Claude Code (terminal):**
   ```bash
   claude mcp add --transport http figma-desktop http://127.0.0.1:3845/mcp
   ```

   **VS Code:**
   `⌘ Shift P` → `MCP: Add Server` → `HTTP` → enter `http://127.0.0.1:3845/mcp` → set ID as `figma-desktop`. Requires GitHub Copilot enabled and Agent mode active (`⌥⌘B` or `⌃⌘I`).

   **Cursor:**
   `Settings → MCP tab → Add new global MCP server`:
   ```json
   {
     "figma-desktop": {
       "url": "http://127.0.0.1:3845/mcp",
       "type": "http"
     }
   }
   ```

4. **Use selection-based workflow**

   In Figma, select one or more frames or layers. Then in your editor:
   ```
   "Implement my current Figma selection using React and Tailwind"
   "Generate the selected component using files in src/components/"
   ```

### Decision Points
| At this step... | If... | Then... |
|---|---|---|
| Enabling server | No Dev Mode toggle visible | Confirm you have Dev or Full seat on a paid plan |
| Image assets needed in project | Using downloaded images in code | Choose `Download assets` in image handling settings |
| Running both remote and desktop | Need both link and selection workflows | Add both servers with different IDs (`figma` and `figma-desktop`) |

### Common Mistakes
- Running the desktop server without keeping the Figma desktop app open — the server stops when the app closes
- Using the old SSE endpoint path (`/sse`) — current endpoint is `/mcp`
- Selecting deeply nested layers instead of top-level frames — select the frame, not individual elements inside it

### See Also
- [Remote Server Setup](remote-server-setup.md) | [Claude Code Plugin](claude-code-plugin.md)
- Reference: https://developers.figma.com/docs/figma-mcp-server/local-server-installation/
