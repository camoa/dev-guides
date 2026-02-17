---
description: Use get_screenshot for visual ground truth and get_metadata to navigate large Figma frames without exceeding context limits
---

# Screenshots and Metadata

### When to Use
Two complementary tools for handling cases where `get_design_context` alone is insufficient: screenshots provide visual ground truth; metadata provides structure without weight for large frames.

### Decision
| If you need... | Use... | Why |
|---|---|---|
| Visual reference alongside code generation | `get_screenshot` | Layout fidelity check; reduces misinterpretation of structure |
| Identify node IDs in a large frame | `get_metadata` | Sparse XML without styling data; cheap on token usage |
| Navigate a complex design before generating | `get_metadata` first | Map the layer hierarchy, then target specific nodes |
| FigJam diagram content | `get_figjam` | Returns metadata XML + screenshots for FigJam nodes |

### Pattern
```
# Large frame workflow
"Get metadata for [figma-link] to understand its structure"
→ agent returns XML layer hierarchy with node IDs

"Now generate only the HeroSection node (ID: 123:456) in React"
→ agent calls get_design_context with specific node ID

# Visual accuracy workflow
"Get a screenshot of [figma-link] and then generate the HTML"
→ agent captures screenshot + calls get_design_context
→ uses visual reference to validate layout decisions
```

### Common Mistakes
- Skipping `get_metadata` on complex pages — going straight to `get_design_context` on a 50-element page wastes tokens and often returns truncated results
- Using `get_screenshot` without `get_design_context` — the screenshot alone gives the agent less structured information; use both
- Forgetting `get_figjam` exists for FigJam files — using `get_design_context` on a FigJam link will fail; the tool is FigJam-specific

### See Also
- [Code Connect Integration](code-connect-integration.md) | [FigJam and Diagram Tools](figjam-and-diagram-tools.md)
- Reference: https://developers.figma.com/docs/figma-mcp-server/tools-and-prompts/
