---
description: Extract design tokens and variable names from Figma for token-aware code generation using get_variable_defs
---

# Design Tokens and Variables

### When to Use
When generating code that should reference design system tokens (colors, spacing, typography, border radius) by name rather than hardcoded values. Requires variables to be defined in Figma's Variables panel and applied to elements in the design.

### Decision
| If you need... | Use... | Why |
|---|---|---|
| All tokens used in a frame | `get_variable_defs` with frame link/selection | Returns only tokens actually used |
| Specific token type | `get_variable_defs` with type filter | Scopes output to COLOR, FLOAT, STRING, or BOOLEAN |
| Token names in generated code | Reference in prompt after fetching | Agent uses token names not raw hex/px values |

### Pattern
```
# Fetch tokens first
"Get the variable names and values used in my current selection"
→ agent calls get_variable_defs, lists token names and values

# Then reference them in generation
"Generate this component using the token names you just retrieved"
→ agent uses --color-primary, --spacing-4, etc. in generated code

# Combined single-prompt approach
"Generate [figma-link] using our design tokens — fetch variable names first"
```

### Common Mistakes
- Using `get_variable_defs` when Figma elements have unlinked fills — the tool only returns linked variables, not raw fill values
- Generating code before fetching tokens — agent may hardcode hex values instead of token references
- Expecting CSS custom property names from Figma — Figma variable names need mapping to your CSS token naming convention; add this to your custom rules file

### See Also
- [Design Context Extraction](design-context-extraction.md) | [Code Connect Integration](code-connect-integration.md)
- Reference: https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/
