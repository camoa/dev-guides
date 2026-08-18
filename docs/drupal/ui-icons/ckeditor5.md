---
description: "Embed icons inline in CKEditor 5 body text via the drupal-icon tag and icon_embed filter."
tldr: "Enable ui_icons_ckeditor5 + ui_icons_text, add the Icon toolbar button and Embed icon filter to a text format. The passthrough attributes land on a wrapper <span>, not the pack's own markup, and aria-hidden=\"false\" inverts to a bare aria-hidden — omit it instead."
drupal_version: "11.x"
---

# CKEditor 5 Integration

## When to Use

> Letting authors embed icons inline in body text (e.g., a paragraph with a check mark next to a phrase) without writing markup.

## Pattern

Enable `ui_icons_ckeditor5` and `ui_icons_text`.

For each text format that should support icons:

1. **Configuration → Text formats and editors → {your format} → Configure**
2. **Toolbar**: drag the **Icon** button to the active toolbar
3. **Filters**: enable **"Embed icon"**
4. **Save**

The Icon button opens a modal picker. On save, an `<drupal-icon>` tag is inserted:

```html
<drupal-icon
  data-icon-id="my_theme_icons:check"
  data-icon-settings='{"size":18,"color":"#0a0"}'
  class="text-success"
  aria-label="Included"
  role="img"
></drupal-icon>
```

The `icon_embed` text filter transforms the tag at render time using the pack's template.

## Where the passthrough attributes actually land

`class`, `aria-label`, `aria-hidden` and `role` do **not** reach the element your pack template emits. `IconEmbed::getWrappedRenderable()` builds the icon renderable, then wraps it in a `<span>` and puts those attributes there, always appending its own `drupal-icon` class:

```html
<span class="text-success drupal-icon" aria-label="Included" role="img">
  <!-- the pack template's own markup, untouched -->
</span>
```

It also attaches the `ui_icons_text/icon.content` library. So style and target `.drupal-icon`, or the wrapper's own classes — a selector written against the `<svg>` will not see them.

Two attribute quirks worth knowing:

- **`aria-hidden` is a presence check, not a value check.** The filter does `if ($node->getAttribute('aria-hidden'))`, and the string `"false"` is truthy in PHP, so `aria-hidden="false"` becomes boolean `TRUE` and renders as a bare valueless `aria-hidden`. The only way to get a non-hidden icon is to omit the attribute entirely.
- **`role="presentation"` or `role="none"` drops `aria-label`.** That is deliberate — an element removed from the accessibility tree must not carry an accessible name.

Selecting an inserted icon in the editor opens a balloon toolbar with an **Edit** button, which reopens the dialog pre-filled from the element's icon id and settings — no need to delete and re-insert to change one.

## Pattern: Configuring the text format

`ui_icons_text` validates the format form and will **block the save** on three things:

1. **Allowed HTML.** With `filter_html` enabled, the allowed-tags string must contain `<drupal-icon data-icon-id data-icon-settings class aria-label aria-hidden role>`. All six attributes are required (or `*`); a missing one is named in the error.
2. **Filter order.** `Embed icon` must run **after** `filter_html` and `filter_autop` — that is, at a higher weight. Placing it earlier is a form error.
3. **`filter_html_escape`.** If "Display any HTML as plain text" is on, icons cannot work; the validator errors and tells you to remove one or the other.

## Decision

| Need | Approach |
|---|---|
| Inline icons in body text | `<drupal-icon>` filter (this guide) |
| Icons as a separate field | `ui_icon` field type — see [Field API Integration](field-api.md) |
| Both | Both — they're independent integrations |

## Common Mistakes

- **Wrong**: enabling the toolbar button without enabling the filter → **Right**: `<drupal-icon>` shows up as raw text in output without `icon_embed` enabled
- **Wrong**: putting `Embed icon` before `Limit allowed HTML tags` → **Right**: the icon filter consumes the tag `filter_html` has already vetted, so it must run after, at a higher weight
- **Wrong**: allowing `<drupal-icon data-icon-id data-icon-settings>` only → **Right**: the format form errors naming `class aria-label aria-hidden role` as missing; the filter needs all six attributes
- **Wrong**: writing `aria-hidden="false"` to mark an icon as meaningful → **Right**: the filter treats any non-empty value as true and emits a bare `aria-hidden`. Omit the attribute instead
- **Wrong**: styling the `<svg>` the pack template emits and wondering where `class` went → **Right**: it is on the `<span class="… drupal-icon">` wrapper the filter adds
- **Wrong**: listing only some packs implicitly → **Right**: restrict via the filter's `allowed_icon_pack` setting. `result_format` (`list` or `grid`) and `max_result` (default 24) are settings on the same filter

## See Also

- [Field API Integration](field-api.md)
- [UI Icons Overview](overview.md)
- Reference: `modules/ui_icons_text/src/Plugin/Filter/IconEmbed.php`
- Reference: `modules/ui_icons_ckeditor5/js/ckeditor5_plugins/icon/src/iconToolbar.js`
