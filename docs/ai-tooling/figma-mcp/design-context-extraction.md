---
description: Use get_design_context to convert Figma frames into structured data for AI code generation — patterns for link-based and selection-based workflows
---

# Design Context Extraction

### When to Use
Every code generation session starts here. `get_design_context` is the core tool — it converts Figma's visual representation into structured data AI agents can translate into code.

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Full layout, component structure, styles | `get_design_context` (default) | Complete representation for code generation |
| Large frame that may exceed context | `get_metadata` first, then targeted `get_design_context` | Metadata identifies sub-nodes to fetch individually |
| Visual reference alongside structure | `get_design_context` + `get_screenshot` | Structural + visual = highest accuracy |
| Framework-specific output | Prompt with framework name | Default is React + Tailwind |
| Component reuse from codebase | Specify component path in prompt | Agent maps Figma components to your files |

### Pattern
```
# Link-based (remote or desktop server)
"Generate [figma-link] in plain HTML and CSS"
"Implement [figma-link] using components from src/components/ui/"
"Generate [figma-link] in Vue using our design tokens"

# Selection-based (desktop server only)
"Implement my current Figma selection in React"
"Generate the selected frame using Tailwind utility classes"

# Targeted extraction for large frames
"Get the metadata for [figma-link] first, then generate only the hero section"
```

### Common Mistakes
- Not specifying a framework — agent defaults to React + Tailwind regardless of your stack
- Asking to "generate the whole page" when the frame is complex — break large pages into sections and generate each individually
- Expecting pixel-perfect output on the first pass — MCP output is a strong starting point, not a final implementation

### See Also
- [Available Tools Reference](available-tools-reference.md) | [Design Tokens and Variables](design-tokens-and-variables.md)
- Reference: https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/
