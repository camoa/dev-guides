---
description: Read FigJam architecture diagrams and user flows with get_figjam, or generate new FigJam diagrams from Mermaid syntax using generate_diagram
---

# FigJam and Diagram Tools

### When to Use
When your workflow involves FigJam diagrams — architecture maps, user flows, process diagrams — or when you want to generate new FigJam diagrams from code or descriptions.

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Read existing FigJam diagram | `get_figjam` | Converts FigJam content to XML + screenshots |
| Create a new diagram from description | `generate_diagram` | Natural language or Mermaid → FigJam file |
| Use flow diagram as implementation reference | `get_figjam` + summarize prompt | Extracts diagram intent for developer context |

### Pattern
```
# Extract FigJam content
"Get the user registration flow from this FigJam: [link]"
→ agent calls get_figjam, returns XML structure + node screenshots
→ use as reference for implementing the described flow

# Generate a new diagram
"Create a sequence diagram for our API authentication flow in Mermaid syntax
and save it to our FigJam file: [figma-file-link]"
→ agent calls generate_diagram with Mermaid input
→ diagram appears in FigJam file

# Supported Mermaid types
flowchart LR, sequenceDiagram, stateDiagram-v2, gantt
```

### Common Mistakes
- Using `get_design_context` on a FigJam link — it will fail or return empty; use `get_figjam` for FigJam files
- Treating FigJam output as implementation-ready specs — FigJam diagrams are planning artifacts; use them for flow reference, not pixel-precise layouts
- Omitting a target FigJam file when generating diagrams — `generate_diagram` needs a destination file URL

### See Also
- [Screenshots and Metadata](screenshots-and-metadata.md) | [Design System Rules](design-system-rules.md)
- Reference: https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/
