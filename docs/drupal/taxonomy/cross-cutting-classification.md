---
description: When is a controlled set of values a taxonomy vocabulary vs a list_string field vs an entity reference to a content type? Decision rule for classification dimensions used across multiple bundles.
tldr: Use taxonomy when the values are USED AS A CLASSIFICATION DIMENSION across MULTIPLE bundles AND the set is finite. Bundle-private list (1 bundle, small set) → list_string. Unbounded or growing-over-time set with rich content → entity reference to a content type. Hierarchical classifications (Country > State > City) → taxonomy with parent terms. Share the entity_reference field storage across bundles, NOT one per bundle.
---

# Taxonomy as Cross-Cutting Classification

## When to Use

> Use this when planning a fixed set of values that classifies content — industries, regions, audiences, content types, statuses. Should the storage be a `list_string` field, a taxonomy vocabulary + entity_reference, or a node entity reference?

The [Taxonomy System Overview](taxonomy-overview.md) explains what taxonomy is. The [Vocabulary Config Schema](vocabulary-config-schema.md) covers YAML mechanics. This page documents the *decision rule* — when to reach for taxonomy vs the alternatives. It is the Q3 entry point of the [Storage Decision Tree](../entities/storage-decision-tree.md).

The wrong choices (list_string for shared classification, entity_reference for what should be a vocabulary) lead to data drift, hard-to-evolve term sets, and broken filtering across content types.

## What "Classification Dimension" Means

A **classification dimension** is a finite set of values that classifies content, orthogonal to the content's primary identity. Examples:

- Industry (Healthcare, Finance, Education, Manufacturing) — orthogonal to whether the content is a `service` or `case_study`
- Region (North America, EMEA, APAC) — orthogonal to content type
- Audience (Customers, Partners, Employees) — orthogonal to content type
- Status (Draft, Published, Archived) — but careful — this is moderation state, not content classification

A classification dimension is **shared across bundles** when ≥2 bundles use it as a filtering/categorization mechanism.

## The Q3 Dispatch Rule

For each classification-shaped field:

```
Categorical (finite set) AND used as classification dimension AND ≥2 bundles?
  YES → Taxonomy vocabulary + entity_reference (shared across bundles)
  NO  → Continue to alternatives below
```

If YES, commit one `taxonomy.vocabulary.{name}.yml` + one shared `field.storage.{entity_type}.field_{name}.yml` of type `entity_reference` with `target_type: taxonomy_term` and `handler_settings.target_bundles: [{name}]`. Instance the field on every classifying bundle.

## When NOT to Use Taxonomy

| Situation | Use instead | Why |
|-----------|-------------|-----|
| Bundle-private set of options (1 bundle, small finite list) | `list_string` field with `allowed_values` | Taxonomy is overhead for a single-bundle list of <5 fixed values |
| Set is unbounded or grows over time, with rich per-value content | Entity reference to a content type (e.g., `node.industry_page`) | Taxonomy terms are lightweight; if each "term" needs its own page, fields, layout, it's a content type |
| The values ARE the primary content (e.g., "products") | Their own content type, not a vocabulary | Vocabularies classify; content types ARE the things being classified |
| Moderation state, workflow status | Content Moderation / Workflows module | Workflows have their own state-management API |

## Hierarchy Considerations

Drupal taxonomies can be flat or hierarchical (terms with parent terms):

- **Flat vocabulary** — use when terms have no parent/child relationship (industries: Healthcare, Finance, Education)
- **Hierarchical vocabulary** — use when classification has nesting (Geography: Country > State > City; Topics: Section > Sub-section)

See [Hierarchical Taxonomy](hierarchical-taxonomy.md) for the mechanics. Default to flat unless the classification has natural depth — flat vocabularies are easier for editors and faster to query.

## Sharing the entity_reference Field Storage

When a classification recurs on ≥2 bundles, the `entity_reference` field storage MUST be shared, not duplicated per bundle.

**Correct:**

```yaml
# field.storage.node.field_industry.yml — one shared storage
field_name: field_industry
entity_type: node
type: entity_reference
settings:
  target_type: taxonomy_term

# field.field.node.service.field_industry.yml      — instance on service
# field.field.node.case_study.field_industry.yml   — instance on case_study
# (one storage, N instances)
```

**Incorrect** (fragmentation anti-pattern):

```yaml
# field.storage.node.field_service_industry.yml    — DON'T duplicate per bundle
# field.storage.node.field_case_industry.yml       — DON'T duplicate per bundle
```

This is the same generic-naming rule as [Shared Field Storage Strategy](../entities/shared-field-storage-strategy.md) — concern-shaped names, one storage per concern.

## Worked Examples

### Example 1 — Industry on service + case_study

Industry is a finite controlled set (Healthcare, Finance, Education, …) used to classify both `node.service` and `node.case_study`.

- Categorical: yes
- Used as classification dimension: yes
- ≥2 bundles: yes
- **Commit**: `taxonomy.vocabulary.industry.yml` + `field.storage.node.field_industry.yml` (`entity_reference` to `taxonomy_term`, `target_bundles: [industry]`) + field instances on `node.service` and `node.case_study`.

### Example 2 — Status on product only, 3 values

A `product` bundle has a `status` field with three values: In Stock, Backorder, Discontinued. Used only by `product`.

- Categorical: yes
- ≥2 bundles: NO
- **Commit**: `list_string` field with `allowed_values: {in_stock: 'In Stock', backorder: 'Backorder', discontinued: 'Discontinued'}` on `node.product`. No vocabulary.

### Example 3 — Author reference

An `article` bundle needs to reference its author. Authors are users.

- Categorical: NO (users grow over time; not a finite set)
- **Commit**: `entity_reference` field to `user`. Not a taxonomy.

### Example 4 — Industry page with rich content per industry

If each "industry" needs its own page, hero, body content, related case studies, the industry isn't just a classifier — it's a content type.

- **Commit**: `node.industry_page` content type. Other bundles that classify by industry then `entity_reference` `node.industry_page`, not a taxonomy term.

### Example 5 — Geography (Country > State > City)

A `location` field on multiple bundles needs three-level nesting.

- Categorical: yes
- Used as classification dimension: yes
- ≥2 bundles: yes
- Hierarchical: yes
- **Commit**: `taxonomy.vocabulary.geography.yml` with hierarchical terms (parent references). Shared `entity_reference` field storage.

## Forbidden Patterns

- **Per-bundle entity_reference field storage to the same vocabulary** — `field.storage.node.field_service_industry` AND `field.storage.node.field_case_industry` both referencing `taxonomy.vocabulary.industry`. Reconcile to one shared storage `field.storage.node.field_industry`.
- **list_string for shared classification** — using `list_string` with hardcoded `allowed_values` when the values are used across multiple bundles. The values fragment across YAML files; evolving the set requires editing every bundle.
- **entity_reference to content type for a thin classifier** — `entity_reference` to `node.industry` when each industry is just a name. Use taxonomy.
- **Taxonomy for moderation state** — content moderation has its own API (Workflows module). Don't model publish/draft as a vocabulary.

## See Also

- [Storage Decision Tree](../entities/storage-decision-tree.md) — Q3 entry point
- [Vocabulary Configuration Schema](vocabulary-config-schema.md) — vocabulary YAML schema
- [Creating Vocabularies via Config](creating-vocabularies-config.md) — vocabulary YAML authoring
- [Term Reference Field Configuration](term-reference-config.md) — entity_reference field YAML to taxonomy
- [Hierarchical Taxonomy](hierarchical-taxonomy.md) — parent term mechanics
- [Entity Reference Patterns](../entities/entity-reference-patterns.md) — handler settings for taxonomy references
- [Shared Field Storage Strategy](../entities/shared-field-storage-strategy.md) — generic naming for shared storages
