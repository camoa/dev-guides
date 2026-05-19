---
description: Ordered Q1–Q6 ruleset for choosing a Drupal field pattern (shared storage, taxonomy, custom_field, wrapper bundle, entity reference, bundle-private) deterministically.
tldr: Use this whenever you need to commit a field pattern for a new field on a Drupal bundle. Ask Q1–Q6 in order; first YES wins. The order matters — polymorphism (Q1) overrides sharing (Q2); classification (Q3) overrides sharing (Q2); ownership (Q4) overrides reuse (Q5). Default at Q6 is bundle-private. Once committed, look up the specific field type within the chosen pattern via field-type-selection.
---

# Storage Decision Tree

## When to Use

> Use this when planning fields on a Drupal bundle — greenfield content types, converter pipelines (React/Figma → Drupal), or refactoring an existing site that has fragmented per-bundle storages for the same concern.

Drupal documents individual patterns (shared field storage, taxonomy reference, entity reference, `custom_field`, multi-value reference) in isolation. The question "in what order do I ask which pattern fits this field?" has no canonical answer in core docs. Asking in random order produces fragmentation (per-bundle storages of the same concern) or under-modeling (polymorphic atoms coerced into a single shape).

This page is the ordered ruleset. Use it before reaching for [Field Type Selection](field-type-selection.md) — the tree commits the pattern; field-type-selection then narrows to a specific type within that pattern.

## The Q1–Q6 Ordered Ruleset

For each field on a bundle, ask in this order. Earlier questions take precedence — once a question returns YES, commit to its pattern and stop.

```
Q1: Is the value polymorphic — has ≥2 mutually-exclusive sub-shapes that no
    single core field type can express?
      YES → Pattern 7: custom_field compound
      NO  → Q2

Q2: Does the same conceptual field appear on ≥2 other bundles (cross-cutting
    concern)?
      YES → Pattern 1-shared: shared field storage + bundle instance
      NO  → Q3

Q3: Is the value a categorical/finite set used as a classification dimension
    across ≥2 bundles?
      YES → Pattern 8: taxonomy vocabulary + entity_reference field
      NO  → Q4

Q4: Is the field a single repeatable child of this bundle — a sub-list owned
    together as one authoring unit?
      YES → Pattern 2: wrapper bundle + multi-value entity_reference
      NO  → Q5

Q5: Does the field reference an entity managed independently (its own
    lifecycle, reused from multiple contexts)?
      YES → Pattern 5: entity_reference to that bundle
      NO  → Q6

Q6: (default) Pattern 1-private — bundle-private field storage.
```

## Pattern Reference Table

| Pattern | Q | When | Storage shape |
|---------|---|------|----------------|
| **P1-shared** | Q2 | Same concern on ≥2 bundles (e.g., `field_eyebrow` on hero + pillar_section + feature_card) | One `field.storage.{entity_type}.{field_name}.yml` + one `field.field.{entity_type}.{bundle}.{field_name}.yml` per instancing bundle |
| **P1-private** | Q6 | Bundle-private field, no reuse signal | One `field.storage.*.yml` + one `field.field.*.yml` (single bundle) |
| **P2** | Q4 | Multi-item child collection owned by parent (e.g., `pillar_card` inside `pillar_section`) | Wrapper bundle + multi-value `entity_reference` field referencing the child bundle |
| **P5** | Q5 | Reference to independent entity (e.g., a reusable `person` or `service` node) | `entity_reference` field with `target_type: node`/`media`/`block_content` and target bundle restriction |
| **P7** | Q1 | Polymorphic data (e.g., logo as image OR text fallback) | `custom_field` storage with named columns + formatter branching rule |
| **P8** | Q3 | Controlled vocabulary used for cross-bundle classification | Taxonomy vocabulary + `entity_reference` field with `target_type: taxonomy_term` |

## Precedence Notes

- **Q1 takes precedence over Q2.** A polymorphic field that recurs on multiple bundles still emits as `custom_field`; the sharing decision then applies to the storage (one `field.storage.*` of type `custom_field` shared across bundles).
- **Q3 takes precedence over Q2.** A classification term reference is always taxonomy + entity_reference, even if every bundle in the system references it.
- **Q4 takes precedence over Q5.** A multi-item child owned by the parent is Pattern 2 (wrapper + multi-value), not Pattern 5 (entity_reference to independent entity), even if the child bundle could in principle be reused — ownership trumps potential reuse.

## Worked Examples

### Example 1 — `eyebrow` text on hero + pillar_section + feature_card

- Q1: not polymorphic (always a short string) → NO
- Q2: appears on ≥2 bundles (3 here) → **YES → P1-shared**

Commit one `field.storage.block_content.field_eyebrow` of type `string`. Emit `field.field.block_content.{hero,pillar_section,feature_card}.field_eyebrow` instances.

NOT acceptable: `field_hero_eyebrow`, `field_pillar_eyebrow`, `field_card_eyebrow`. Bundle-prefixed names are the fragmentation anti-pattern — see [Shared Field Storage Strategy](shared-field-storage-strategy.md).

### Example 2 — `industry` classification on service + case_study

- Q1: not polymorphic
- Q2: yes (≥2 bundles) — would map to P1-shared on its own
- Q3: BUT the value is a controlled vocabulary used as a classification dimension — **YES → P8**

Q3 takes precedence over Q2 when the value is categorical. Commit `taxonomy.vocabulary.industry.yml` + one shared `entity_reference` field storage `field.storage.node.field_industry.yml` with `target_type: taxonomy_term` and `handler_settings.target_bundles: [industry]`. Instance on `node.service` and `node.case_study`.

### Example 3 — `pillar_card` items inside `pillar_section`

- Q1–Q3: NO (cards have consistent shape, not classification, not cross-bundle reuse)
- Q4: **YES → P2**

Commit two bundles: wrapper `block_content.pillar_section` + child `block_content.pillar_card`. Add `field_pillars` on the wrapper as multi-value `entity_reference` (`target_type: block_content`, `target_bundles: [pillar_card]`, cardinality unlimited).

NOT acceptable: emitting N independent inline-block placements of `pillar_card` in the LB region of `pillar_section`. That fragments the authoring experience and breaks ownership semantics.

### Example 4 — `partner_logo` (image OR text fallback)

- Q1: **YES → P7** — `image_ref` and `label_text` are mutually exclusive sub-shapes.

Commit `field.storage.block_content.field_partner_logo` of type `custom_field` with columns:

```yaml
settings:
  columns:
    image_ref:
      type: entity_reference
      target_type: media
    label_text:
      type: string
      max_length: 255
```

Formatter branching: `image_ref ? render_image : (label_text ? render_label : empty)`. Full pattern: [Polymorphic Compound Fields](../custom-field/polymorphic-compound.md).

### Example 5 — `featured_person` on case_study referencing `node.person`

- Q1: NO; Q2: NO (only on `case_study`); Q3: NO (person is not a vocabulary)
- Q4: NO (the person is not a child owned by case_study; the person has independent lifecycle on `/people`)
- Q5: **YES → P5**

Commit `field.storage.node.field_featured_person` as `entity_reference`, `target_type: node`, `target_bundles: [person]`.

### Example 6 — `legal_disclaimer` on `node.privacy_page` only

- Q1–Q5: all NO
- Q6: **default → P1-private**

Commit `field.storage.node.field_legal_disclaimer` of type `text_long` + a single instance on `node.privacy_page`. No sharing; no wrapper.

### Example 7 — `cta` on hero + cta_banner (link with optional icon)

- Q1: not polymorphic — link is always link; icon is metadata on the link
- Q2: appears on ≥2 bundles → **YES → P1-shared**

Commit `field.storage.block_content.field_cta` of type `link`. Instance on both bundles. If a downstream variant introduces a genuine mutual exclusion (e.g., text-only label vs link), re-evaluate Q1 at that point.

## Generic Naming Rule

Shared field storages (P1-shared, P8) MUST use generic names. The field name describes the **concern**, not the bundle:

| Concern | Generic name | Bad (fragmentation) |
|---------|--------------|---------------------|
| Eyebrow text on a section | `field_eyebrow` | `field_hero_eyebrow`, `field_pillar_eyebrow` |
| Section heading | `field_heading` | `field_hero_heading`, `field_cta_heading` |
| Section body / lede | `field_body` | `field_hero_body`, `field_about_body` |
| Section CTA | `field_cta` | `field_hero_cta`, `field_card_cta` |
| Industry classification | `field_industry` | `field_service_industry`, `field_case_industry` |

Bundle-prefixed names are reserved for genuinely bundle-private fields where Q6 applied. If two bundles use bundle-prefixed names for the same concept, reconcile them via Q2.

## Field-Type Selection Within a Pattern

Once the pattern is locked, the specific Drupal field type follows from the data shape. See [Field Type Selection](field-type-selection.md). Common mappings:

| Data shape | Type |
|------------|------|
| Short string ≤255 chars | `string` |
| Long text with format | `text_long` (or `text_with_summary`) |
| Plain long text | `string_long` |
| URL with optional link text | `link` |
| Boolean toggle | `boolean` |
| Media reference | `entity_reference` `target_type: media` |
| Taxonomy reference (P8) | `entity_reference` `target_type: taxonomy_term` |
| Polymorphic compound (P7) | `custom_field` |

## Forbidden Patterns

- **Bundle-per-leaf-SDC** — emitting `block_content.button` because the analyzer found a `button` SDC. Buttons are sub-properties of their containing section; they MUST NOT have their own bundle.
- **Sibling fragmented storages** — `field_hero_cta` AND `field_card_cta` on the same site when the concern is the same. Reconcile to one shared `field_cta` via Q2.
- **N inline blocks for a multi-item collection** — placing 6 independent `pillar_card` inline blocks in a region instead of a `pillar_section` wrapper with `field_pillars`. Q4 forces P2. See [Layout Builder Multi-Block Sections](../layout-builder/multi-block-sections.md).
- **Single-column custom_field** — using `custom_field` with one column when a core field type fits. Q1 is for genuine polymorphism only.
- **Bundle-prefixed shared storages** — see Generic Naming Rule above.

## See Also

- [Field Type Selection](field-type-selection.md) — type choice within the chosen pattern
- [Field Storage Configuration](field-storage-configuration.md) — storage YAML schema
- [Entity Reference Patterns](entity-reference-patterns.md) — handler settings for P5 and P8
- [Shared Field Storage Strategy](shared-field-storage-strategy.md) — how to share storages across bundles when Q2 returns YES
- [Polymorphic Compound Fields](../custom-field/polymorphic-compound.md) — `custom_field` column shapes and formatter branching (P7)
- [Layout Builder Multi-Block Sections](../layout-builder/multi-block-sections.md) — P2 wrapper pattern vs LB section grouping
- [Recipe Boundaries Strategy](../recipes/recipe-boundaries-strategy.md) — which recipe owns which storage
- [Taxonomy as Cross-Cutting Classification](../taxonomy/cross-cutting-classification.md) — Q3 details
- [Creating Vocabularies via Config](../taxonomy/creating-vocabularies-config.md) — vocabulary YAML
- [Custom Field Column Types](../custom-field/column-types.md) — `custom_field` column definitions
