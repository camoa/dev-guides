---
description: Core 11.4 moved core.entity_view_mode.node.search_index out of the node module — drupal_cms_search's cloneAs action crashes fresh installs; ship the view mode defensively (Haven pattern).
drupal_version: "11.x"
tldr: On core 11.4, drupal_cms_search 2.1.x clones node displays as `node.%.search_index` but the `search_index` view mode is no longer in the node module, so a fresh `site:install` crashes with `getConfigDependencyName() on null`. In-place-upgraded sites survive (mode already in DB), masking it. Ship `core.entity_view_mode.node.search_index.yml` in your own config/ (Haven does), or ship a FLAT recipe — a COMPOSED recipe can't fix it because sub-recipes run first.
---

# Ship core.entity_view_mode.node.search_index Defensively (Haven Pattern)

**What:** If your site template applies `drupal_cms_search` (or clones node view displays into a `search_index` view mode), ship `core.entity_view_mode.node.search_index.yml` in your own `config/` — or ship a flat recipe whose full active config already contains that view mode. Do not rely on the view mode existing.

**Rationale:** Core 11.4 moved `core.entity_view_mode.node.search_index` **out of the node module** (it now lives only in `core/modules/search/modules/search_node/config/optional/`). `drupal_cms_search` 2.1.x has a `recipe.yml` action that clones each node view display as `node.%.search_index` (`cloneAs`) and declares `config.import: node: [core.entity_view_mode.node.search_index]` to pull the mode in first — but on core 11.4 that import **silently no-ops** (the config is no longer in the node module), so the clone's display save crashes with `getConfigDependencyName() on null` at `EntityDisplayBase:302` (the null is the missing `$mode_entity`). This bites **every fresh install** applying `drupal_cms_search` on 11.4. Sites upgraded in place survive because the view mode is already in the DB from an 11.3-era install — which makes the failure look mysterious and intermittent. `Haven` ships `core.entity_view_mode.node.search_index.yml` in its own `config/` — official prior art for the fix.

**When it applies:** Any Drupal CMS site template or recipe on core 11.4+ that applies `drupal_cms_search`, or otherwise clones displays into a `search_index` view mode. Note the composition trap: a **composed** recipe that lists `drupal_cms_search` as a sub-recipe **cannot** fix this from its own `config/`, because sub-recipes run first — the crash happens before the parent's config imports. Options are to inline the search recipe's actions (so you control import order) or ship a flat recipe.

**Example:**

```yaml
# config/core.entity_view_mode.node.search_index.yml  (shipped in YOUR recipe, Haven pattern)
langcode: en
status: true
dependencies:
  module:
    - node
id: node.search_index
label: 'Search index'
targetEntityType: node
cache: true
```

```text
Composed recipe (BROKEN on 11.4):           Flat recipe (IMMUNE — the site:export output):
  recipes:                                    install: [ ...flat extension list... ]
    - drupal_cms_search   ← runs FIRST,       config/  ← full active config already
      crashes before parent config imports      contains search_index view mode + displays,
  config/core.entity_view_mode... ← too late    NO cloneAs action to crash
```
