---
description: schemadotorg alpha mappings omit their mapping_type config dependency — a flat recipe imports alphabetically and creates mappings before their types, failing install. Enrich the deps post-export.
drupal_version: "11.x"
tldr: "`schemadotorg` alpha `schemadotorg_mapping` entities don't declare their `schemadotorg_mapping_type` config dependency. A flat recipe imports config alphabetically, so `...mapping.media` lands before `...mapping_type.media` → \"A mapping type for 'media' does not exist\". Add the mapping_type to each mapping's `dependencies.config` after export. `site:export` regenerates WITHOUT it — re-apply the patch every export and document it."
---

# schemadotorg mapping_type Dependency Enrichment Post-Export

**What:** After `drush site:export`, add `schemadotorg.schemadotorg_mapping_type.<entity>` to each `schemadotorg.schemadotorg_mapping.<entity>` config file's `dependencies.config`. This is a post-export patch that must be re-applied every export and documented (e.g. in `AGENTS.md`).

**Rationale:** `schemadotorg` at alpha (observed `1.0.0-alpha37`) ships `schemadotorg_mapping` config entities that do **not** declare a dependency on their corresponding `schemadotorg_mapping_type`. A recipe with a **flat** config list imports config files in **alphabetical** order, so `schemadotorg.schemadotorg_mapping.media` is created before `schemadotorg.schemadotorg_mapping_type.media` exists, and install dies with `A mapping type for 'media' does not exist`. Declaring the dependency in the mapping forces the config system to import the type first, resolving the ordering race. This is an upstream gap (issue candidate) — the mapping should declare the dep itself — so the fix lives outside the module in the consuming template. Because `site:export` **regenerates the mapping config from the live DB without the dependency**, the enrichment is lost on every re-export; treat it as a standing post-export step, not a one-time edit.

**When it applies:** Any recipe/site template that ships `schemadotorg` mappings (alpha) with a flat config-import order and is produced via `site:export`. Watch for it on the first fresh consumer install — an in-place-upgraded source site won't reproduce it (mappings and types already coexist in the DB).

**Example:**

```yaml
# config/schemadotorg.schemadotorg_mapping.media.image.yml  (post-export patch)
dependencies:
  config:
    - schemadotorg.schemadotorg_mapping_type.media   # ← ADD: forces the type to import first
    - media.type.image
  module:
    - schemadotorg
# ...repeat for every schemadotorg_mapping.<entity>.<bundle> file (9 in the observed package)
```

```text
Without the dep (flat, alphabetical):        With the dep:
  schemadotorg_mapping.media   ← first  ✗     schemadotorg_mapping_type.media  ← pulled first  ✓
  schemadotorg_mapping_type.media ← too late   schemadotorg_mapping.media       ← resolves      ✓
  → "A mapping type for 'media' does not exist"
```
