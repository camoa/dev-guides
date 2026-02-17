---
description: Generate a persistent design system rules file using create_design_system_rules to align AI agent behavior with your tech stack across all sessions
---

# Design System Rules

### When to Use
At the start of a project or after onboarding a new design system. `create_design_system_rules` generates a persistent rules file that tells your AI agent how to translate designs in your specific technology stack — component preferences, token usage, file organization, naming conventions.

### Steps

1. **Generate the rules file**
   ```
   "Create design system rules for this project.
    We use React, Tailwind v4, and components from src/components/.
    Save the rules to rules/figma-rules.md"
   ```
   Agent calls `create_design_system_rules` and writes the output file.

2. **Review and customize the generated file**
   Open `rules/figma-rules.md` and verify/add:
   - Component import paths
   - Token naming conventions (Figma token names → CSS custom property names)
   - File placement rules (`src/components/marketing/` vs `src/components/ui/`)
   - Layout primitives preference (flexbox, grid, absolute)
   - Things to never do (hardcode colors, use inline styles, recreate existing components)

3. **Commit the rules file to version control**
   The file becomes part of your project. AI agents in Claude Code read files from your project directory on startup or when referenced in prompts.

4. **Reference in prompts (Claude Code)**
   ```
   "Following our rules in rules/figma-rules.md, implement this design: [link]"
   ```

### Decision Points
| At this step... | If... | Then... |
|---|---|---|
| Choosing rules file location | Using Claude Code | `rules/` or `.claude/` directory |
| Choosing rules file location | Using Cursor | `.cursorrules` or `.cursor/rules/` directory |
| Rules need updating | Design system evolves | Re-run `create_design_system_rules` and diff against existing file |

### Common Mistakes
- Running `create_design_system_rules` without specifying your stack — the generated rules will be generic React + Tailwind defaults
- Not committing the rules file — rules only persist if they're in version control and referenced in prompts
- Treating generated rules as final — always review and add project-specific conventions the agent cannot infer

### See Also
- [FigJam and Diagram Tools](figjam-and-diagram-tools.md) | [Selection vs Link Workflows](selection-vs-link-workflows.md)
- Reference: https://github.com/figma/mcp-server-guide
