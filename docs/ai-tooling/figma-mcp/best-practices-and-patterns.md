---
description: Sustainable design-to-code workflow patterns — session setup sequence, per-frame workflow, large frame handling, performance and security considerations
---

# Best Practices and Patterns

### When to Use
When setting up a sustainable design-to-code workflow. These practices apply across all clients and server types.

### Decision
| Scenario | Recommended approach |
|---|---|
| First session in a project | Generate rules file first, validate on a simple component, then tackle complex frames |
| Complex multi-section page | Generate each section individually, then assemble |
| Existing component library | Set up Code Connect before generating any code |
| Design system with tokens | Run `get_variable_defs` before first `get_design_context` call |
| Unfamiliar Figma file | Run `get_metadata` to map structure before generating code |

### Pattern

**Optimal session sequence:**
```
Session setup (once per project):
1. whoami → verify account and seat type
2. create_design_system_rules → save to rules/figma-rules.md
3. get_code_connect_suggestions → establish component mappings

Per-frame workflow:
1. get_screenshot → visual reference
2. get_variable_defs → token names
3. get_design_context → structured layout data
4. Generate code referencing tokens and mapped components
5. Validate output against screenshot

Large frame workflow:
1. get_metadata → identify node hierarchy and sub-node IDs
2. get_screenshot → visual reference for the full frame
3. get_design_context on specific sub-nodes → targeted extraction
4. Assemble generated sections
```

### Performance Considerations
- Each tool call counts against your rate limit — batch decisions before starting (know your framework, component paths, and output location before prompting)
- `get_design_context` on deeply nested frames is the most expensive call — use `get_metadata` to scope before calling
- Avoid calling `get_screenshot` + `get_design_context` + `get_variable_defs` separately when a single well-structured prompt triggers all three in sequence

### Security Considerations
- The MCP server accesses only Figma files your account has permission to view or edit — the server enforces Figma's own access controls
- Personal access tokens (if used in older setups) should be stored as environment variables, never hardcoded in config files
- OAuth authentication (current standard) is scoped to your Figma account — shared workstations should use separate authentication per user
- Rules files committed to version control should not contain account-specific paths or credentials

### Development Standards
- Treat generated code as a starting draft — review for accessibility (ARIA roles, focus management, semantic HTML) before committing
- Generated code rarely handles edge cases (empty states, error states, loading states) — add these manually
- Do not generate code from low-fidelity wireframes — MCP output quality scales directly with design completeness
- Run your linter/formatter on generated code before reviewing — auto-fix style issues before evaluating logic

### See Also
- [Rate Limits and Access Tiers](rate-limits-and-access-tiers.md) | [Limitations and Workarounds](limitations-and-workarounds.md)
- Reference: https://github.com/figma/mcp-server-guide
