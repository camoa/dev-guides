---
description: Group Drupal config into recipes by installation cohesion — what installs together to make a working unit. Five-recipe layout (foundation + tier1_sections + tier1_pages + tier2_* + site) with topological install order.
tldr: Five-recipe layout for greenfield sites — foundation (shared storages, taxonomies, image styles, media bundles, UI Styles/Skins/Icons), tier1_sections (repeatable block_content), tier1_pages (node bundles + LB defaults), tier2_{entity} (one per standalone entity), site (top-level entry point declaring all dependencies). Topological install order foundation → tier2_* → tier1_sections → tier1_pages → site guarantees storages and reference targets exist before consumers.
---

# Recipe Boundaries Strategy

## When to Use

> Use this when planning a greenfield Drupal site or refactoring a "one big recipe" prototype into deployable units. Recipes (core 10.3+, stable in 11.0) are atomic deployable boundaries; install order is enforced topologically. This page documents the strategy of *what* to split, not the *mechanism* of recipe YAML (covered in [Recipe YAML Schema](recipe-yaml-schema.md)).

Drupal's [Recipe System Overview](recipe-system-overview.md) explains the mechanism. The strategy — which config belongs in which recipe — is folklore. The default "ship everything in one big recipe" works for proofs-of-concept but breaks down as the site grows: piecewise iteration becomes impossible, recipe inputs proliferate, and dependency ordering becomes implicit.

This page documents a five-recipe layout inspired by [Kanopi's `cms-planner`](https://www.drupal.org/project/cms_planner) and extended for tier-aware sites.

## The Five Recipe Boundaries

| Recipe | Owns | Why |
|--------|------|-----|
| `{theme}_foundation` | Shared field storages, taxonomy vocabularies, image styles + responsive image styles, media bundles, UI Styles `.ui_styles.yml`, UI Skins `.skins.yml`, UI Icons `.icons.yml` | These are dependency targets. Every other recipe references them. |
| `{theme}_tier1_sections` | Tier 1 `block_content` bundles + their field instances + view displays | Repeatable section building blocks (hero, pillar_section, feature_card, cta_banner). |
| `{theme}_tier1_pages` | Tier 1 `node` bundles + LB defaults + per-bundle inline-block restrictions + form displays | Page types that compose sections via Layout Builder. |
| `{theme}_tier2_{entity}` | One recipe per Tier 2 standalone entity (`{theme}_person`, `{theme}_service`, `{theme}_location`) | Independent reusable entities with their own lifecycle. Flat-name precedent — one recipe per entity type. |
| `{theme}_site` | Top-level recipe; declares `recipes:` dependencies on all the above; pinned install order | One-shot install entry point. |

## Topological Install Order

Drupal Recipes installs in declared dependency order:

```
foundation
   ↓ (depends on)
tier2_*  (each tier2_* depends on foundation)
   ↓
tier1_sections  (depends on foundation; may depend on tier2_* if a section references one)
   ↓
tier1_pages     (depends on tier1_sections)
   ↓
site            (depends on all of the above)
```

This order guarantees:

1. Field storages and taxonomies exist before any field instance references them.
2. Tier 2 reference-target bundles exist before Tier 1 sections that reference them via entity reference.
3. Tier 1 section bundles exist before Tier 1 page LB defaults reference them as inline blocks.

## Assignment Rules

For each config item, place it in the recipe that owns its lifecycle:

| Item | Owning recipe | Notes |
|------|---------------|-------|
| Shared field storage | `foundation` | Always, regardless of which bundles instance it |
| Bundle-private field storage | The bundle's recipe | Travels with its single instancing bundle |
| Taxonomy vocabulary | `foundation` | Always |
| `entity_reference` storage to taxonomy | `foundation` if shared across bundles; bundle's recipe if bundle-private |
| `image_style` / `responsive_image_style` | `foundation` | Image chain is shared infrastructure |
| `media.type.*` | `foundation` | Media bundles are shared infrastructure |
| `block_content.type.{tier1_section}` | `tier1_sections` | All Tier 1 sections together |
| `node.type.{tier1_page}` | `tier1_pages` | All Tier 1 pages together |
| `node.type.{tier2_entity}` | `tier2_{entity}` | One recipe per Tier 2 entity |
| `field.field.*` (instances) | The instancing bundle's recipe | Always travels with the bundle |
| `core.entity_view_display.*` | The bundle's recipe | View modes ship with the bundle |
| `core.entity_form_display.*` | The bundle's recipe | Form displays ship with the bundle |
| LB defaults (`third_party_settings.layout_builder.sections`) | The bundle's recipe (typically `tier1_pages`) | LB config is part of the view display |
| `{theme}.ui_styles.yml`, `.skins.yml`, `.icons.yml` | `foundation` | Layout config infrastructure |

## Spanning Concerns

When a config item is referenced across recipe boundaries, place it in the broadest recipe that all consumers depend on:

- A taxonomy vocabulary referenced by both Tier 1 and Tier 2 → `foundation`
- A media bundle referenced by storages across recipes → `foundation`
- A Tier 1 section bundle that references a Tier 2 entity → declare `tier1_sections` depends on `tier2_{entity}`

**Default rule**: when in doubt, place in `foundation`. Broadest dependency root; never wrong, sometimes over-broad.

## Recipe YAML Shape

Each recipe declares `recipes:` for upstream dependencies and `config:` for what it installs:

```yaml
# {theme}_tier1_sections/recipe.yml
name: '{theme} — Tier 1 sections'
description: 'Tier 1 block_content bundles for repeatable page sections.'

recipes:
  - {theme}_foundation
  # add tier2_* as needed if any tier1 section references them

install:
  - layout_builder
  - layout_discovery
  - block_content

config:
  import:
    - block_content.type.hero
    - block_content.type.pillar_section
    - field.field.block_content.hero.field_eyebrow
    - field.field.block_content.pillar_section.field_eyebrow
    # ... per the recipe's assigned config list
```

Full YAML schema: [Recipe YAML Schema](recipe-yaml-schema.md). Composition mechanics: [Recipe Composition](recipe-composition.md).

## Worked Examples

### Example 1 — Greenfield site, no Tier 2

Three Tier 1 sections, three Tier 1 page types, no standalone entities:

- `{theme}_foundation` — `field_eyebrow`, `field_heading`, `field_body`, `field_cta` storages; image styles; media bundle; UI Styles/Skins/Icons
- `{theme}_tier1_sections` — `block_content.hero`, `pillar_section`, `feature_card` + instances + view displays
- `{theme}_tier1_pages` — `node.landing_page`, `service_page`, `legal_page` + LB defaults
- `{theme}_site` — depends on all three

No `tier2_*` recipes needed. The `site` recipe is the install entry point.

### Example 2 — Site with Person + Service Tier 2 entities

- `{theme}_foundation` — as above + `field_industry` taxonomy reference + `taxonomy.vocabulary.industry`
- `{theme}_tier2_person` — `node.person` + `field.field.node.person.*`
- `{theme}_tier2_service` — `node.service` + instance of `field_industry`
- `{theme}_tier1_sections` — sections; if any section references `node.person` (e.g., `featured_person_card`), declare `recipes: [{theme}_foundation, {theme}_tier2_person]`
- `{theme}_tier1_pages` — pages
- `{theme}_site` — depends on all

### Example 3 — Cross-cutting taxonomy

A `field_industry` taxonomy is referenced by Tier 2 `node.service` AND Tier 1 `node.case_study`. Both recipes need it before they install.

Commit the storage + vocabulary to `foundation`; both `tier2_service` and `tier1_pages` recipes declare dependency on `foundation`. No special handling needed — the topological order resolves it.

## Forbidden Patterns

- **Per-bundle micro-recipes** — one recipe per `block_content` bundle. Recipes are deployable units, not bundle wrappers. Group by tier and by entity type.
- **Mixing tier 1 and tier 2 in one recipe** — a `tier1_pages` recipe that also installs `node.person`. Tier 2 entities have their own lifecycle and recipe.
- **Foundation circularity** — `foundation` declaring a dependency on `tier1_sections`. Foundation is the dependency root; nothing else depends downward into it.
- **Skipping `site`** — install scripts that loop over individual recipes. The `site` recipe IS the install order; let Drupal Recipes resolve topologically.

## See Also

- [Recipe System Overview](recipe-system-overview.md) — when to use recipes vs distributions vs config split
- [Recipe YAML Schema](recipe-yaml-schema.md) — full YAML schema
- [Recipe Composition](recipe-composition.md) — composing recipes via `recipes:` key
- [Best Practices & Patterns](best-practices-patterns.md) — additional recipe best practices
- [Shared Field Storage Strategy](../entities/shared-field-storage-strategy.md) — what lives in foundation
- [Storage Decision Tree](../entities/storage-decision-tree.md) — pattern names that recipe assignment honors
- [Kanopi cms-planner](https://www.drupal.org/project/cms_planner) — recipe-grouping precedent
