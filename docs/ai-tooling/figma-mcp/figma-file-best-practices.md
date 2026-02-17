---
description: Prepare Figma files for AI-assisted code generation — layer naming, components, variables, auto layout, and annotation practices that improve MCP output quality
---

# Figma File Best Practices

### When to Use
When preparing a Figma file for AI-assisted code generation. The quality of MCP output is directly proportional to how well the Figma file is structured. These practices apply before your team starts generating code.

### Decision
| If your Figma file has... | Impact on code generation |
|---|---|
| Semantic layer names (`CardContainer` vs `Group 5`) | Agents produce more accurate class names and component structure |
| Components for reusable elements | Code Connect can link to real implementations; agents detect reuse |
| Figma Variables applied to elements | `get_variable_defs` returns usable token names |
| Auto layout on frames | Agents infer flexbox/grid intent accurately |
| Deeply nested unnamed groups | Agents produce deeply nested, hard-to-maintain output |
| Hardcoded fill values (not variable-linked) | Agents hardcode hex/px values in generated code |

### Pattern
```
File structure checklist before AI generation:

Components:
- All reusable elements published as components (buttons, inputs, cards, nav items)
- Component variants use Figma's Variants feature, not duplicate frames
- Components linked to code via Code Connect for frequently-used items

Variables:
- Color tokens defined in Variables panel and applied to all fills/strokes
- Spacing tokens applied to padding, gap, and margin intent (via Auto layout)
- Typography tokens applied via Text styles or Variables

Layer naming:
- Top-level frames: PascalCase matching intended component name (HeroSection, PricingCard)
- Containers: semantic names (CardHeader, NavigationList, FormGroup)
- No: Group 1, Frame 234, Rectangle 12

Auto layout:
- Applied to all responsive frames
- Gap, padding, and direction set explicitly
- Constraints set on child elements for responsive behavior

Annotations:
- Add dev resource annotations for interaction behaviors (hover states, click handlers)
- Note any accessibility requirements (ARIA roles, keyboard behavior)
```

### Common Mistakes
- Using rasterized images instead of vector components for UI elements — agents cannot extract structural data from rasters
- Nesting Auto layouts 10+ levels deep — produces unnecessarily deep DOM trees in generated code; flatten where possible
- Having no Figma Variables — agents fall back to hardcoded values; token setup is the highest-ROI Figma investment for code generation quality
- Testing a complex frame for the first time without a simpler one first — validate MCP output quality on a simple card component before running a full page

### See Also
- [Prompting Strategies](prompting-strategies.md) | [Custom Agent Rules](custom-agent-rules.md)
- Reference: https://github.com/figma/mcp-server-guide
