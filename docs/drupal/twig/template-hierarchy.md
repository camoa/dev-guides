---
topic: drupal/twig
guide: template-hierarchy
---

## Template Hierarchy

### When to Use
When you need to understand the full rendering chain — which template wraps which — and where to override at each level.

### Decision
| Level | Template | Controls |
|---|---|---|
| 1. Document | `html.html.twig` | `<html>`, `<head>`, `<body>` wrapper |
| 2. Page | `page.html.twig` | Header, footer, region layout |
| 3. Region | `region.html.twig` | Individual region wrapper |
| 4. Block | `block.html.twig` | Block wrapper, label, content slot |
| 5. Node | `node.html.twig` | Article/content wrapper, fields via `content` |
| 6. Field | `field.html.twig` | Field label + items loop |
| 7. Views | `views-view.html.twig` | View header/rows/footer/pager |

This is a containment hierarchy, not strict parent-child HTML. A block in the header region contains its own rendering pipeline, independent of the node pipeline on the page.

### Pattern
```
html.html.twig
  └── page.html.twig
        ├── region.html.twig (header, content, footer, etc.)
        │     └── block.html.twig (each block in region)
        └── [page.content region]
              └── node.html.twig (if page is a node)
                    └── field.html.twig (each displayed field)
```

**Key insight:** `page.html.twig` receives `{{ page.content }}` which contains the node render array. The node template renders when that array is processed. You can override at any level — override `page.html.twig` for layout changes, `node.html.twig` for content changes, `field.html.twig` for field presentation.

### Common Mistakes
- Overriding `page.html.twig` when you only need to change a node field → override `node.html.twig` instead
- Expecting `node` variable in `page.html.twig` for all pages → it's only set when the route parameter is a node
- Trying to access field values in `block.html.twig` → block content is in `content`, not a field array

### See Also
- Variables at each level → [Variables by Template Level](variables-by-template-level.md)
- Core templates: `core/modules/system/templates/`, `core/modules/node/templates/`
