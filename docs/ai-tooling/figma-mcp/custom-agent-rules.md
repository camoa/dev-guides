---
description: Create and maintain a project-level rules file for consistent AI agent behavior across all Figma-to-code sessions — component imports, token mapping, file placement, and workflow constraints
---

# Custom Agent Rules

### When to Use
When you want consistent AI agent behavior across all Figma-to-code sessions in a project — same component imports, same token naming conventions, same file placement rules. Rules files persist between sessions and prevent agents from reverting to generic defaults.

### Steps

1. **Generate a starting point**
   ```
   "Create design system rules for this project and save to rules/figma-rules.md"
   ```

2. **Add project-specific workflow rules**
   In your rules file, include a numbered workflow section:
   ```markdown
   ## Figma-to-Code Workflow

   1. Call get_design_context first to get the structured representation
   2. If the response is truncated, call get_metadata to identify sub-nodes,
      then re-call get_design_context on specific node IDs
   3. Call get_screenshot for visual reference before generating layout code
   4. Download or reference assets before beginning implementation
   5. Translate token names from Figma variables to our CSS custom property names:
      - Figma "Color/Primary" → --color-primary
      - Figma "Spacing/4" → --spacing-4
   6. Reuse existing components from src/components/ before creating new ones
   7. Validate generated output against the screenshot — flag divergences
   8. Treat MCP output as design/behavior intent, not final code style
   ```

3. **Add "never do" rules**
   ```markdown
   ## Constraints

   - Never hardcode hex color values — always use CSS custom properties
   - Never recreate existing components from src/components/ui/
   - Never use inline styles
   - Never use absolute positioning unless the design explicitly shows overlapping elements
   - Never generate code without first checking Code Connect mappings
   ```

4. **Reference rules in prompts**
   ```
   "Following rules/figma-rules.md, implement my current Figma selection"
   ```

### Common Mistakes
- Writing rules that conflict with each other — review the full file after editing to check for contradictions
- Making rules too prescriptive about code style — rules should cover design-system alignment, not code formatting (use your linter for that)
- Forgetting to version control the rules file — treat it like project configuration

### See Also
- [Figma File Best Practices](figma-file-best-practices.md) | [Rate Limits and Access Tiers](rate-limits-and-access-tiers.md)
- Reference: https://github.com/figma/mcp-server-guide
