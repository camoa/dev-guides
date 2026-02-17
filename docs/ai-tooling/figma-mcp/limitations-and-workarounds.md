---
description: Known limitations of Figma MCP code generation — token limits, no visual iteration, missing states, selection-only desktop — and practical workarounds for each
---

# Limitations and Workarounds

### When to Use
When you hit a wall — token limits, unexpected output, or workflow gaps. Understanding limitations prevents frustration and helps you find the right workaround.

### Items

#### No Iterative Visual Refinement
**Limitation:** The AI cannot see the rendered output it generates and adjust it. Once code is generated, the visual feedback loop ends — you cannot say "make the button slightly larger" and have the agent visually verify the change.

**Workaround:** Use `get_screenshot` before generation to establish visual ground truth. Review generated code against the screenshot manually. For visual adjustments, edit the code directly or return to Figma, update the design, and regenerate.

---

#### Multi-Frame and Multi-Section Pages
**Limitation:** Complex pages with many sections produce unreliable output when generated as a single `get_design_context` call. Context window overflow causes truncation or loss of detail in later sections.

**Workaround:**
```
1. Use get_metadata to map the page structure
2. Generate each section individually with its own get_design_context call
3. Prompt to assemble sections: "Combine HeroSection, FeaturesGrid, and Footer
   into a single page component"
```

---

#### Token Context Window Limits
**Limitation:** Very large frames — full-page layouts, data tables, complex dashboards — can exceed the model's context window when `get_design_context` returns the full representation.

**Workaround:**
```
1. get_metadata first → identify sub-node IDs
2. get_design_context on specific node IDs → targeted extraction
3. Process sections sequentially rather than all at once
```

---

#### Selection-Based Workflow Desktop-Only
**Limitation:** The remote server cannot read active Figma selections. If you're on the remote server (or VS Code/Cursor without the desktop app), you must copy frame links.

**Workaround:** Use the link-based workflow. Right-click any frame → Copy link to selection. The node ID in the URL is extracted automatically by the MCP server.

---

#### Design Updates Require Regeneration
**Limitation:** When a Figma design evolves after initial code generation, the agent cannot surgically update the existing component. Regeneration often produces a full replacement rather than a diff-based edit.

**Workaround:**
- For small changes (color, spacing): edit code directly using token references
- For structural changes: regenerate the component and diff against the existing version
- Code Connect reduces this problem — connected components import real implementations that may already handle the change

---

#### Generated Code Missing States
**Limitation:** MCP output reflects the Figma frame's visible state. Hover states, error states, loading states, empty states, and animation are not present in static designs and will not appear in generated code.

**Workaround:**
- Add Figma annotations describing behavior (right-click → Add annotation in Dev Mode)
- Include behavioral notes in your custom rules file
- Review generated output for missing states and add them manually

---

### Common Mistakes
- Regenerating a component for every minor design change — for cosmetic changes, edit the token reference directly
- Generating a full page in one prompt — always break complex pages into sections
- Assuming generated code is production-ready without review — accessibility, error states, and performance (image optimization, lazy loading) require manual validation

### See Also
- [Best Practices and Patterns](best-practices-and-patterns.md) | [Figma MCP Overview](figma-mcp-overview.md)
- Reference: https://www.builder.io/blog/claude-code-figma-mcp-server
