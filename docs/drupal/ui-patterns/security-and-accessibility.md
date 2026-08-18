---
description: Security and accessibility — XSS protection, sanitization, and a11y considerations
tldr: "Security and accessibility — XSS protection, sanitization, and a11y considerations"
drupal_version: "11.x"
---

# Security & Accessibility

## XSS Protection

UI Patterns inherits SDC's rendering pipeline, which means:

- **String props** are handled entirely in `StringPropType::normalize()`, and the default reversed after 2.0.15 (issue #3611167). A plain PHP string is now left untrusted and Twig autoescapes it at render. Only a `MarkupInterface` value passes through as safe HTML, and a render array is rendered through the render pipeline and then wrapped in `Markup::create()`. To emit raw HTML from a string prop, the source must return `Markup::create($html)` — and must have sanitized it first.
- **String props** with `contentMediaType: text/plain` are run through `strip_tags()`, unconditionally, even when the value arrives as `Markup`.
- **Slot content** passes through Drupal's render API, which auto-escapes by default via Twig's autoescape.
- **Token replacement** (`SourcePluginBase::replaceTokens()`) uses `Token::replace()` for markup contexts and `Token::replacePlain()` otherwise, both with `['clear' => TRUE]`, so unresolved tokens are stripped rather than printed.

## Sanitization Best Practices

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

## Block Source Security

The `BlockSource` filters dangerous blocks via `hook_plugin_filter_block__ui_patterns_alter()`:
- `inline_block` is excluded (prevents config-to-content dependencies)
- `system_main_block` and `page_title_block` are excluded (Layout Builder convention)
- `layout_builder` and `ui_patterns_blocks` provider blocks are excluded (prevents recursion)

## Attributes and Injection

The `attributes` prop type accepts arbitrary key-value pairs. This is safe because Drupal's `Attribute` class escapes attribute values during rendering. However:

- Never pass `attributes` values directly into JavaScript contexts without escaping
- Since 2.0.16 attribute values go through `Html::escape()` rather than `strip_tags()` (issue #3558573); escaping happens at render, in `Attribute::__toString()`
- For CSS-only input, use the `attributes` widget. The older `class_attribute` widget still exists but is **deprecated** (removed in 3.0.0, merged into `attributes`) and its form shows a deprecation warning — do not recommend it in new work

## Accessibility Considerations

- **Always use the `attributes` prop** on wrapper elements. Accessibility tools inject `aria-*` attributes through this mechanism.
- **Provide meaningful titles** for all props and slots. These become form labels for screen reader users configuring components.
- **Use semantic HTML** in component templates. UI Patterns does not enforce semantics; that responsibility stays with the component author.
- **Support keyboard navigation** in interactive components. UI Patterns handles the data layer; interaction patterns are the template's responsibility.
- **Mark decorative slots as optional** in the component definition. Required slots that may be empty create broken layouts for assistive technology users.

## Content Security Policy (CSP)

UI Patterns does not add inline scripts or styles. Components should follow the same CSP guidelines as any Drupal theme component. If a component needs JavaScript, attach it via the Drupal library system, not inline scripts.

## Common Mistakes

| Mistake | Why It Is Wrong |
|---|---|
| Using `Markup::create()` on user input | This marks content as safe, bypassing Twig's autoescape. Only use it on already-sanitized content. As of 2.0.19 `StringPropType` no longer wraps strings for you — wrapping is now an explicit decision the source makes, and the responsibility for sanitizing comes with it. |
| Skipping `attributes` on the wrapper element | Drupal modules that add `data-*` attributes for contextual links, quick edit, and accessibility features will silently fail. |
| Not setting `contentMediaType: text/plain` for plain text props | Without it, string props allow HTML, which may be unexpected if the value comes from user input. |

## See Also

- Drupal Security Guide
- [Best Practices & Anti-Patterns](best-practices-and-anti-patterns.md)