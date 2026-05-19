---
description: Group semantically-related blocks into ONE Layout Builder section via multiple SectionComponent entries — preserves section-level styling (background, spacing, container width) as one editable unit instead of fragmenting across sibling sections.
tldr: When a page region aggregates 2+ blocks that share authoring intent AND section-level styling AND coordinated order, emit ONE LB section with N SectionComponents instead of N sibling sections. Sibling-section fragmentation breaks UI Styles section-level coordination. Counter-example — multi-item collections (4 pillar cards) are Pattern 2 wrapper bundles, NOT N SectionComponents.
---

# Multi-Block Sections

## When to Use

> Use this when planning Layout Builder defaults for a page bundle whose design has page regions that aggregate multiple blocks under one editable section-level styling (background, spacing, container width). The `SectionComponent` API supports multiple components per section; this page documents *when* to group vs split.

Drupal's [Layout Builder overview](lb-overview.md) and [Sections & Layouts](sections-layouts.md) document the section + component data model. The strategy — when ≥2 semantically-related blocks should share ONE section vs be placed in sibling sections — is implicit in the API. This page makes the rule explicit.

A common Layout Builder anti-pattern: a page region in the design that aggregates "section heading + section body + section CTA" as one editable unit gets emitted as THREE sibling LB sections. Each section then has its own background, spacing, and container width — fragmenting editor-controlled section styling and breaking section-level coordination.

## Core Rule

A page region that aggregates "section heading + section body + section CTA" as one editable unit MUST emit as ONE Layout Builder section containing THREE `SectionComponent` entries — NOT three sibling sections.

The block bundles remain separate Tier 1 entities (`section_heading`, `section_body`, `section_cta`); the LB section unifies them. UI Styles options (background, spacing) attach to the section once and apply to all components within.

## Detection Rule — Three Signals

Group blocks into ONE section when ALL THREE signals fire:

1. **Shared authoring intent** — the blocks introduce a topic and elaborate it together; editors think of them as one unit.
2. **Shared section-level styling** — one background, one vertical spacing, one container width applies to all of them.
3. **Coordinated render order** — the blocks render in a fixed sequence relative to each other.

If any signal is absent, use sibling sections — each block independently controllable.

## SectionComponent Shape

In `core.entity_view_display.{entity}.{bundle}.default.yml`:

```yaml
third_party_settings:
  layout_builder:
    enabled: true
    sections:
      - layout_id: layout_onecol
        layout_settings:
          ui_styles_section:
            section_background: surface_subtle
            section_spacing_vertical: comfortable
        components:
          # Three SectionComponents in one section
          'uuid_1':
            uuid: 'uuid_1'
            region: content
            configuration:
              id: 'inline_block:section_heading'
              label_display: '0'
            weight: 0
          'uuid_2':
            uuid: 'uuid_2'
            region: content
            configuration:
              id: 'inline_block:section_body'
              label_display: '0'
            weight: 1
          'uuid_3':
            uuid: 'uuid_3'
            region: content
            configuration:
              id: 'inline_block:section_cta'
              label_display: '0'
            weight: 2
```

`weight` controls render order. `region` is the layout's region (most layouts use `content`; multi-region layouts dispatch components per region).

See [Config Schema](lb-config-schema.md) for the full LB YAML structure.

## Layout Choice

Pick the layout per the section's grid pattern:

| Section shape | Layout |
|---------------|--------|
| Single column of stacked blocks | `layout_onecol` |
| Two-column (e.g., heading on left, body+CTA on right) | `layout_twocol_section` |
| Three-column feature grid | `layout_threecol_section` |
| Custom designer layout | A theme-provided layout plugin |

When multiple blocks fit one region, weight ordering controls render. When blocks dispatch across regions (heading in `top`, image in `left`, CTA in `right`), assign `region` per component.

## Inline Blocks vs Reusable Blocks

`SectionComponent` references a block via `configuration.id`. Two formats:

- **`inline_block:{bundle}`** — Inline Block: bundle ships with the recipe; instances are page-scoped. **Default choice** for sections that compose pages.
- **`block_content:{uuid}`** — Reusable Block: a saved `block_content` entity with a fixed UUID. Use only when the same content instance must appear on multiple pages (rare; usually an entity reference is a better fit).

See [Inline vs Reusable](inline-vs-reusable.md) for the full comparison.

## When NOT to Use Multi-Block Sections

| Situation | Use instead |
|-----------|-------------|
| Multi-item collection where items repeat with same shape (e.g., 4 pillar_card under one heading) | Pattern 2 wrapper bundle + multi-value field. The wrapper bundle owns the heading + the multi-value pillar list. ONE block in the LB section, not N. See [Storage Decision Tree Q4](../entities/storage-decision-tree.md). |
| Two visually-similar blocks with NO shared authoring intent | Two sibling LB sections. The detection rule explicitly requires shared intent. |
| Three wholly distinct page sections (hero, services overview, testimonial) | Three sibling LB sections. Each section gets its own SectionComponents per its own internal composition. |

## Worked Examples

### Example 1 — Hero with heading + body + CTA

A `hero` Tier 1 entity has three internal blocks: `section_heading`, `section_body`, `section_cta`. STYLEGUIDE shows shared section background + spacing.

Emit ONE LB section with THREE SectionComponents (one per block bundle).

**Subtlety**: if `heading`, `body`, `cta` are *fields of one `block_content.hero` bundle* (not independent block bundles), the LB section contains ONE SectionComponent for `inline_block:hero`. Multi-block-per-section applies when the blocks are independently editable bundles, NOT when they're fields of one bundle.

### Example 2 — Two-column "About" — heading left, body+CTA right

An `about_section` page region has three blocks across two regions:

```
layout_id: layout_twocol_section
components:
  heading_uuid:  { region: first,  weight: 0, ... inline_block:section_heading }
  body_uuid:     { region: second, weight: 0, ... inline_block:section_body }
  cta_uuid:      { region: second, weight: 1, ... inline_block:section_cta }
```

One LB section, three SectionComponents distributed across two regions.

### Example 3 — Pillar grid of 4 feature cards (counter-example)

A `pillar_section` contains 4 `pillar_card` entries. NOT a multi-block-section case — this is Pattern 2 (multi-item collection).

Commit ONE wrapper bundle `block_content.pillar_section` with `field_pillars` multi-value referencing `block_content.pillar_card`. The LB section contains ONE SectionComponent for `inline_block:pillar_section`. The wrapper's view display renders the multi-value field; cards are NOT individual SectionComponents.

### Example 4 — Three sibling sections on a landing page

A landing page has hero, services-overview, testimonials — three independent page sections. They don't share intent or styling.

Commit THREE LB sections (one per concern), each with one or more SectionComponents internal to that section per the section's own composition.

## Section-Level Styling (UI Styles)

Section background, vertical spacing, and container width attach to the SECTION via `layout_settings.ui_styles_section.*` — not to individual SectionComponents. This is precisely why multi-block sections matter: one section = one set of styling choices = one coordinated visual unit.

See:

- [UI Styles overview](../ui-styles/overview.md) — section-level option lists (`section_background`, `section_spacing_vertical`)
- [Layout Builder Styles](lb-styles-overview.md) — legacy mechanism for similar effect (UI Styles supersedes for new work)

## Forbidden Patterns

- **Sibling LB sections for coupled blocks** — emitting `section_heading` and `section_body` as two adjacent LB sections when they share intent + styling. The architectural fix is at LB-default emission time, not render-time hygiene.
- **One LB section per block universally** — adopting a "1 block = 1 section" convention. LB sections are styling/grouping containers; blocks are content.
- **N inline blocks for what should be Pattern 2** — see counter-example 3. Multi-item collections are wrapper-bundle + multi-value field, NOT N SectionComponents.
- **Hardcoding section bg/spacing on the SectionComponent** — section-level styling lives in `layout_settings.ui_styles_section`. SectionComponent-level `configuration` is for per-block options, not section-level layout.

## See Also

- [Sections & Layouts](sections-layouts.md) — section + component data model
- [Config Schema](lb-config-schema.md) — full LB YAML structure
- [Inline vs Reusable](inline-vs-reusable.md) — `inline_block:` vs `block_content:` choice
- [Block Placement](block-placement.md) — programmatic block placement in sections
- [Storage Decision Tree](../entities/storage-decision-tree.md) — Q4 (Pattern 2) for multi-item collections
- [UI Styles](../ui-styles/index.md) — section-level styling option lists
- [UI Styles vs UI Skins vs UI Icons](../ui-styles/decision-rule.md) — choose which mechanism for which concern
