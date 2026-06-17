---
# Routing block — an orchestrator reads to here and decides.
name: drupal_seo_foundation
capability: drupal-seo-foundation
description: Use when a Drupal 11.3+ site needs a complete on-page SEO foundation (metatag defaults, Schema.org JSON-LD, XML sitemap, pathauto patterns, redirects, robots.txt, google_tag, 403/404 + non-content defaults), composed from the site's own field inventory and runnable fully unattended via a typed input contract. Leverages drupal_cms_seo_basic + drupal_cms_seo_tools as the baseline; overlays only the gaps.

# Metadata — read only after a match.
label: Drupal SEO foundation
recipe_schema_version: 1.0.0
version: 0.1.0

# Machine-readable dependency declaration.
requires_guides:
  - drupal/seo-geo/overview
  - drupal/seo-geo/seo-recipe-baseline
  - drupal/seo-geo/metatag-architecture
  - drupal/seo-geo/core-meta-tags
  - drupal/seo-geo/open-graph
  - drupal/seo-geo/twitter-cards
  - drupal/seo-geo/canonical-urls
  - drupal/seo-geo/metatag-multilingual
  - drupal/seo-geo/structured-data-decision
  - drupal/seo-geo/schema-metatag-setup
  - drupal/seo-geo/schema-types-reference
  - drupal/seo-geo/pathauto-patterns
  - drupal/seo-geo/redirect-management
  - drupal/seo-geo/xml-sitemap
  - drupal/seo-geo/robots-txt
  - drupal/seo-geo/breadcrumbs-structured-data
  - drupal/seo-geo/testing-validation

requires_plays:
  - drupal/best-practices/camoa/metatag-per-bundle

drupal_compatibility: "^11.3"

requires_modules:
  - metatag
  - metatag_open_graph
  - metatag_twitter_cards
  - schema_metatag
  - schema_article
  - schema_organization
  - schema_product
  - schema_service
  - schema_web_page
  - pathauto
  - redirect
  - redirect_404
  - easy_breadcrumb
  - simple_sitemap
  - robotstxt
  - google_tag
  - token
  - token_or

invokes_drupal_recipes:
  - drupal_cms_seo_basic       # optional, configurable via input
  - drupal_cms_seo_tools       # optional, configurable via input

authors:
  - name: Palcera

license: GPL-2.0-or-later
---

## Goal

Deliver a complete on-page SEO foundation for a Drupal site — per-bundle metatag defaults (title, description, og:*, twitter:*, canonical), per-bundle Schema.org JSON-LD, an XML sitemap tuned per content priority, pathauto URL patterns for nodes and taxonomy terms, redirect-on-alias-change behavior, google_tag installed with its config excluded from sync, robots.txt managed as config, and 403/404/`user`/`taxonomy_term` defaults — **composed from the target site's own field inventory**, deterministically and idempotently, with the operator's policy supplied once via a typed input contract.

The recipe runs **fully unattended**. Decisions are encoded in the input contract; when the contract doesn't cover a situation, the recipe halts with a typed reason rather than guessing.

## Opinion

**Adapt to the target's actual fields, never bolt on.** Token chains are composed by walking a priority list against the audited per-bundle field set; first present field wins; if none, the recipe omits the override and lets the parent default fall through. The recipe does not assume a reference site's fields exist; it does not reference fields that the bundle doesn't carry. This stance is invariant — it is expressed by the Input-contract `priority_chains` walk and the State-awareness contract, not by a defaulting fallback.

**Per-bundle defaults, not one-size-fits-all.** Each bundle gets its own `metatag.metatag_defaults.<entity>__<bundle>.yml` declaring the chains relevant to its field set plus the Schema.org type that fits its semantic role. Source: play `drupal/best-practices/camoa/metatag-per-bundle`.

**Schema.org type per semantic role, not auto-derived.** `Article` for content pieces, `Product` for products, `Service` for solutions, `WebPage` for pages and landings, `LocalBusiness`/`Organization` on home. The mapping is declared by the operator in the input contract; the recipe does not infer it. Source: guide `drupal/seo-geo/schema-types-reference`.

**No hardcoded JSON-LD without explicit policy.** Tags like `schema_article_publisher`, `schema_article_author`, `schema_product_brand` carry hardcoded JSON blobs. The recipe never authors them unless the input contract names each blob and supplies (or accepts) its content. Source: guide `drupal/seo-geo/schema-metatag-setup`.

**Sitemap priority and changefreq per editorial role.** Uniform `0.9 / daily` across every bundle is a smell — it signals poor quality to search engines. Priority and changefreq are derived from the semantic role declared in the input. Source: guide `drupal/seo-geo/xml-sitemap`.

**Pathauto: one pattern per bundle, taxonomy terms are first-class.** Every content type reachable on the public site gets a deterministic pattern. `taxonomy_term` is enabled in `pathauto.settings.yml` and individual vocabularies get their own patterns when the input contract names them. Source: guide `drupal/seo-geo/pathauto-patterns`.

**robots.txt is content, not scaffold.** Use the `robotstxt` module so robots.txt is editable via config without redeploying core scaffold. The static `robots.txt` shipped by Drupal core scaffold is removed via the composer `drupal-scaffold.file-mapping` exclusion. Source: guide `drupal/seo-geo/robots-txt`.

**google_tag is installed, never config-managed.** A GA4 / GTM container is environment-specific, so its config must not live in tracked config sync. When `google_tag` is in scope the recipe installs the module and adds `google_tag` to `$settings['config_exclude_modules']` in `settings.php`; it authors **no** container config. The container is set per environment by the operator, outside config management — the recipe never fabricates or exports a GA4 / GTM ID.

**The recipe never makes a judgment call.** Every situation is either covered by the input contract (proceed) or it isn't (halt with a typed reason). It doesn't infer defaults; it doesn't have a "smart" fallback. This stance is invariant — it is expressed by the escalation policy in the Input contract and the adversarial Verifier, not by a play.

## The chain

The layers are configured in this order, and the order is load-bearing:

1. **Modules present and enabled.** `composer require` + `drush en` for any missing module the input names.
2. **Global metatag defaults.** Sitewide patterns that everything inherits. Source: guide `drupal/seo-geo/metatag-architecture` (cascading inheritance).
3. **Per-entity defaults.** `node`, `taxonomy_term`, `user` — the entity-level defaults. Source: guide `drupal/seo-geo/core-meta-tags`.
4. **Per-bundle defaults.** `node__<bundle>` files declaring the chains and Schema.org tags specific to each bundle's field set + semantic role.
5. **Page-context defaults.** `403`, `404`, `front` (if not present).
6. **Schema.org / JSON-LD per bundle.** Schema_metatag tags inside the per-bundle defaults from step 4. Source: guide `drupal/seo-geo/schema-metatag-setup`.
7. **Pathauto patterns.** Per-bundle node patterns + per-vocabulary taxonomy patterns. Source: guide `drupal/seo-geo/pathauto-patterns`.
8. **Sitemap settings.** Per-bundle priority + changefreq + image inclusion. Source: guide `drupal/seo-geo/xml-sitemap`.
9. **robots.txt content.** `robotstxt.settings.yml` + remove the static `robots.txt` via composer scaffold exclusion. Source: guide `drupal/seo-geo/robots-txt`.
10. **google_tag install + config exclusion.** Install the module and add `google_tag` to `$settings['config_exclude_modules']` in `settings.php` so its environment-specific container config stays out of config sync. The recipe authors no `google_tag` config; the container is configured per environment by the operator.
11. **Breadcrumb structured data.** Verify `easy_breadcrumb` has `add_structured_data_json_ld: true`. Source: guide `drupal/seo-geo/breadcrumbs-structured-data`.

The bundle defaults cannot exist until the per-entity defaults exist; pathauto patterns cannot generate aliases until the patterns are imported; the sitemap cannot reference URLs until aliases exist — hence the order.

## Preconditions

- Drupal 11.3+ (required by `drupal_cms_seo_basic` and `drupal_cms_seo_tools`, which this recipe leverages).
- Composer-managed install (the recipe writes to `composer.json` and runs `composer require`).
- A writable config sync directory the recipe can author into, and a writable `settings.php` (the recipe appends `google_tag` to `$settings['config_exclude_modules']` when `google_tag` is in scope).
- A working `drush` from the project root (or via ddev/docker wrapper).
- A typed input contract supplied by the caller (see below).

## Input contract

Generic schema, source-agnostic, supplied by the caller. **No field in this contract has a runtime default**; missing fields fail Phase 0 validation.

```yaml
mode: dry-run | apply
project_root: string                   # absolute path to the Drupal site
config_sync_dir: string                # relative to project_root

layers_in_scope:                       # opt-in per layer; absent = false
  metatag: true
  schema_org: true
  sitemap: true
  pathauto: true
  redirect: true                       # verify auto-redirect-on-alias-change behavior
  robotstxt: true
  google_tag: false                    # install module + exclude its config (settings.php)
  non_content_defaults: false          # 403/404/taxonomy_term/user metatag defaults

semantic_role_by_bundle:               # operator-chosen; no auto-derivation
  # role enum: content_article | product | service | web_page | landing_page | none
  <bundle>: <role>

priority_chains:                       # walked top-down against audited fields;
  og_image:                            #   first present field wins; if none, omit
    - <field_machine_name>
  meta_title:
    - <field_machine_name>
    - node:title                       # always-present terminator
  meta_description:
    - <field_machine_name>

reference_sources: [string]            # absolute paths to reference projects;
                                       # Phase 2 reads ONLY these
reference_selections: [string]         # explicit menu items pre-approved;
                                       # unselected items are dropped silently

home_node:                             # single source of truth; recipe does not infer
  nid: integer
  bundle: string
  og_image_strategy: omit | static_url
  og_image_static_url: string|null

sitemap_priority_by_role:              # role → (priority, changefreq)
  content_article: {priority: <0.0-1.0>, changefreq: <enum>}
  product:         {priority: <0.0-1.0>, changefreq: <enum>}
  service:         {priority: <0.0-1.0>, changefreq: <enum>}
  web_page:        {priority: <0.0-1.0>, changefreq: <enum>}
  landing_page:    {priority: <0.0-1.0>, changefreq: <enum>}

pathauto_patterns_by_bundle:           # bundles omitted get no pattern
  <bundle>: <pattern_string>

pathauto_patterns_by_vocabulary:       # vocabularies omitted get no pattern
  <vocabulary>: <pattern_string>

redirect:                              # verified when redirect in layers_in_scope
  auto_redirect: bool                  # expected true
  default_status_code: integer         # expected 301
  suppress_404: bool                   # redirect_404.suppress_404; expected true

robotstxt_content: string              # full robots.txt body
robotstxt_remove_static_scaffold: bool # remove web/robots.txt via composer scaffold

# google_tag has no contract fields — when in scope the recipe installs the module
# and excludes its config via settings.php (config_exclude_modules). The GA4 / GTM
# container is environment-specific and set by the operator per environment.

escalation_policy:                     # per ambiguity class; default = halt
  no_image_field_for_bundle: halt | omit_og_image | use_site_default
  no_description_field_for_bundle: halt | use_fallback | use_static
  url_convention_change_on_live_aliases: halt | apply_with_redirects | skip
  hardcoded_schema_org_blob: halt | apply | skip
  conflict_with_existing_config: halt | overwrite | skip
  new_entity_field_required: halt      # always halts; data-model changes out of scope
  content_seed_required: halt          # always halts; content authoring out of scope
```

## Sequence

If `mode: dry-run`, perform all reads and derivations but emit a preview instead of writing.

1. **Validate input contract.** Halt with `contract_error` on missing/inconsistent fields, on bundles that don't exist, on roles that aren't in the enum, on priority chains that name no terminator.

2. **Audit target project state.** Inventory composer.json modules, `core.extension.yml`, per-bundle field lists, existing sync configs matching the in-scope layers, taxonomies, home node. Read-only. Emit a structured `audit.json`. See guide `drupal/seo-geo/overview` for what's worth inventorying.

3. **Reference scan (advisory menu).** Read only `reference_sources`; produce a labelled menu of reference patterns. Filter to `reference_selections`; drop everything else. The recipe never carries unselected reference patterns into the plan. See guide `drupal/seo-geo/seo-recipe-baseline` for the Drupal CMS recipe shape if it's a selected source.

4. **Compose the plan.** For each in-scope layer, walk the contract's rules over the audit:
   - For each bundle in `semantic_role_by_bundle`: compose its per-bundle metatag default by walking `priority_chains` against the bundle's audited fields. Cite the rule and the field for every produced line.
   - For each role: derive Schema.org type and sitemap priority/changefreq from the input mapping.
   - For each bundle in `pathauto_patterns_by_bundle`: produce the pattern file.
   - For each vocabulary in `pathauto_patterns_by_vocabulary`: produce the pattern file.
   - For `google_tag` (if in scope): plan the module install and the `settings.php` `config_exclude_modules` entry. No container config is produced.
   - For robotstxt, redirect verification, 403/404, taxonomy_term, user, home: produce per the input.
   Emit a structured `plan.json`.

5. **Resolve escalations.** Walk every ambiguity and apply the escalation_policy. If any policy is `halt`, emit a structured `escalation.json` and exit non-zero. The operator updates the contract and re-runs.

6. **Apply.** Walk the plan:
   - `composer require <missing modules>` + `drush en <missing modules>` (includes `google_tag` when in scope).
   - For each emitted config file: absent → write; present + matching → no-op + log; present + differing → halt with `conflict` (already escalated in step 5; reaching this means a TOCTOU change).
   - For `google_tag` in scope: add `google_tag` to `$settings['config_exclude_modules']` in `settings.php`. The module is installed (above); no container config is written or exported.
   - `drush cim`.
   - `drush pathauto:aliases-generate create` per added pattern.
   - `drush simple-sitemap:generate`.
   - `drush cr`.
   - For `robotstxt_remove_static_scaffold: true`: update `composer.json` `extra.drupal-scaffold.file-mapping` to exclude `[web-root]/robots.txt`; delete the file.

7. **Verify.** Run the verifier (next section). Non-zero exit on any failure.

8. **Emit summary.** Change log: files written, modules installed, aliases regenerated, verifier results.

## Data flow

```
input: contract (operator-supplied, validated up front)

reads project state:
       composer.json + core.extension.yml
       field.field.<entity>.<bundle>.<field>.yml  (per bundle field inventory)
       taxonomy.vocabulary.*.yml
       existing metatag.metatag_defaults.* / simple_sitemap.* / pathauto.* /
         redirect.* / robotstxt.*
       settings.php (config_exclude_modules — for the google_tag exclusion)
       system.site.yml (home node)

applies opinion:
       play  drupal/best-practices/camoa/metatag-per-bundle  (per-bundle defaults)
       inline invariant stances: adapt-to-project-fields · schema-type-per-role ·
         no-hardcoded-json-ld-without-policy · sitemap-priority-per-role ·
         one-pathauto-pattern-per-bundle · robotstxt-as-content ·
         google-tag-install-only · halt-on-ambiguity ·
         headless-via-input-contract · verifier-runs-adversarially

references atomic detail (guides):
       drupal/seo-geo/{ overview, seo-recipe-baseline, metatag-architecture,
         core-meta-tags, open-graph, twitter-cards, canonical-urls,
         metatag-multilingual, structured-data-decision, schema-metatag-setup,
         schema-types-reference, pathauto-patterns, redirect-management,
         xml-sitemap, robots-txt, breadcrumbs-structured-data, testing-validation }

emits (in chain order):
       composer.json updates                          (modules + scaffold exclusion)
       metatag.metatag_defaults.global.yml            (update)
       metatag.metatag_defaults.node.yml              (update; chains pruned to audit)
       metatag.metatag_defaults.taxonomy_term.yml     (create, if non_content_defaults)
       metatag.metatag_defaults.user.yml              (create, if non_content_defaults)
       metatag.metatag_defaults.403.yml               (create, if non_content_defaults)
       metatag.metatag_defaults.404.yml               (create, if non_content_defaults)
       metatag.metatag_defaults.node__<bundle>.yml    (per bundle in semantic_role_by_bundle)
       pathauto.settings.yml                          (taxonomy_term enabled if needed)
       pathauto.pattern.<bundle>.yml                  (per bundle in input)
       pathauto.pattern.taxonomy_<vocabulary>.yml     (per vocab in input)
       simple_sitemap.bundle_settings.default.node.<bundle>.yml  (per role mapping)
       simple_sitemap.bundle_settings.default.taxonomy_term.<vocab>.yml  (per input)
       robotstxt.settings.yml                         (from input)
       settings.php  (config_exclude_modules += google_tag, if in scope)
       core.extension.yml                             (newly-enabled modules)
```

## State-awareness contract

For every emitted config object: absent → create; present and matching the derived spec → skip with `no-op`; present and differing → conflict, do not overwrite unless `escalation_policy.conflict_with_existing_config: overwrite`. A field listed in `priority_chains` that does not exist on **any** in-scope bundle → log warning, drop from chain. A bundle in `semantic_role_by_bundle` whose role implies fields it lacks (e.g. `content_article` without `field_seo_title`) → halt with `contract_error` so the operator either adjusts the role or the chain.

Idempotent: running the recipe twice on identical input and identical project state produces no changes on the second run, including no alias regeneration if no new pattern was added.

## Verifier

After `apply`, the recipe runs each check and emits PASS / FAIL. Failures exit non-zero with actual-vs-expected.

1. **metatag-resolves-per-bundle** — For each bundle with ≥1 published node: fetch a sample page; every metatag tag in the bundle's emitted default is present in `<head>` and its token chain resolved to non-empty content.

2. **json-ld-per-bundle-role** — For each bundle in `schema_org` scope: `<head>` contains at least one `<script type="application/ld+json">`; it parses; one of its `@graph` entries (or the root) carries `@type` matching the configured Schema.org type for the bundle's role.

3. **sitemap-covers-indexed-bundles** — `/sitemap.xml` returns 200; contains URLs from every indexed bundle; for each role mapping, at least one URL has the configured `priority` and `changefreq`.

4. **robotstxt-served-by-module** — `/robots.txt` content matches `robotstxt_content` from input; the static `web/robots.txt` is absent (composer scaffold exclusion applied).

5. **pathauto-pattern-produces-matching-alias** — For each pathauto pattern in input, the most recently created entity of that bundle/vocabulary has an alias matching the pattern.

6. **pathauto-context-fix-clean** — Run `drush pathauto:aliases-generate update canonical_entities:node`; assert no `ContextException` warnings in output. (This is the `context_mapping.node: node` fix that emerged from the cotea session.)

7. **redirect-on-alias-change** — When `pathauto` regenerates an alias for a node whose alias changed, `redirect` module creates a 301 from the old alias to the new. Verify: assert `redirect.settings.auto_redirect: true`, `default_status_code: 301`, `redirect_404.suppress_404: true`; fetch the old alias of a known-renamed node, assert `301` → new alias.

8. **google-tag-installed-and-config-excluded** — If `google_tag` is in scope: assert the `google_tag` module is enabled and that `google_tag` is listed in `$settings['config_exclude_modules']` (`settings.php`), so its environment-specific container config is not under config management. The recipe authors no container; per-environment container configuration is the operator's, out of scope.

9. **idempotency** — Immediately re-run `apply` with the same contract and project state; assert `drush cim` reports 0 changes and no aliases are regenerated.

The verifier is recipe-runnable, not operator-driven. Failures exit non-zero.

## References

### Guides

| Guide | Status | Used for |
|---|---|---|
| `drupal/seo-geo/overview` | ✅ exists | Module landscape; entry point |
| `drupal/seo-geo/seo-recipe-baseline` | ✅ exists | Drupal CMS recipe selection in Phase 3 |
| `drupal/seo-geo/metatag-architecture` | ✅ exists | Cascade order (global → entity → bundle) the chain follows |
| `drupal/seo-geo/core-meta-tags` | ✅ exists | Foundation tags written in steps 2–3 |
| `drupal/seo-geo/open-graph` | ✅ exists | og:* tags in per-bundle defaults |
| `drupal/seo-geo/twitter-cards` | ✅ exists | twitter:* tags |
| `drupal/seo-geo/canonical-urls` | ✅ exists | Canonical URL configuration |
| `drupal/seo-geo/metatag-multilingual` | ✅ exists | hreflang for multilingual sites (when in scope) |
| `drupal/seo-geo/structured-data-decision` | ✅ exists | Schema_metatag vs Schema.org Blueprints choice |
| `drupal/seo-geo/schema-metatag-setup` | ✅ exists | Per-bundle JSON-LD via schema_metatag |
| `drupal/seo-geo/schema-types-reference` | ✅ exists | Bundle role → Schema.org type mapping reference |
| `drupal/seo-geo/pathauto-patterns` | ✅ exists | Pattern syntax + token reference |
| `drupal/seo-geo/redirect-management` | ✅ exists | Redirect module behavior on alias changes |
| `drupal/seo-geo/xml-sitemap` | ✅ exists | simple_sitemap config + per-bundle tuning |
| `drupal/seo-geo/robots-txt` | ✅ exists | robotstxt module vs core scaffold |
| `drupal/seo-geo/breadcrumbs-structured-data` | ✅ exists | BreadcrumbList JSON-LD via easy_breadcrumb |
| `drupal/seo-geo/testing-validation` | ✅ exists | Verifier reference: structured data testing |

### Plays

| Play | Status | Notes |
|---|---|---|
| `drupal/best-practices/camoa/metatag-per-bundle` | ✅ exists | The per-bundle defaults principle |

The remaining SEO stances (adapt-to-project-fields, schema-type-per-role, no-hardcoded-json-ld, sitemap-priority-per-role, one-pathauto-pattern-per-bundle, robotstxt-as-content, google-tag-install-only) are expressed inline in the Opinion section and cite the relevant `drupal/seo-geo/*` guide for their mechanics. The cross-cutting invariants (headless-via-input-contract, halt-on-ambiguity, verifier-runs-adversarially) are expressed structurally by the Input contract, escalation policy, and Verifier sections rather than by a play citation.

### Drupal recipes invoked

The recipe optionally invokes `drupal_cms_seo_basic`, `drupal_cms_seo_tools`, or both (controlled via input). When invoked, the agentic recipe still owns the per-bundle adaptation and verifier; the Drupal core recipes only install the module set + carry their own opinionated config that the agentic recipe then overlays.
