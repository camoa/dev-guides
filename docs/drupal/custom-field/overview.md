---
description: "When to use Custom Field 5.0.2 vs Paragraphs, entity references, or core multi-value fields for compound data storage in Drupal."
tldr: "Use Custom Field to store 3-10 related values in one table row instead of creating entity references or Paragraphs; a compound column can even hold an entity_reference sub-field, so \"needs a reference\" alone doesn't force a wrapper entity."
drupal_version: "11.x"
---

# Custom Field Overview

## Version

```
composer require 'drupal/custom_field:^5.0'
```

**5.0.2** (`core_version_requirement: ^11.4 || ^12`) is the version documented here. The 4.0.x branch is still maintained upstream, but 4.0.10 retargeted its compatibility to `^10.3 || >=11.0 <11.4` -- it will **not** install on Drupal 11.4 or later. On current core, 5.x is the only branch that installs. 5.0.0 is a modernization release (procedural `.module` hook shims and `DeprecationHelper` removed in favour of OO `#[Hook]` classes); the public API surface is unchanged from 4.0.x, so 4.x code and config carry over. The one upgrade action item is a post-update that backfills the taxonomy index -- see Schema Updates.

## When to Use

You need to store multiple related values together in a single field without creating entity references or separate content types -- for example, an address with street/city/state/zip, a product with SKU/price/weight/dimensions, or a person with first/last/email/phone.

## Decision

| If you need... | Use... | Why |
|---|---|---|
| 3-10 related simple values (text, numbers, dates) in one field | Custom Field | Single table storage, best performance, simpler queries, no entity overhead |
| Complex nested structures with their own fields and displays | Paragraphs | Full entity features, but significant performance cost from joins |
| Reusable components across content types with revisions | Paragraphs or Field Collection | Entity reference provides shared data, revision tracking |
| Simple multi-value field (one type repeated) | Core multi-value field | Simplest solution, no module needed |
| 50+ properties describing one thing | Custom field type plugin | Avoid field sprawl, keep related data together |

**Performance comparison**: Custom Field stores all sub-fields in one table row (one JOIN). Paragraphs creates separate entities (N+1 queries for N paragraphs). For 10 paragraph items, expect 20+ queries vs 1 query with Custom Field.

## Two Triggers for a `custom` Compound Field

A compound field (`type: custom`) is the right tool for two distinct reasons -- reach for it when EITHER applies:

1. **Grouping trigger** -- 3-10 related values that always belong together and render together (address parts; SKU/price/weight/dimensions). This is the performance play above: one table row instead of entity overhead.
2. **Polymorphic trigger** -- a value has **>=2 mutually-exclusive sub-shapes**, only one of which renders per instance, and no single core field type expresses all of them. Examples: a partner logo that is an image OR a text fallback; a contact method that is an email OR a phone OR a URL. Model each shape as its own column on one `custom` field and populate only the relevant one per instance.

**Overengineering guard (counter-example):** an *optional single* thing is NOT polymorphic. An optional link is just a single-value `link` field with `required: false` at the instance level -- there is no "cardinality 0..1" in Drupal (cardinality counts values; "optional" is the `required` setting). Do not reach for `custom` for the mere presence/absence of one shape.

**A `custom` compound field CAN hold an `entity_reference` column** -- the module ships an `entity_reference` sub-field type (`type: entity_reference` with a `target_type`). So "route to a wrapper entity because a column would be a reference" is wrong as a technical claim. The real rule is a judgment call: give a child its own wrapper entity when it needs its own view modes, cross-parent reuse, or an independent lifecycle -- NOT because a compound "can't hold a reference."

## Pattern

**Creating via UI (config-first approach)**:

1. Structure > Content types > [Type] > Manage fields > Add field
2. Select "Custom field" type
3. Define sub-fields (columns): name, type, length/size/precision
4. Configure widgets and formatters per sub-field
5. Save -- single table created with all columns

**Accessing in code**:

```php
// Load entity and access sub-fields
$node = \Drupal::entityTypeManager()->getStorage('node')->load($nid);
$street = $node->field_address->value; // Main property
$city = $node->field_address->city;    // Named sub-field
$state = $node->field_address->state;

// Multi-value access
foreach ($node->field_address as $delta => $item) {
  $line1 = $item->line1;
  $city = $item->city;
}
```

## Common Mistakes

- **Creating entity references when Custom Field would work** -- Use Custom Field for data that always belongs together (address parts), use entity references for independent reusable entities (taxonomy terms, referenced content). Entity references add query overhead
- **Not planning column schema before adding data** -- Column types (string length, decimal precision, datetime type) are locked after data exists. Plan schema carefully or use update service
- **Checking isEmpty() on individual sub-fields** -- Custom Field's isEmpty() checks all sub-fields together. Some fields marked `never_check_empty` (like UUIDs) don't affect empty state
- **Forgetting the double-underscore separator for extended properties** -- Image fields use `field__alt`, `field__title`, `field__width`, `field__height`. Link fields use `field__title`, `field__options`. Access via `$item->{'field__alt'}` syntax
- **Using Custom Field for complex editorial workflows** -- Paragraphs better for content that needs independent revisions, moderation, translations, or reuse across entities

## See Also

- Reference: [Custom Field project page](https://www.drupal.org/project/custom_field)
- Reference: [drupal.org handbook pages](https://www.drupal.org/docs/extending-drupal/contributed-modules/contributed-module-documentation/custom-field) -- still live, but no longer the canonical reference
- Reference: the module's own documentation site, shipped in the release tarball under `docs/` (mkdocs, Material theme; built from the project's GitLab repository). It documents every field type, widget and formatter plugin individually and is the canonical upstream reference as of 5.0.0
