---
description: UI Patterns Security & Accessibility — XSS protection, block filtering, attributes
drupal_version: "11.x"
---

# Security & Accessibility

## When to Use

> Reference this guide when defining string props that may carry user input, choosing between slots and props for rich text, or ensuring components work with Drupal's accessibility tooling.

## Decision

| Content | Safe Approach |
|---------|--------------|
| User-visible text that should never contain HTML | `type: string` + `contentMediaType: text/plain` (applies `strip_tags()`) |
| Rich text content | Use a slot with WYSIWYG source |
| HTML from a trusted/sanitized source | `contentMediaType: text/html` (passes through `Markup::create()`) |
| Arbitrary HTML attributes | `attributes` prop (Drupal's `Attribute` class escapes values) |

## Pattern

### Prop sanitization via `contentMediaType`

```yaml
# For plain text — strip_tags() applied automatically
description:
  title: "Description"
  type: "string"
  contentMediaType: "text/plain"

# For rich text — use a slot instead of a string prop
slots:
  body:
    title: "Body content"
```

### XSS protection chain

- **`text/plain` string props**: `strip_tags()` applied during `normalize()`
- **`text/html` string props**: `Markup::create()` applied during `preprocess()` — only use on already-sanitized content
- **Slot content**: passes through Drupal's render API with Twig autoescape
- **Token replacement**: `Token::replacePlain()` for non-markup; `Token::replace(['clear' => TRUE])` for markup

### Block source security — excluded from slots

- `inline_block` — prevents config-to-content dependencies
- `system_main_block`, `page_title_block` — Layout Builder convention
- `layout_builder` and `ui_patterns_blocks` provider blocks — prevents recursion

### Accessibility checklist

- Always apply `{{ attributes }}` on wrapper elements — accessibility tools inject `aria-*` attributes through this
- Provide meaningful `title` values for all props and slots (become form labels)
- Use semantic HTML in component templates — UI Patterns does not enforce semantics
- Mark decorative slots as optional — required slots that may be empty create broken layouts for assistive technology users
- Attach JavaScript via the Drupal library system, not inline scripts (CSP compliance)

## Common Mistakes

- **Wrong**: `Markup::create()` on raw user input → **Right**: Only use it on already-sanitized content; it bypasses Twig's autoescape
- **Wrong**: Skipping `{{ attributes }}` on the wrapper element → **Right**: Drupal modules that add `data-*` attributes for contextual links and accessibility features will silently fail
- **Wrong**: Not setting `contentMediaType: text/plain` for plain text props → **Right**: Without it, string props allow HTML, which may be unexpected for user input

## See Also

- [Best Practices & Anti-Patterns](best-practices-and-anti-patterns.md)
- Reference: [Drupal Security Guide](../security/index.md)
