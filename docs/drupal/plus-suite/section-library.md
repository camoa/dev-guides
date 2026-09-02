---
description: "Section Library — save and reuse Layout Builder sections, deep cloning, SectionLibraryTemplate entity, and LB+ toolbar integration"
tldr: "Use the Section Library to save and reuse Layout Builder sections, with all their blocks, as templates across pages."
drupal_version: "11.x"
---

# Section Library

## When to Use

> When you need to save and reuse Layout Builder sections (with all their blocks) as templates across pages.

## Architecture

Section Library provides:
- `SectionLibraryTemplate` — custom entity type for storing section templates
- Save sections from the current layout to the library
- Import saved sections into any layout
- Integration with LB+ via the `lb_plus_section_library` sub-module

## Section Library Tool

The `SectionLibrary` tool plugin (`lb_plus_section_library`) adds:
- **Left sidebar**: Lists all saved templates as draggable items with thumbnail images
- **Global top bar button**: "Save to Section Library" button (appears after the save button)
- **Tool indicator**: Section-level save link on hover

| Feature | Implementation |
|---|---|
| Hotkey | `s` |
| Weight | 160 |
| Sidebar content | Loads `SectionLibraryTemplate` entities |
| Save button | Opens AJAX dialog for template creation |
| Import | Drag template from sidebar, drops as new section |

## Deep Cloning

Section Library uses `DeepCloningTrait` to clone section data:
- Clones all section plugins
- Clones all block components within sections
- Generates new UUIDs for all cloned elements
- Clones inline block content entities (including nested layout blocks)

## Pattern: Template Entity

```php
// SectionLibraryTemplate entity
$template = SectionLibraryTemplate::create([
  'label' => 'Hero Section',
  'type' => 'section',
  'image' => $file_id,  // Optional thumbnail
]);
```

## Using Without LB+

Section Library works independently of Plus Suite — it can be used with standard Layout Builder. The `lb_plus_section_library` sub-module just adds the toolbar integration.

## Decision

| Scenario | Use Section Library? |
|---|---|
| Reusable hero sections across landing pages | Yes |
| Common footer/CTA patterns | Yes |
| One-off custom layouts | No |
| Design system components | Yes — save each as template |
| Content that varies per page | No — use blocks directly |

## Common Mistakes

- **Do not** save templates without a thumbnail image — the LB+ sidebar falls back to `section_library/images/default.png`, so every template without one looks identical and editors cannot tell them apart while dragging.
- **Do not** save every section to the library — only save sections that will actually be reused; clutter reduces discoverability.

## See Also

- [Nested Layouts](nested-layouts.md)
- [Place Block & Promoted Blocks](place-block-promoted-blocks.md)
- [Custom Design System Integration](custom-design-system.md)
- Reference: `section_library/src/Entity/SectionLibraryTemplate.php`
