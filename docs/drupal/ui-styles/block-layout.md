---
description: "Apply curated UI Styles to blocks placed via Drupal's core Block layout UI."
tldr: "Enable ui_styles_block; each block's configuration form gains a UI Styles fieldset. Selections persist in block config entity third-party settings under ui_styles_block.selected and are injected into #attributes['class'] at render time."
drupal_version: "11.x"
---

# Integration: Block Layout

## When to Use

> Use this guide when letting site builders apply curated styles to blocks placed via the core Block layout (`/admin/structure/block`).

## Pattern

Enable `ui_styles_block`. Each block's "Configure block" form gains a **UI Styles** fieldset with all active styles grouped by category. Selections persist in the block configuration entity's third-party settings:

```yaml
# config/sync/block.block.my_block.yml (excerpt)
third_party_settings:
  ui_styles_block:
    selected:
      text_color: "text-primary"
      spacing: "p-4"
    extra: "my-custom-class"
```

At render time, `hook_preprocess_block()` merges the selected classes into `#attributes['class']`.

`extra` is a freeform "additional CSS classes" textbox — stored verbatim, no validation.

## Common Mistakes

- **Deleting a style definition while blocks reference it** → Orphaned `selected` entries persist silently and render as empty/nonexistent classes. Audit before removing styles in production
- **Using `extra` for everything** → Defeats the purpose of curated UI Styles. Use it only for one-off overrides

## See Also

- [Integration: Layout Builder](layout-builder.md)
- [Anti-Patterns](anti-patterns.md)
- Reference: `modules/ui_styles_block/` in the UI Styles module
