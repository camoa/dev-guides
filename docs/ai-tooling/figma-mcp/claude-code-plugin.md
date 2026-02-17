---
description: Install the Figma MCP server via the Claude Code plugin for the fastest setup with bundled design-to-code skills
---

# Claude Code Plugin

### When to Use
When you want the fastest Claude Code setup — one command installs the server and pre-built skills for common Figma workflows. The plugin bundles the MCP server with curated skill definitions.

### Steps

1. **Install the plugin**
   ```bash
   claude plugin install figma@claude-plugins-official
   ```

2. **Authenticate**
   Type `/mcp` in Claude Code → select figma → Authenticate → Allow Access.

3. **Use bundled skills**
   Skills are pre-built prompt workflows. In Claude Code, reference them by task:
   - `Connect design components to code` — walks through Code Connect mapping setup
   - `Generate design system rules` — runs `create_design_system_rules` and saves output

### Decision Points
| At this step... | If... | Then... |
|---|---|---|
| Plugin vs manual install | Want skills bundled | Use plugin install |
| Plugin vs manual install | Want explicit control over MCP config | Use manual `claude mcp add` command |
| After plugin install | Need desktop selection workflow | Also add the desktop server manually |

### Common Mistakes
- Expecting the plugin to replace the desktop server — it installs the remote server only; desktop still requires manual setup
- Skipping authentication after install — the plugin installs the server config but authentication is a separate step

### See Also
- [Desktop Server Setup](desktop-server-setup.md) | [Available Tools Reference](available-tools-reference.md)
- Reference: https://help.figma.com/hc/en-us/articles/32132100833559-Guide-to-the-Figma-MCP-server
