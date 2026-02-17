---
description: Map Figma components to existing codebase files using Code Connect so AI agents reuse real implementations instead of regenerating them
---

# Code Connect Integration

### When to Use
When your codebase has existing component implementations you want AI agents to reuse rather than regenerate. Code Connect maps Figma components to actual code files, so generated code imports and uses your real components.

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Simple path mapping (fastest setup) | Code Connect UI (Figma inspect panel) | Link component to file path without CLI tooling |
| Rich implementation snippets | Code Connect CLI | Provides actual usage examples with prop mappings |
| View existing mappings | `get_code_connect_map` | Returns node ID → file path object |
| Create mappings from agent | `add_code_connect_map` | Agent writes mappings during a "connect components" session |
| Detect mapping opportunities | `get_code_connect_suggestions` | Agent analyzes design and codebase for matches |

### Pattern
**Setup via Figma UI:**
```
1. Select component in Figma inspect panel
2. Find "Code" section → "Connect code"
3. Paste file path: src/components/Button.tsx
4. Add component name: Button
5. Optionally: Add MCP instructions (usage patterns, accessibility notes)
```

**Setup via agent workflow:**
```
"Connect my Figma components to code. Check src/components/ for matches."
→ agent calls get_code_connect_suggestions
→ agent reviews matches with you
→ agent calls send_code_connect_mappings to confirm
```

**Using connected components in generation:**
```
"Generate my current Figma selection using components from my codebase"
→ agent calls get_code_connect_map + get_design_context
→ output uses import { Button } from 'src/components/Button' not a reimplementation
```

### Common Mistakes
- Mapping every component immediately — prioritize frequently-used components (buttons, inputs, cards) first; low-usage components can be generated fresh
- Using CLI setup when UI setup is sufficient — UI mapping is faster for most teams; CLI adds value when you need prop mapping examples
- Forgetting to enable Code Connect in desktop server settings — toggle it in the inspect panel MCP server section
- Expecting `get_code_connect_map` to work on the remote server without Code Connect configured — it returns empty without mappings

### See Also
- [Design Tokens and Variables](design-tokens-and-variables.md) | [Screenshots and Metadata](screenshots-and-metadata.md)
- Reference: https://developers.figma.com/docs/figma-mcp-server/code-connect-integration/
- Reference: https://help.figma.com/hc/en-us/articles/23920389749655-Code-Connect
