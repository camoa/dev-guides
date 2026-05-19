---
description: Use custom_field for polymorphic data — values with ≥2 mutually-exclusive sub-shapes that no single core field type can express. The canonical trigger for custom_field over a core field type.
tldr: Detect polymorphism with three tests — ≥2 sub-shapes observed, mutually exclusive at render time, no single core field type fits. The canonical custom_field use case (logo as image OR text, contact as email OR phone OR URL, pricing as flat OR ranged OR quote). Avoid coercing into one shape or N parallel fields with form-level "fill one" guidance. Composite formatter + delegation preferred over custom plugin when sub-shapes match existing formatters.
---

# Polymorphic Compound Fields

## When to Use

> Use this when planning a field whose data has ≥2 mutually-exclusive sub-shapes — only one renders per instance, and no single core field type expresses both shapes acceptably. This is the canonical trigger for `custom_field`.

The [Column Types](column-types.md) reference catalogs the column types `custom_field` supports. This page documents the **use case**: when polymorphism is the right reason to reach for `custom_field` vs a core field type.

## The Polymorphism Test

A field is polymorphic when ALL of:

1. **≥2 sub-shapes observed** in the source data (e.g., a logo as image OR as text fallback).
2. **Mutually exclusive at render time** — only one sub-shape renders per instance.
3. **No single core field type fits** — coercing into one shape loses type information; using N parallel fields breaks mutual-exclusion enforcement.

If any of 1/2/3 fails, do NOT reach for `custom_field`. Use the matching core field type.

## Polymorphic vs Not Polymorphic

| Concern | Polymorphic? | Why |
|---------|--------------|-----|
| Partner logo — image_ref OR label_text | YES | Image when uploaded, text fallback when not. `entity_reference` to media doesn't carry text; `string` can't reference media. |
| Profile contact — email OR phone OR URL | YES | Three valid contact methods; one chosen per profile. |
| Pricing display — flat_price OR ranged_price OR contact_for_quote | YES | Three distinct shapes (decimal, two decimals, boolean + text). |
| Optional CTA (link OR empty) | NO | `link` field with cardinality 0..1 — empty is absence, not a different shape. |
| Heading on hero (always short string) | NO | One shape — short string. |
| Image with optional alt text | NO | `entity_reference` to media; alt is metadata on the media entity, not a sibling sub-shape on this field. |

## Column Shape Declaration

A `custom_field` storage declares named columns; each column has its own type. The instance-level widget chooses which subset of columns is editable per bundle.

### Worked Example — Partner Logo (image OR text fallback)

```yaml
# field.storage.block_content.field_partner_logo.yml
field_name: field_partner_logo
entity_type: block_content
type: custom_field
cardinality: -1  # multi-value if logo bar; 1 for single-logo bundles
settings:
  columns:
    image_ref:
      type: entity_reference
      target_type: media
      handler: 'default:media'
      handler_settings:
        target_bundles: [image]
    label_text:
      type: string
      max_length: 255
```

The matching `field.field.*.yml` declares the widget (form display) and formatter (view display). The formatter implements branching:

```
if (item.image_ref is not empty) {
  render via image_ref formatter (responsive_image, image_style, …)
}
elseif (item.label_text is not empty) {
  render label_text as styled text fallback
}
else {
  render nothing (empty state)
}
```

### Worked Example — Profile Contact (email OR phone OR URL)

```yaml
field_name: field_contact_method
entity_type: node
type: custom_field
cardinality: 1
settings:
  columns:
    contact_email:
      type: email
    contact_phone:
      type: telephone
    contact_url:
      type: link
```

Form widget surfaces all three; editor fills exactly one. Formatter branching:

```
if (item.contact_email is not empty) → render mailto:
elseif (item.contact_phone is not empty) → render tel:
elseif (item.contact_url is not empty) → render external link
```

## Formatter Branching — Three Encodings

| Encoding | When to use |
|----------|-------------|
| **Composite formatter + sub-formatter delegation** | Preferred. Sub-shapes match existing formatters (image, link, text). Compose by delegation; no custom PHP. |
| **Twig template branching** | Branching is presentation-only and can ride on the field's view display template. |
| **Custom formatter plugin (PHP)** | Branching needs server-side logic (hashing, permission checks, dynamic decisions). |

Default to composite delegation; reach for a custom plugin only when delegation cannot express the rule.

## Per-Bundle Widget Settings

Per-bundle widget config can:

- Hide columns the bundle doesn't use (e.g., a brand-only logo bundle hides `label_text`).
- Reorder column entry forms.
- Pre-fill defaults.

But the storage-level `columns:` definition is **shared across all instances** — adding columns post-deployment requires a storage update + migration. Plan column shapes deliberately at design time.

## Naming Convention

Storage name follows the concern, not the type:

- `field_partner_logo` — not `field_partner_logo_compound`
- `field_contact_method` — not `field_contact_method_polymorphic`

The field type (`custom_field`) lives in the storage YAML; the name describes the concern. Same generic-naming rule as [Shared Field Storage Strategy](../entities/shared-field-storage-strategy.md).

## Counter-Example — When NOT to Use custom_field

### Optional CTA on hero

A hero block has an optional CTA link. The CTA is either present (a link) or absent (nothing).

NOT polymorphic — emptiness is not a sub-shape. Use a `link` field with cardinality 0..1, not `custom_field`.

### Image with optional alt text

An image field optionally has alt text.

NOT polymorphic — alt is metadata on the media entity, not a sibling sub-shape on this field. Use `entity_reference` to `media`; the alt lives on the media entity's `field_media_image` alt attribute.

### Single-column custom_field

A field that uses `custom_field` with one column when a core field type fits.

NOT polymorphic — Q1 of the [Storage Decision Tree](../entities/storage-decision-tree.md) returns NO. Use the column type directly as a regular field.

## Forbidden Patterns

- **Coercing polymorphic data into one shape** — saving "logo image OR text" as a single `string` field that holds either the URL of the image or the text. Loses type information; breaks rendering.
- **N parallel fields with form-level "fill one" guidance** — `field_logo_image` AND `field_logo_text`, each with its own storage, expecting only one filled per instance. Form-level constraints don't enforce mutual exclusion; data integrity drifts.
- **Single-column custom_field** — Q1 in the Storage Decision Tree returns NO. Use the column type directly.
- **Adding columns ad-hoc post-deploy** — every column addition is a storage update with migration costs. Plan the column set up front.

## See Also

- [Storage Decision Tree](../entities/storage-decision-tree.md) — Q1 (polymorphism test) entry point
- [Column Types](column-types.md) — all 27 supported column types with schema details
- [Config-First Creation](config-first-creation.md) — how to author `custom_field` storages in YAML
- [Field-Level Formatters](field-level-formatters.md) — composite formatter delegation patterns
- [Shared Field Storage Strategy](../entities/shared-field-storage-strategy.md) — generic-naming rule for compound storages
