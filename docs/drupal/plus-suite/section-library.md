---
description: Section Library — save and reuse Layout Builder sections, deep cloning, SectionLibraryTemplate entity, and LB+ toolbar integration
drupal_version: "11.x"
---

# Section Library

## When to Use

> Use Section Library to save reusable section templates (with all their blocks) that content editors can drag into any page. Skip it for one-off layouts.

## Decision

| Scenario | Use Section Library? |
|----------|---------------------|
| Reusable hero sections across landing pages | Yes |
| Common footer/CTA patterns | Yes |
| One-off custom layouts | No |
| Design system components | Yes — save each as template |
| Content that varies per page | No — use blocks directly |

## Pattern

**LB+ Section Library tool** (hotkey `s`, weight 160):
- Left sidebar: Lists saved templates as draggable items with thumbnails
- Global top bar: "Save to Section Library" button
- Tool indicator: Section-level save link on hover

**Creating a template:**

```php
$template = SectionLibraryTemplate::create([
  'label' => 'Hero Section',
  'type' => 'section',
  'image' => $file_id,  // Optional thumbnail
]);
$template->save();
```

**Deep cloning** on import:
- Clones all section plugins and block components
- Generates new UUIDs for all cloned elements
- Clones inline block content entities including nested layout blocks

**Standalone use:** Section Library works without Plus Suite — use it with standard Layout Builder. The `lb_plus_section_library` sub-module adds only the toolbar integration.

## Common Mistakes

- **Wrong**: Saving sections without thumbnails → **Right**: Thumbnail images in the sidebar help editors identify templates quickly
- **Wrong**: Saving every section — **Right**: Only save sections that will actually be reused; clutter reduces discoverability

## See Also

- [Nested Layouts](nested-layouts.md)
- [Place Block & Promoted Blocks](place-block-promoted-blocks.md)
- [Custom Design System Integration](custom-design-system.md)
- Reference: `section_library/src/Entity/SectionLibraryTemplate.php`
