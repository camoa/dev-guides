---
tldr: "Harden the form display (separate config from view display) before editor handoff: set media_library_widget, hide legacy fields via hidden:, add descriptions. Applies to both node bundles and block_content inline-block bundles."

---
## 15.1. Editor Form-Display Hardening for Handoff

### When to Use

Before handing a Layout Builder site to content editors, when you need the **Manage form display** (the editing side) to be as clean and safe as the render side the rest of this guide covers. Applies to node bundles AND to `block_content` bundles used as inline blocks.

### Pattern

The view/render display controls what visitors see; the **form display** controls what editors edit. Harden it separately:

1. **Use the Media Library widget for media fields** — set the widget to `media_library_widget` so editors get the Media Library picker instead of a raw autocomplete.
2. **Hide legacy/raw fields editors shouldn't touch** via the `hidden:` region — a legacy `field_image` superseded by a Media Library field, plus node base fields `created`, `uid`, `promote`, `sticky`, and `path`.
3. **Add non-empty `description:` on editorially-facing fields** so editors get inline guidance.

```yaml
# core.entity_form_display.node.<bundle>.default.yml
hidden:
  created: true
  field_image: true   # legacy field superseded by a Media Library field
  path: true
  promote: true
  sticky: true
  uid: true
```

The same hardening applies to `core.entity_form_display.block_content.<bundle>.default.yml` for inline-block bundles: pick the media_library_widget, hide superseded/raw fields, and describe the fields editors do use.

### Common Mistakes

- **Exposing a raw legacy image field alongside its Media Library replacement** → Editors see two ways to add an image, produce inconsistent data, and get confused about which is authoritative. Hide the legacy `field_image`
- **Hardening only the view display** → The form display is a separate config export. A clean render side can still ship a messy, unsafe editing form
- **Leaving base fields (`created`/`uid`/`promote`/`sticky`/`path`) editable** → Non-editorial fields clutter the form and let editors change authorship/publishing metadata unintentionally
- **Shipping fields with no description** → Editors guess at intent; add a non-empty `description:` on editorially-facing fields

### See Also

- Section 2: Enabling Layout Builder (`enabling-lb`) — editor permission set for handoff
- Section 15: Theming Layout Builder (`theming-lb`) — the render-side counterpart
- Reference: `/core/modules/media_library/src/Plugin/Field/FieldWidget/MediaLibraryWidget.php`
