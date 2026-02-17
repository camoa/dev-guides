---
description: Prompt patterns for getting accurate framework-targeted code output from Figma MCP tools — framework targeting, component reuse, file placement, and multi-step workflows
---

# Prompting Strategies

### When to Use
When you want to get better code output from the MCP tools. Prompt specificity directly correlates with output quality — vague prompts produce generic React + Tailwind regardless of your stack.

### Decision
| Goal | Prompt pattern | Example |
|---|---|---|
| Framework targeting | "Generate [link] in [framework]" | "Generate [link] in plain HTML + CSS" |
| Component reuse | "Generate using components from [path]" | "...using components from src/components/ui" |
| File placement | "Add this to [file path]" | "Add this to src/components/marketing/PricingCard.tsx" |
| Design system adherence | "Following rules/figma-rules.md, generate..." | Reference your rules file explicitly |
| Token extraction first | "Fetch variables first, then generate" | Two-step prompt for token-aware output |
| Visual validation | "Get a screenshot and then generate" | Forces visual reference before code |
| Explicit tool trigger | "Get the variable names used in [link]" | Triggers get_variable_defs specifically |
| Code Connect reuse | "Generate using components from my codebase" | Triggers get_code_connect_map lookup |

### Pattern
```
# Minimal effective prompt
"Generate [figma-link] in React using components from src/components/"

# Full-fidelity prompt
"Following our design system rules in rules/figma-rules.md:
 1. Get a screenshot of [figma-link] for visual reference
 2. Fetch variable names used in the frame
 3. Generate the component in React using Tailwind v4
 4. Use existing components from src/components/ui/
 5. Place the output in src/components/marketing/HeroSection.tsx"

# Framework alternatives
"Generate [link] in Vue 3 with Composition API"
"Generate [link] in plain HTML + CSS (no framework)"
"Generate [link] in iOS SwiftUI"
```

### Common Mistakes
- Writing open-ended prompts like "implement this design" — always specify framework, component paths, and output file location
- Chaining too many design system constraints in one prompt — agents lose specifics in long prompts; use a rules file instead for persistent constraints
- Not specifying where to place the output file — agents may create files in unexpected locations
- Generating the entire page at once — complex pages produce better results when each section is generated and validated individually

### See Also
- [Selection vs Link Workflows](selection-vs-link-workflows.md) | [Figma File Best Practices](figma-file-best-practices.md)
- Reference: https://github.com/figma/mcp-server-guide
