---
description: Choose between selection-based workflow (desktop server, no link copying) and link-based workflow (remote or desktop server) for Figma design context
---

# Selection vs Link Workflows

### When to Use
Every Figma MCP session requires choosing how to provide design context. This decision affects which server type you need and how fluid your workflow feels.

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Select in Figma → immediately generate | Selection-based (desktop server) | No link copying; works with active selection |
| Work from any client without desktop app | Link-based (remote or desktop server) | Copy link → paste → agent fetches |
| Multiple disconnected frames at once | Link-based with multiple links | Paste multiple links in one prompt |
| Quick iteration on selected frame | Selection-based | Fastest loop; no context-switching |
| Share a specific design state with team | Link-based | Links capture a specific frame state |

### Pattern
```
# Selection-based (desktop server required)
1. Select frame or layers in Figma desktop app
2. Switch to editor
3. Prompt: "Implement my current Figma selection in [framework]"
   → agent calls get_design_context using active selection

# Link-based (remote or desktop server)
1. In Figma: Right-click frame → Copy link to selection
   (or: Share → Copy link, then add ?node-id=... for specific frame)
2. Paste link in prompt: "Generate [pasted-link] in [framework]"
   → agent extracts node-id from URL and calls get_design_context

# Multi-frame workflow (link-based)
"Generate each of these sections individually:
 Header: [link1]
 Features: [link2]
 Footer: [link3]
 Then combine them into a single page component"
```

### Common Mistakes
- Pasting a page-level URL instead of a frame-specific link — page links don't include a node ID; right-click the specific frame to get a frame link
- Expecting selection-based workflow on the remote server — it only works with the desktop server running
- Selecting a frame group and a nested element simultaneously — select the top-level frame only; nested selections confuse the tool

### See Also
- [Design System Rules](design-system-rules.md) | [Prompting Strategies](prompting-strategies.md)
- Reference: https://developers.figma.com/docs/figma-mcp-server/
