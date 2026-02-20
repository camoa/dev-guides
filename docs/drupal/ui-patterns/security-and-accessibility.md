---
description: Security and accessibility — XSS protection, sanitization, and a11y considerations
drupal_version: "10.3+ / 11"
---

## Security & Accessibility

### XSS Protection

UI Patterns inherits SDC's rendering pipeline, which means:

- **String props** with `contentMediaType: text/html` pass through `Markup::create()` during preprocessing, marking them as safe HTML. Ensure the source data is already sanitized.
- **String props** with `contentMediaType: text/plain` are run through `strip_tags()` during normalization, providing automatic XSS protection.
- **Slot content** passes through Drupal's render API, which auto-escapes by default via Twig's autoescape.
- **Token replacement** uses `Token::replacePlain()` for non-markup contexts and `Token::replace()` with `['clear' => TRUE]` for markup, preventing unresolved tokens from appearing.

### Sanitization Best Practices

```yaml
# For user-visible text that should never contain HTML:
description:
  title: "Description"
  type: "string"
  contentMediaType: "text/plain"   # strip_tags() applied

# For rich text content:
# Use a slot instead of a string prop
slots:
  body:
    title: "Body content"
```

### Block Source Security

The `BlockSource` filters dangerous blocks via `hook_plugin_filter_block__ui_patterns_alter()`:
- `inline_block` is excluded (prevents config-to-content dependencies)
- `system_main_block` and `page_title_block` are excluded (Layout Builder convention)
- `layout_builder` and `ui_patterns_blocks` provider blocks are excluded (prevents recursion)

### Attributes and Injection

The `attributes` prop type accepts arbitrary key-value pairs. This is safe because Drupal's `Attribute` class escapes attribute values during rendering. However:

- Never pass `attributes` values directly into JavaScript contexts without escaping
- The `class_attribute` widget provides a safer interface for CSS-only attribute input

### Accessibility Considerations

- **Always use the `attributes` prop** on wrapper elements. Accessibility tools inject `aria-*` attributes through this mechanism.
- **Provide meaningful titles** for all props and slots. These become form labels for screen reader users configuring components.
- **Use semantic HTML** in component templates. UI Patterns does not enforce semantics; that responsibility stays with the component author.
- **Support keyboard navigation** in interactive components. UI Patterns handles the data layer; interaction patterns are the template's responsibility.
- **Mark decorative slots as optional** in the component definition. Required slots that may be empty create broken layouts for assistive technology users.

### Content Security Policy (CSP)

UI Patterns does not add inline scripts or styles. Components should follow the same CSP guidelines as any Drupal theme component. If a component needs JavaScript, attach it via the Drupal library system, not inline scripts.

### Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Using `Markup::create()` on user input | This marks content as safe, bypassing Twig's autoescape. Only use it on already-sanitized content. UI Patterns' StringPropType does this in `preprocess()` because normalization has already occurred. |
| Skipping `attributes` on the wrapper element | Drupal modules that add `data-*` attributes for contextual links, quick edit, and accessibility features will silently fail. |
| Not setting `contentMediaType: text/plain` for plain text props | Without it, string props allow HTML, which may be unexpected if the value comes from user input. |

### See Also

- Drupal Security Guide
- [Best Practices & Anti-Patterns](#best-practices--anti-patterns)