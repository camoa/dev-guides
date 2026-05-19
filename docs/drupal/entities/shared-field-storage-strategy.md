---
description: When N bundles share a concern, emit ONE field storage + N instances with generic concern-shaped names. Strategy companion to field-storage-configuration (which covers the mechanism).
tldr: Drupal field storages are per entity-type, not per bundle. When the same concern recurs on ≥2 bundles, emit one storage and N instances — never N storages. Use concern-shaped names (`field_eyebrow`, not `field_hero_eyebrow`). Reconcile cardinality to the maximum; type-promote on the broader type. Field storages live in the foundation recipe; bundles + instances live in their respective bundle recipes.
---

# Shared Field Storage Strategy

## When to Use

> Use this when planning fields that recur across multiple bundles — the same conceptual field (heading, eyebrow, body, CTA, image) appears on hero AND pillar_section AND feature_card. The mechanism (storage vs instance) is documented elsewhere; this page documents the strategy of *when* to share and *how* to name.

Drupal's [Field Storage Configuration](field-storage-configuration.md) explains the two-layer model: storages are per-entity-type technical definitions, instances per-bundle apply them. The strategy of when to share is folklore. The result on many sites: `field_hero_eyebrow`, `field_pillar_eyebrow`, `field_card_eyebrow` — three storages for the same concern, fragmenting the data architecture.

Kanopi's open-source [`cms-planner`](https://www.drupal.org/project/cms_planner) encodes the shared-field-storage discipline as a planning starter: generic field names, one storage per concern, instances per bundle. This page documents the discipline as a Drupal best practice.

## Core Rule

Drupal field storages are **per entity-type, not per bundle**. If a concern surfaces on N bundles of the same entity type, emit:

- ONE `field.storage.{entity_type}.{field_name}.yml`
- N `field.field.{entity_type}.{bundle}.{field_name}.yml`

Never emit N independent storages for the same concern. The `field_eyebrow` text on hero / pillar_section / feature_card MUST be a single `field.storage.block_content.field_eyebrow` with three field-instance YAML files referencing it.

## Detection Patterns

A concern qualifies as "shared" when ALL of:

1. **Same semantic role** across bundles (heading vs CTA vs eyebrow are distinct roles, even if all are short text).
2. **Same field-shape requirements** (cardinality, allowed formats, type).
3. **Recurs on ≥2 bundles** within the same entity type.

If 1+2+3 all hold, reconcile to one storage. If 1+2 hold but bundle count is 1, the concern is reuse-ready but emits as bundle-private until a second bundle adopts it.

## Generic Naming Convention

Storage names describe the **concern**, not the bundle:

| Concern | Generic name | Anti-pattern (do not emit) |
|---------|--------------|------------------------------|
| Section eyebrow text | `field_eyebrow` | `field_hero_eyebrow`, `field_pillar_eyebrow` |
| Section heading | `field_heading` | `field_hero_heading`, `field_cta_heading` |
| Section body / lede | `field_body` | `field_hero_body`, `field_about_body` |
| Section CTA | `field_cta` | `field_hero_cta`, `field_card_cta` |
| Featured image (reference to media) | `field_image` | `field_hero_image`, `field_card_image` |
| Industry classification | `field_industry` | `field_service_industry`, `field_case_industry` |

Bundle-prefixed names are reserved for fields that genuinely apply to one bundle only.

## Reconciliation Algorithm

For each concern shared across bundles:

1. Collect all per-bundle drafts that surface the concern.
2. If all drafts use the same generic name → emit one shared storage.
3. If drafts use bundle-prefixed names → **rewrite to the generic name**; record the rename.
4. If drafts disagree on **field type** (e.g., `string` on hero, `text_long` on pillar_section):
   - If one is a strict subtype of the other (`string` ⊂ `text_long` for plain text), promote to the broader type.
   - If incompatible (`link` vs `string`), the concerns are distinct — keep them separate with distinct generic names.
5. If drafts disagree on **cardinality**: take the maximum cardinality observed.

## Cardinality Rule

A field storage's cardinality is the **maximum** any instancing bundle requires. Reducing cardinality at the instance level is not supported by core; over-provisioned storage is normal.

**Example:** `field_cta` on `hero` (max 1) + `cta_banner` (max 2) + `feature_card` (max 1) → emit storage with `cardinality: 2`. Hero and feature_card instance forms display a single entry; widget config — not storage — enforces the per-bundle limit.

## Cross-Entity-Type Concerns

Field storages are scoped to one entity type. A concern that crosses entity types (e.g., `field_image` on `block_content.hero` AND `node.case_study`) is **two storages** by Drupal rule:

```
field.storage.block_content.field_image  → instance on block_content.hero
field.storage.node.field_image           → instance on node.case_study
```

Both reference `media` and may use identical handler settings. The duplication is intrinsic to Drupal's data model — it is **not fragmentation**. Same name across entity types is fine and expected.

## Dependency Ordering

Field storages MUST install before any bundle that instances them. The recommended layout:

- **Storages live in a `{theme}_foundation` recipe** (or any recipe declared as a dependency root)
- **Bundles + their `field.field.*` instances live in their respective bundle recipes** (e.g., `{theme}_tier1_sections`, `{theme}_tier1_pages`, `{theme}_tier2_{entity}`)
- Bundle recipes declare `recipes: [{theme}_foundation]`

Drupal's recipe topological install order then guarantees storages exist before any field instance references them. See [Recipe Boundaries Strategy](../recipes/recipe-boundaries-strategy.md).

## Worked Examples

### Example 1 — Three bundles, one shared eyebrow

Three drafts show `eyebrow` recurring on `block_content.hero`, `block_content.pillar_section`, `block_content.feature_card`. All three name `field_eyebrow`, type `string`, cardinality 1.

Commit:

```yaml
# field.storage.block_content.field_eyebrow.yml
field_name: field_eyebrow
entity_type: block_content
type: string
cardinality: 1

# field.field.block_content.hero.field_eyebrow.yml
# field.field.block_content.pillar_section.field_eyebrow.yml
# field.field.block_content.feature_card.field_eyebrow.yml
# (one instance per bundle, all referencing the shared storage)
```

### Example 2 — Naming conflict requires rewrite

Drafts disagree on name for the same concern:

- `hero` → `field_hero_eyebrow`
- `pillar_section` → `field_pillar_eyebrow`
- `feature_card` → `field_card_eyebrow`

Rewrite all three to `field_eyebrow`. Emit one storage and three instances.

### Example 3 — Type promotion

Drafts:

- `hero.field_body` → `string_long` (analyzer saw plain text in source)
- `pillar_section.field_body` → `text_long` (analyzer saw rich-text formatting)

Promote to `text_long` (broader). Hero's instance can still restrict allowed text formats at the form-widget level.

### Example 4 — Type incompatibility = distinct concerns

Drafts:

- `hero.field_action` → `link` (anchor with href)
- `feature_card.field_action` → `string` (plain text label)

Cannot reconcile — these are distinct concerns. Emit `field.storage.block_content.field_cta` (link) on hero AND `field.storage.block_content.field_label` (string) on feature_card. Different concerns, different names.

### Example 5 — Cross-entity-type concern

`field_image` appears on `block_content.hero` AND `node.case_study`. Field storages are per entity type; this is two storages by design:

```
field.storage.block_content.field_image  (instance on block_content.hero)
field.storage.node.field_image           (instance on node.case_study)
```

Not fragmentation — intrinsic to Drupal's data model.

## Forbidden Patterns

- **Bundle-prefixed shared storages** — `field_hero_cta` + `field_card_cta` for the same concern on different bundles. Always rewrite to `field_cta`.
- **Multiple storages for the same concern within one entity type** — even if names differ. Two `string`-type fields conceptually for "eyebrow" must collapse to one.
- **Per-bundle cardinality storages** — splitting a storage into `field_cta_single` and `field_cta_multi` to enforce per-bundle limits. Use widget config; one storage with the higher cardinality.
- **Narrow-typed storages that block reuse** — `string` (max 64) when one instancer needs longer text. Promote at storage; constrain at widget.

## See Also

- [Storage Decision Tree](storage-decision-tree.md) — Q1–Q6 ordered ruleset; Q2 entry point for sharing
- [Field Storage Configuration](field-storage-configuration.md) — storage YAML schema and required keys
- [Field Instance Configuration](field-instance-configuration.md) — per-bundle instance settings (label, widget, formatter)
- [Field Type Selection](field-type-selection.md) — type choice rationale
- [Recipe Boundaries Strategy](../recipes/recipe-boundaries-strategy.md) — foundation recipe ownership of shared storages
- [Kanopi cms-planner](https://www.drupal.org/project/cms_planner) — open-source planning tool that encodes this discipline
