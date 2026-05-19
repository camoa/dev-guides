---
description: Q1/Q2/Q3 dispatch rule for choosing between UI Styles, UI Skins, and UI Icons when assigning a layout concern to YAML config. Eliminates hardcoded background/spacing/icon-pack choices from Twig.
tldr: Three-question dispatch for layout concerns. Q1 single independent style choice (one dimension, mutually exclusive options) → UI Styles. Q2 coordinated bundle of styles applied as one semantic unit (e.g., dark mode flips bg + text + CTA together) → UI Skin. Q3 icon-pack choice → UI Icons. Default greenfield posture — adopt UI Styles + UI Icons; skip skins until coordinated variants recur.
---

# UI Styles / UI Skins / UI Icons — Decision Rule

## When to Use

> Use this when assigning a layout concern (section background, vertical spacing, container width, theme variant, icon-pack choice) to one of the three UI Patterns ecosystem mechanisms. Each module has its own scope; this page is the dispatch rule that picks which one fits which concern.

The UI Patterns ecosystem (UI Styles, UI Skins, UI Icons) is the canonical mechanism for keeping background, spacing, container width, theme variants, and icon-pack choices OUT of Twig templates. Hardcoding those concerns in Twig is the common anti-pattern — editors lose control, design tokens cannot evolve.

Each module is documented in isolation:

- [UI Styles](index.md) — curated CSS class options
- [UI Skins](../ui-skins/index.md) — CSS custom property values and named theme variants
- [UI Icons](../ui-icons/index.md) — icon pack registration

This page is the dispatch rule that picks which one fits which concern.

## The Q1/Q2/Q3 Dispatch

For each layout concern in your design:

```
Q1: Is the concern a single independent style choice (one dimension; choices
    are mutually exclusive within that dimension)?
      YES → UI Styles (one option list under {theme}.ui_styles.yml)
      NO  → Q2

Q2: Is the concern a coordinated bundle of styles applied together as one
    semantic unit (e.g., "dark mode" flips bg + text + CTA together)?
      YES → UI Skin (grouped variants under {theme}.ui_skins.themes.yml)
      NO  → Q3

Q3: Is the concern an icon-pack choice or icon variant?
      YES → UI Icons (pack registration under {theme}.icons.yml)
      NO  → Re-examine — the concern is probably not a UI Patterns ecosystem
            concern; may belong in SDC props, Field API, or theme settings
            directly
```

## Quick Reference

| Concern | Mechanism | YAML |
|---------|-----------|------|
| Section background colour (one dimension, mutually-exclusive options) | UI Styles | `{theme}.ui_styles.yml` |
| Section vertical spacing (one dimension) | UI Styles | `{theme}.ui_styles.yml` |
| Container width (one dimension) | UI Styles | `{theme}.ui_styles.yml` |
| Block alignment (one dimension) | UI Styles | `{theme}.ui_styles.yml` |
| Dark-mode hero (inverted bg + light text + adjusted CTA contrast, all coordinated) | UI Skin | `{theme}.ui_skins.themes.yml` |
| Brand-flavored variant (alternate logo + tinted bg + accent color, coordinated) | UI Skin | `{theme}.ui_skins.themes.yml` |
| Icon pack registration (Heroicons, Material, Feather, …) | UI Icons | `{theme}.icons.yml` |

## Q1 — UI Styles (Single-Dimension Option Lists)

Use UI Styles when one concern has multiple **mutually-exclusive options within one dimension**.

**Examples** — each is one option list:

| Concern | Option list machine name | Options |
|---------|---------------------------|---------|
| Section background | `section_background` | `surface_default`, `surface_subtle`, `surface_inverse`, `brand_primary` |
| Section vertical spacing | `section_spacing_vertical` | `compact`, `default`, `comfortable`, `roomy` |
| Container width | `section_container_width` | `narrow`, `default`, `wide`, `full` |
| Block alignment | `block_alignment` | `left`, `center`, `right` |

Each option in `{theme}.ui_styles.yml` carries `label` (human-readable) and a `class` (Tailwind utility or theme CSS class). See [Style Definition Format](definition-format.md) for the full schema.

## Q2 — UI Skin (Coordinated Variant Bundles)

Use a UI Skin when multiple style values must change **together** as one semantic unit — changing one without the others would be incoherent.

**Examples** — each is one skin:

| Skin | What it bundles |
|------|------------------|
| `hero_dark` | Inverted bg + light text + dark-mode CTA contrast — must change together |
| `hero_a11y_contrast` | Text-size bump + color-contrast adjustment + focus-ring intensity — accessibility coordination |
| `theme_holiday` | Holiday-tinted background + accent color + alternate brand mark — coordinated brand variant |

If the variants are **independently meaningful** (e.g., bg is a free choice AND spacing is a free choice), use TWO UI Styles option lists, NOT a skin. Skins are for coordinated bundles only.

### When NOT to Use a Skin

| Situation | Use instead |
|-----------|-------------|
| Background and spacing are independently chosen | Two UI Styles option lists, not a skin |
| One-off variant used on one bundle only | Bundle-specific UI Styles option, not a skin |
| Runtime theme toggle (user-facing dark mode switcher) | DaisyUI runtime theme controller or similar; UI Skins is config-time |

## Q3 — UI Icons (Pack Registration)

Use UI Icons when registering an icon pack the site uses across fields, body text, menu links, or components.

```yaml
# {theme}.icons.yml
icons:
  packs:
    heroicons-outline:
      label: 'Heroicons (outline)'
      provider: heroicons
      variant: outline
    heroicons-solid:
      label: 'Heroicons (solid)'
      provider: heroicons
      variant: solid
```

**Scope clarification**: UI Icons handles **pack registration**. Per-instance icon CHOICE (which icon from a registered pack a specific component instance uses) is handled by:

- UI Patterns icon fields (when used as SDC slot props)
- Drupal Field API Icon field (`type: ui_icon`)
- CKEditor 5 icon embed filter
- Menu link icon widget

See [UI Icons overview](../ui-icons/index.md) for the integration matrix.

## Greenfield Adoption Posture

Default adoption order for a new project:

1. **UI Styles + UI Icons** — adopt from day one; they cover 90% of layout-concern needs and have a low cognitive cost.
2. **UI Skins** — defer until coordinated variants recur. Skins are opt-in; most projects either don't need them or need only one.

This is a deliberate complexity-deferral. A site with two themes (light/dark) doesn't *need* UI Skins until a third variant or a coordinated brand bundle enters the picture — until then, light/dark can ride on existing UI Styles option lists or on the theme's own CSS-variable scope.

## Worked Examples

### Example 1 — Section bg + spacing on hero

The hero bundle has independently-chosen background (4 options) and vertical spacing (4 options). 16 visual combinations.

- Q1: bg is one dimension → UI Styles option list `section_background`
- Q1: spacing is one dimension → UI Styles option list `section_spacing_vertical`

Two option lists, both `applies_to: [section]`. NOT a skin (independently meaningful).

### Example 2 — Dark-mode hero variant

A specific hero variant flips background to inverse, text to light, and CTA contrast together. Editors should see ONE choice: "Use dark hero variant: yes/no".

- Q1: not a single style choice (3 things change together)
- Q2: coordinated bundle of styles → UI Skin `hero_dark`

The skin bundles the three CSS-variable changes. Editors flip one switch.

### Example 3 — Icon pack registration

The site uses Heroicons (outline + solid) and Material Symbols. Three packs.

- Q3: icon pack choice → UI Icons

Three entries under `{theme}.icons.yml > icons > packs`. Per-instance choice (which icon a specific CTA uses) is via UI Patterns icon prop or Drupal Icon field — registration is the UI Icons job.

### Example 4 — Editor wants to pick an icon pack for a CTA component

A CTA SDC has an icon slot. Editor wants to choose Heroicons outline vs Material.

- This is **per-instance icon choice**, not a layout concern across bundles.
- UI Icons registers the packs; the SDC icon slot prop (UI Patterns `ui:icon` PropType or Drupal Icon field) provides the per-instance picker.

Not a UI Styles or UI Skins concern.

## Forbidden Patterns

- **Hardcoded `class="bg-primary"` in Twig** — section background is UI Styles config; the Twig template uses `attributes.addClass()` and lets Layout Builder apply the chosen class.
- **Hardcoded vertical spacing in Twig** — same rule; use `section_spacing_vertical` UI Styles.
- **One UI Skin per visual variant when each variant is independently meaningful** — use UI Styles option lists. Skins are for coordinated bundles only.
- **Renaming design-token keys at the YAML layer** — `surface_default` from your styleguide stays `surface_default` in `ui_styles.yml`. Renaming breaks the contract; new keys require a styleguide edit, not a converter rewrite.
- **Inline icon SVG in SDC templates** — register the pack via `ui_icons.yml` and consume via the icon field/prop layer.

## See Also

- [UI Styles overview](index.md) — single-dimension option lists
- [UI Skins overview](../ui-skins/index.md) — coordinated variant bundles
- [UI Icons overview](../ui-icons/index.md) — icon pack registration
- [UI Patterns](../ui-patterns/index.md) — SDC components that consume Styles/Skins/Icons
- [Layout Builder Multi-Block Sections](../layout-builder/multi-block-sections.md) — how `applies_to: [section]` styles attach to LB sections
- [UI Skins + UI Styles Together](../ui-skins/ui-skins-with-ui-styles.md) — wiring CSS variables (skin) into utility classes (styles)
