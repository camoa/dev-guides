---
# Routing block — an orchestrator reads to here and decides.
name: drupal_seo_foundation
capability: drupal-seo-foundation
description: Use when a Drupal 11.3+ site needs a complete on-page SEO foundation (metatag defaults, Schema.org JSON-LD, XML sitemap, pathauto patterns, redirects, robots.txt, google_tag, 403/404 + non-content defaults), composed from the site's own field inventory and runnable fully unattended via a typed input contract. Leverages drupal_cms_seo_basic + drupal_cms_seo_tools as the baseline; overlays only the gaps; supports `Person`/`Organization` roles, per-bundle `og_type` and date meta, an optional sitemap index, and breadcrumb customization.

# Metadata — read only after a match.
label: Drupal SEO foundation
recipe_schema_version: 1.0.0
version: 0.3.0

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
  - metatag_custom_tags   # only required when `alternate_links` is used (rel="alternate" custom tags)
  - schema_metatag
  - schema_article
  - schema_organization
  - schema_person
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
7. **Metatag entity-type groups.** Emit `metatag.settings.yml` `entity_type_groups` per `metatag_groups_by_bundle` (or the default derived from `semantic_role_by_bundle`) so only the relevant tag groups (basic, open_graph, schema_article, schema_person, …) surface on each bundle's edit form. Sequenced after the per-bundle defaults exist. Source: guide `drupal/seo-geo/metatag-architecture`.
8. **Pathauto patterns.** Per-bundle node patterns + per-vocabulary taxonomy patterns. Source: guide `drupal/seo-geo/pathauto-patterns`.
9. **Sitemap settings.** Per-bundle priority + changefreq (empty `changefreq` allowed = no crawl-frequency hint) + image inclusion. Source: guide `drupal/seo-geo/xml-sitemap`.
10. **Sitemap index.** simple_sitemap 4.x installs the `default` sitemap with type `default_hreflang`, so hreflang needs no step. It also installs the `index` sitemap, disabled. Set `status` in `simple_sitemap.sitemap.index.yml` to `sitemap_index`. The recipe writes no sitemap type and does not change `default_variant`. Source: guide `drupal/seo-geo/xml-sitemap`.
11. **robots.txt content.** `robotstxt.settings.yml` + remove the static `robots.txt` via composer scaffold exclusion. Source: guide `drupal/seo-geo/robots-txt`.
12. **google_tag install + config exclusion.** Install the module and add `google_tag` to `$settings['config_exclude_modules']` in `settings.php` so its environment-specific container config stays out of config sync. The recipe authors no `google_tag` config; the container is configured per environment by the operator.
13. **Breadcrumb structured data.** Verify `easy_breadcrumb` has `add_structured_data_json_ld: true`. Source: guide `drupal/seo-geo/breadcrumbs-structured-data`.
14. **Breadcrumb customization.** When declared, write `easy_breadcrumb.settings.yml` `alternative_title_field` (custom display-label field) and `custom_paths` (path-to-label overrides). Source: guide `drupal/seo-geo/breadcrumbs-structured-data`.

The bundle defaults cannot exist until the per-entity defaults exist; the entity-type groups reference the per-bundle defaults; pathauto patterns cannot generate aliases until the patterns are imported; the sitemap cannot reference URLs until aliases exist — hence the order.

## Preconditions

- Drupal 11.3+ (required by `drupal_cms_seo_basic` and `drupal_cms_seo_tools`, which this recipe leverages).
- Composer-managed install (the recipe writes to `composer.json` and runs `composer require`).
- A writable config sync directory the recipe can author into, and a writable `settings.php` (the recipe appends `google_tag` to `$settings['config_exclude_modules']` when `google_tag` is in scope).
- DDEV runs the site, and `ddev drush` works from the project root. The verifier's commands go through `ddev`.
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
  # role enum: content_article | product | service | web_page | landing_page |
  #            person | organization | none
  #   person       → author/profile-style bundles (Schema.org Person)
  #   organization → tenant/agency/brand bundles  (Schema.org Organization)
  <bundle>: <role>

og_type_by_bundle:                     # og:type per bundle; bundles omitted inherit
  # the node-level default. Source: guide drupal/seo-geo/open-graph
  <bundle>: <og_type>                  # e.g. article | website | product

metatag_groups_by_bundle:              # metatag.settings.yml entity_type_groups —
  # which tag groups surface on each bundle's edit form. DEFAULT IS DERIVED from
  # semantic_role_by_bundle: every role gets basic + open_graph, plus, when
  # schema_org is in scope, its role's group: content_article → schema_article;
  # product → schema_product; service → schema_service; web_page and
  # landing_page → schema_web_page; person → schema_person; organization →
  # schema_organization; none → no schema group. Declare a bundle here only to
  # OVERRIDE the derived set.
  <bundle>: [<group>]                  # e.g. [basic, open_graph, schema_article]

date_fields_by_bundle:                 # drives article_published_time /
  # article_modified_time tokens. Bundles omitted get no date meta. Each bundle's
  # actual date fields differ. Source: guide drupal/seo-geo/open-graph
  <bundle>:
    published: <field_machine_name>    # e.g. field_publication_date | created
    modified: <field_machine_name>     # e.g. field_updated_date | changed

alternate_links: []                    # metatag_custom_tags rel="alternate" links
  # (RSS, AMP, …). Empty = none. Requires the metatag_custom_tags module when used.
  # - {rel: alternate, type: <mime_type>, href: <url>}

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
  og_type: string|null                 # og:type on the front-page default; often
                                       #   differs from the node-level default; null = inherit

sitemap_index: bool                    # status of simple_sitemap.sitemap.index. The
  # index lists every other enabled sitemap. simple_sitemap 4.x installs it disabled
  # and installs the `default` sitemap as type default_hreflang, so hreflang takes
  # no input. Source: guide drupal/seo-geo/xml-sitemap

sitemap_priority_by_role:              # role → (priority, changefreq)
  # changefreq enum: always | hourly | daily | weekly | monthly | yearly | never | ""
  #   "" = emit no changefreq hint (a valid, intentional "don't signal crawlers" stance)
  content_article: {priority: <0.0-1.0>, changefreq: <enum|"">}
  product:         {priority: <0.0-1.0>, changefreq: <enum|"">}
  service:         {priority: <0.0-1.0>, changefreq: <enum|"">}
  web_page:        {priority: <0.0-1.0>, changefreq: <enum|"">}
  landing_page:    {priority: <0.0-1.0>, changefreq: <enum|"">}
  person:          {priority: <0.0-1.0>, changefreq: <enum|"">}
  organization:    {priority: <0.0-1.0>, changefreq: <enum|"">}

pathauto_patterns_by_bundle:           # bundles omitted get no pattern
  <bundle>: <pattern_string>

pathauto_patterns_by_vocabulary:       # vocabularies omitted get no pattern
  <vocabulary>: <pattern_string>

excluded_vocabularies: []              # vocabularies that exist as taxonomies but are
  # NOT part of the public SEO surface: no pathauto pattern, no sitemap setting, no
  # metatag default is authored for them. Declared opt-out so the operator need not
  # name every vocabulary just to silently exclude it.
  # - <vocabulary>

redirect:                              # verified when redirect in layers_in_scope
  auto_redirect: bool                  # expected true
  default_status_code: integer         # expected 301
  suppress_404: bool                   # redirect_404.suppress_404; expected true

robotstxt_content: string              # full robots.txt body
robotstxt_remove_static_scaffold: bool # remove web/robots.txt via composer scaffold

# google_tag has no contract fields — when in scope the recipe installs the module
# and excludes its config via settings.php (config_exclude_modules). The GA4 / GTM
# container is environment-specific and set by the operator per environment.

breadcrumb:                            # easy_breadcrumb.settings.yml customization
  alternative_title_field: string|null # custom field for the breadcrumb display label
                                       #   (e.g. field_breadcrumb_title); null = default
  custom_paths: {}                     # path → label overrides, operator-facing as a map;
  # the recipe serializes it to easy_breadcrumb's native `PATH::LABEL` newline-delimited
  # string form. Empty = none.
  #   <path>: <label>

escalation_policy:                     # per ambiguity class; default = halt
  no_image_field_for_bundle: halt | omit_og_image | use_site_default
  no_description_field_for_bundle: halt | use_fallback | use_static
  url_convention_change_on_live_aliases: halt | apply_with_redirects | skip
  hardcoded_schema_org_blob: halt | apply | skip
  conflict_with_existing_config: halt | overwrite | skip
  unknown_bundle_in_groups_map: halt | apply | drop      # bundle in metatag_groups_by_bundle doesn't exist
  unknown_vocabulary_in_excluded_list: halt | apply | drop  # vocab in excluded_vocabularies doesn't exist
  date_field_missing_on_bundle: halt | omit_date_meta | use_node_created_changed  # date_fields_by_bundle names an absent field
  new_entity_field_required: halt      # always halts; data-model changes out of scope
  content_seed_required: halt          # always halts; content authoring out of scope
```

## Sequence

If `mode: dry-run`, perform all reads and derivations but emit a preview instead of writing.

1. **Validate input contract.** Halt with `contract_error` on missing/inconsistent fields, on bundles that don't exist, on roles that aren't in the enum, on priority chains that name no terminator.

2. **Audit target project state.** Inventory composer.json modules, `core.extension.yml`, per-bundle field lists, existing sync configs matching the in-scope layers, taxonomies, home node. Read-only. Emit a structured `audit.json`. See guide `drupal/seo-geo/overview` for what's worth inventorying.

3. **Reference scan (advisory menu).** Read only `reference_sources`; produce a labelled menu of reference patterns. Filter to `reference_selections`; drop everything else. The recipe never carries unselected reference patterns into the plan. See guide `drupal/seo-geo/seo-recipe-baseline` for the Drupal CMS recipe shape if it's a selected source.

4. **Compose the plan.** For each in-scope layer, walk the contract's rules over the audit:
   - For each bundle in `semantic_role_by_bundle`: compose its per-bundle metatag default by walking `priority_chains` against the bundle's audited fields. Cite the rule and the field for every produced line. Add `og_type_by_bundle` and `date_fields_by_bundle` overrides where declared; halt per `date_field_missing_on_bundle` if a named date field is absent.
   - For `metatag_groups_by_bundle` (or the role-derived default): compose `metatag.settings.yml` `entity_type_groups`; halt per `unknown_bundle_in_groups_map` on an unknown bundle.
   - For each role: derive Schema.org type and sitemap priority/changefreq (empty `changefreq` allowed) from the input mapping. Plan `simple_sitemap.sitemap.index.yml` with `status` set to `sitemap_index`.
   - For each bundle in `pathauto_patterns_by_bundle`: produce the pattern file.
   - For each vocabulary in `pathauto_patterns_by_vocabulary`: produce the pattern file. Vocabularies in `excluded_vocabularies` get no pathauto/sitemap/metatag surface; halt per `unknown_vocabulary_in_excluded_list` on an unknown vocabulary.
   - For `alternate_links` (if any): plan `metatag_custom_tags` `rel="alternate"` entries (requires the `metatag_custom_tags` module).
   - For `breadcrumb` (if declared): plan `easy_breadcrumb.settings.yml` `alternative_title_field` + `custom_paths`.
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
       metatag.settings.yml                           (entity_type_groups per metatag_groups_by_bundle / derived)
       pathauto.settings.yml                          (taxonomy_term enabled if needed)
       pathauto.pattern.<bundle>.yml                  (per bundle in input)
       pathauto.pattern.taxonomy_<vocabulary>.yml     (per vocab in input)
       simple_sitemap.bundle_settings.default.node.<bundle>.yml  (per role mapping; changefreq may be '')
       simple_sitemap.bundle_settings.default.taxonomy_term.<vocab>.yml  (per input; excluded_vocabularies omitted)
       simple_sitemap.sitemap.index.yml               (update; status = sitemap_index)
       robotstxt.settings.yml                         (from input)
       easy_breadcrumb.settings.yml                   (alternative_title_field + custom_paths, if declared)
       settings.php  (config_exclude_modules += google_tag, if in scope)
       core.extension.yml                             (newly-enabled modules)
```

## State-awareness contract

For every emitted config object: absent → create; present and matching the derived spec → skip with `no-op`; present and differing → conflict, do not overwrite unless `escalation_policy.conflict_with_existing_config: overwrite`. A field listed in `priority_chains` that does not exist on **any** in-scope bundle → log warning, drop from chain. A bundle in `semantic_role_by_bundle` whose role implies fields it lacks (e.g. `content_article` without `field_seo_title`) → halt with `contract_error` so the operator either adjusts the role or the chain.

Idempotent: running the recipe twice on identical input and identical project state produces no changes on the second run, including no alias regeneration if no new pattern was added.

## Verifier

Each entry is one command, run from the project root after the recipe ran. It is split on spaces and never run through a shell. A non-zero exit fails the entry, whatever `pass` says. `stdout empty` reads standard output only; a non-interactive `ddev drush` keeps Drush's messages on standard error. A stopped DDEV project prints its start-up text on standard output, so start the site before the verify run. Entries that call `.aida/drupal-seo-foundation/verify.php` run the script in `## Files`. It prints one line per violation, prints a violation when an input it needs is missing, and exits non-zero when it printed any.

verifier:
  - id: metatag-defaults-per-bundle
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/drupal-seo-foundation/verify.php -- metatag-defaults {layers_in_scope:json} {semantic_role_by_bundle:json} {og_type_by_bundle:json}
    pass: stdout empty
  - id: head-per-bundle
    kind: live-site
    run: ddev drush php:script /var/www/html/.aida/drupal-seo-foundation/verify.php -- head {layers_in_scope:json} {semantic_role_by_bundle:json} {og_type_by_bundle:json} {date_fields_by_bundle:json}
    pass: stdout empty
  - id: metatag-groups
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/drupal-seo-foundation/verify.php -- metatag-groups {layers_in_scope:json} {semantic_role_by_bundle:json} {metatag_groups_by_bundle:json}
    pass: stdout empty
  - id: sitemap-settings
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/drupal-seo-foundation/verify.php -- sitemap-settings {layers_in_scope:json} {semantic_role_by_bundle:json} {sitemap_priority_by_role:json}
    pass: stdout empty
  - id: sitemap-served
    kind: live-site
    run: ddev drush php:script /var/www/html/.aida/drupal-seo-foundation/verify.php -- sitemap-served {layers_in_scope:json} {semantic_role_by_bundle:json} {sitemap_priority_by_role:json}
    pass: stdout empty
  - id: sitemap-index
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/drupal-seo-foundation/verify.php -- sitemap-index {layers_in_scope:json} {sitemap_index:json}
    pass: stdout empty
  - id: robots-served-by-module
    kind: live-site
    run: ddev drush php:script /var/www/html/.aida/drupal-seo-foundation/verify.php -- robots {layers_in_scope:json} {robotstxt_content:json} {robotstxt_remove_static_scaffold:json}
    pass: stdout empty
  - id: pathauto-patterns
    kind: self-fixture
    run: ddev drush php:script /var/www/html/.aida/drupal-seo-foundation/verify.php -- pathauto {layers_in_scope:json} {pathauto_patterns_by_bundle:json} {pathauto_patterns_by_vocabulary:json}
    pass: stdout empty
  - id: redirect-config
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/drupal-seo-foundation/verify.php -- redirect-config {layers_in_scope:json} {redirect:json}
    pass: stdout empty
  - id: redirect-on-alias-change
    kind: self-fixture
    run: ddev drush php:script /var/www/html/.aida/drupal-seo-foundation/verify.php -- redirect-fixture {layers_in_scope:json} {redirect:json} {pathauto_patterns_by_bundle:json}
    pass: stdout empty
  - id: google-tag-config-excluded
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/drupal-seo-foundation/verify.php -- google-tag {layers_in_scope:json}
    pass: stdout empty
  - id: excluded-vocabularies
    kind: config-assert
    run: ddev drush php:script /var/www/html/.aida/drupal-seo-foundation/verify.php -- excluded {excluded_vocabularies:json}
    pass: stdout empty
  - id: active-equals-export
    kind: config-assert
    run: ddev drush config:status
    pass: stdout empty

What the entries do not prove, and where the checks went:

- Each script check reads `layers_in_scope` and prints nothing for a layer out of scope. `excluded-vocabularies` and `active-equals-export` run whatever the scope.
- `head-per-bundle`, `sitemap-served` and `robots-served-by-module` request the page in process, through the site's own HTTP kernel, as an anonymous visitor. They need no web server and no base URL, but they read the site's content.
- `head-per-bundle` renders the newest published node of each bundle in `semantic_role_by_bundle`, and skips a bundle that has none. It fails when no bundle has a published node. A tag in the bundle's default that is absent or empty on that node fails the entry. A tag is skipped when every node field its tokens name exists and is empty on that node, such as `og_image` on an article with no image. The same holds for the date tags and the fields `date_fields_by_bundle` names.
- `robots-served-by-module` compares the served body with `robotstxt_content`, trimmed. Lines another module adds through `hook_robotstxt()` make them differ. The in-process request always reaches the module's route. A web server that still serves a static file is covered by the file check, run when `robotstxt_remove_static_scaffold` is true.
- `pathauto-patterns` creates an unpublished node per bundle and a term per vocabulary, then deletes them. The pattern pathauto picks for the new entity must equal the input string, and the saved entity must get an alias. This replaces the old check on the newest entity, which depended on existing content. It also covers the old `ContextException` check: pathauto logs that exception and does not apply the pattern, so the fixture gets no pattern.
- `redirect-on-alias-change` uses the first bundle whose pattern holds `[node:title]`, because a title change must move the alias. It changes the title and reads the redirect repository. It does not request the old alias.
- The fixtures' saves run every module's entity hooks, such as the sitemap queue. The fixture deletes its entities, their aliases and their redirects, and nothing else.
- `sitemap-index` checks that the `default` sitemap exists and is enabled, because the bundle settings name it. It checks that the `index` sitemap has type `index` and a `status` equal to `sitemap_index`. simple_sitemap 4.x keeps no list of sitemaps in the index's configuration. The index lists every enabled sitemap whose type is not `index`.
- `metatag-groups` compares each bundle's groups with the declared override, or with the set the Input contract derives from its role.
- The old idempotency check re-ran `apply`. `active-equals-export` proves the configuration half. Nothing proves "no aliases regenerated", so that half is dropped.
- No entry covers the breadcrumb layers (chain steps 13 and 14), `non_content_defaults`, `home_node`, `alternate_links` or `priority_chains`. The old checks covered none of them either.
- The script in `## Files` is written into the project for the verify run and removed after it. Do not commit or edit it.

## Files

The verifier's script. It runs through `ddev drush php:script`, which passes the arguments after `--` to the script as `$extra`.

```php .aida/drupal-seo-foundation/verify.php
<?php

/**
 * @file
 * Verifier checks for drupal_seo_foundation, run by drush php:script.
 *
 * Usage: drush php:script verify.php -- <check> <json args...>
 * Prints one line per violation and nothing when every assertion holds.
 * Throws after printing, so Drush exits non-zero.
 */

use Symfony\Component\HttpFoundation\Request;

$check = $extra[0] ?? '';
$v = [];

$json = function (int $i) use ($extra) {
  if (!array_key_exists($i, $extra)) {
    throw new \InvalidArgumentException("argument $i is missing");
  }
  $value = json_decode($extra[$i], TRUE);
  if ($value === NULL && trim($extra[$i]) !== 'null') {
    throw new \InvalidArgumentException("argument $i is not JSON");
  }
  return $value;
};

// A layer runs when layers_in_scope names it true; absent means false.
$layers = function () use ($json, &$v) {
  $layers = $json(1);
  if (!is_array($layers)) {
    $v[] = 'layers_in_scope is missing';
    return NULL;
  }
  return $layers;
};
$on = fn(array $layers, string $layer) => !empty($layers[$layer]);

// Role to schema_metatag type tag, its value and its metatag group.
$schema = [
  'content_article' => ['schema_article_type', 'Article', 'schema_article'],
  'product' => ['schema_product_type', 'Product', 'schema_product'],
  'service' => ['schema_service_type', 'Service', 'schema_service'],
  'web_page' => ['schema_web_page_type', 'WebPage', 'schema_web_page'],
  'landing_page' => ['schema_web_page_type', 'WebPage', 'schema_web_page'],
  'person' => ['schema_person_type', 'Person', 'schema_person'],
  'organization' => ['schema_organization_type', 'Organization', 'schema_organization'],
  'none' => NULL,
];

// A page requested in process through the site's own HTTP kernel.
$get = function (string $path) {
  $response = \Drupal::service('http_kernel')->handle(Request::create($path));
  return [$response->getStatusCode(), (string) $response->getContent()];
};

$dom = function (string $html) {
  $doc = new \DOMDocument();
  libxml_use_internal_errors(TRUE);
  $doc->loadHTML('<?xml encoding="UTF-8">' . $html);
  libxml_clear_errors();
  return $doc;
};

$alias = function (string $system_path, string $langcode) {
  $row = \Drupal::service('path_alias.repository')->lookupBySystemPath($system_path, $langcode);
  return $row['alias'] ?? '';
};

$config = fn(string $name) => \Drupal::config($name);

switch ($check) {
  case 'metatag-defaults':
    $layers = $layers();
    if ($layers === NULL || (!$on($layers, 'metatag') && !$on($layers, 'schema_org'))) {
      break;
    }
    $roles = $json(2);
    $og = $json(3);
    if (!$roles) {
      $v[] = 'semantic_role_by_bundle is missing or empty';
      break;
    }
    if ($og === NULL) {
      $v[] = 'og_type_by_bundle is missing';
      break;
    }
    foreach ($roles as $bundle => $role) {
      $defaults = $config("metatag.metatag_defaults.node__$bundle");
      if ($defaults->isNew()) {
        $v[] = "metatag.metatag_defaults.node__$bundle does not exist";
        continue;
      }
      $tags = $defaults->get('tags') ?? [];
      if ($on($layers, 'metatag') && isset($og[$bundle]) && ($tags['og_type'] ?? NULL) !== $og[$bundle]) {
        $v[] = "node__$bundle og_type is " . var_export($tags['og_type'] ?? NULL, TRUE) . ", expected {$og[$bundle]}";
      }
      if (!$on($layers, 'schema_org')) {
        continue;
      }
      if (!array_key_exists($role, $schema)) {
        $v[] = "bundle $bundle has unknown role $role";
        continue;
      }
      if ($schema[$role] === NULL) {
        foreach (array_keys($tags) as $tag) {
          if (str_starts_with($tag, 'schema_')) {
            $v[] = "node__$bundle carries $tag, but role none takes no Schema.org tag";
          }
        }
        continue;
      }
      [$tag, $type] = $schema[$role];
      if (($tags[$tag] ?? NULL) !== $type) {
        $v[] = "node__$bundle $tag is " . var_export($tags[$tag] ?? NULL, TRUE) . ", expected $type";
      }
    }
    break;

  case 'head':
    $layers = $layers();
    if ($layers === NULL || (!$on($layers, 'metatag') && !$on($layers, 'schema_org'))) {
      break;
    }
    $roles = $json(2);
    $og = $json(3);
    $dates = $json(4);
    if (!$roles) {
      $v[] = 'semantic_role_by_bundle is missing or empty';
      break;
    }
    if ($og === NULL || $dates === NULL) {
      $v[] = 'og_type_by_bundle or date_fields_by_bundle is missing';
      break;
    }
    $definitions = \Drupal::service('plugin.manager.metatag.tag')->getDefinitions();
    $checked = 0;
    foreach ($roles as $bundle => $role) {
      $nids = \Drupal::entityQuery('node')->accessCheck(FALSE)
        ->condition('type', $bundle)->condition('status', 1)
        ->sort('created', 'DESC')->range(0, 1)->execute();
      if (!$nids) {
        continue;
      }
      $checked++;
      $node = \Drupal::entityTypeManager()->getStorage('node')->load(reset($nids));
      $path = $alias('/node/' . $node->id(), $node->language()->getId()) ?: '/node/' . $node->id();
      [$code, $html] = $get($path);
      if ($code !== 200) {
        $v[] = "$bundle: $path returned $code";
        continue;
      }
      $head = $dom($html)->getElementsByTagName('head')->item(0);
      if (!$head) {
        $v[] = "$bundle: $path has no <head>";
        continue;
      }
      $metas = [];
      foreach ($head->getElementsByTagName('meta') as $meta) {
        $key = $meta->getAttribute('property') ?: $meta->getAttribute('name') ?: $meta->getAttribute('http-equiv');
        $metas[$key][] = trim($meta->getAttribute('content'));
      }
      $links = [];
      foreach ($head->getElementsByTagName('link') as $link) {
        $links[$link->getAttribute('rel')][] = trim($link->getAttribute('href'));
      }
      $title = trim($head->getElementsByTagName('title')->item(0)?->textContent ?? '');
      $filled = fn(string $name) => ($name === 'title' && $title !== '')
        || array_filter($metas[$name] ?? [], 'strlen')
        || array_filter($links[$name] ?? [], 'strlen');
      // A tag is expected in the head unless every node field its tokens read
      // exists and is empty on this node.
      $expected = function ($value) use ($node) {
        preg_match_all('/node:([a-z0-9_]+)/', is_array($value) ? implode(' ', $value) : (string) $value, $m);
        $names = array_unique($m[1]);
        return !$names || array_filter($names, fn($f) => !$node->hasField($f) || !$node->get($f)->isEmpty());
      };

      if ($on($layers, 'metatag')) {
        $tags = $config("metatag.metatag_defaults.node__$bundle")->get('tags') ?? [];
        if (!$tags) {
          $v[] = "$bundle: metatag.metatag_defaults.node__$bundle holds no tags";
        }
        foreach ($tags as $tag => $value) {
          if (str_starts_with($tag, 'schema_')) {
            continue;
          }
          $name = $definitions[$tag]['name'] ?? NULL;
          if ($name === NULL) {
            $v[] = "$bundle: tag $tag has no enabled plugin";
          }
          elseif ($expected($value) && !$filled($name)) {
            $v[] = "$bundle: $name is absent or empty in the <head> of $path";
          }
        }
        if (isset($og[$bundle]) && !in_array($og[$bundle], $metas['og:type'] ?? [], TRUE)) {
          $v[] = "$bundle: og:type on $path is " . implode(',', $metas['og:type'] ?? ['absent']) . ", expected {$og[$bundle]}";
        }
        if (isset($dates[$bundle])) {
          foreach (['published' => 'article:published_time', 'modified' => 'article:modified_time'] as $key => $name) {
            if ($expected('node:' . ($dates[$bundle][$key] ?? '')) && !$filled($name)) {
              $v[] = "$bundle: $name is absent or empty on $path";
            }
          }
        }
      }

      if ($on($layers, 'schema_org') && isset($schema[$role])) {
        $types = [];
        foreach ($head->getElementsByTagName('script') as $script) {
          if ($script->getAttribute('type') !== 'application/ld+json') {
            continue;
          }
          $data = json_decode($script->textContent, TRUE);
          if (!is_array($data)) {
            $v[] = "$bundle: a JSON-LD block on $path does not parse";
            continue;
          }
          foreach (array_merge([$data], $data['@graph'] ?? []) as $item) {
            $types = array_merge($types, (array) ($item['@type'] ?? []));
          }
        }
        if (!in_array($schema[$role][1], $types, TRUE)) {
          $v[] = "$bundle: no JSON-LD entry on $path has @type {$schema[$role][1]}";
        }
      }
    }
    if ($checked === 0) {
      $v[] = 'no bundle in semantic_role_by_bundle has a published node, so no page was checked';
    }
    break;

  case 'metatag-groups':
    $layers = $layers();
    if ($layers === NULL || !$on($layers, 'metatag')) {
      break;
    }
    $roles = $json(2);
    $declared = $json(3);
    if (!$roles) {
      $v[] = 'semantic_role_by_bundle is missing or empty';
      break;
    }
    if ($declared === NULL) {
      $v[] = 'metatag_groups_by_bundle is missing';
      break;
    }
    $groups = \Drupal::service('plugin.manager.metatag.group')->getDefinitions();
    $actual = $config('metatag.settings')->get('entity_type_groups')['node'] ?? [];
    foreach (array_keys($roles + $declared) as $bundle) {
      if (isset($declared[$bundle])) {
        $want = $declared[$bundle];
      }
      else {
        $want = ['basic', 'open_graph'];
        $role = $roles[$bundle];
        if ($on($layers, 'schema_org') && !empty($schema[$role])) {
          $want[] = $schema[$role][2];
        }
      }
      $have = array_values($actual[$bundle] ?? []);
      sort($want);
      sort($have);
      if ($want !== $have) {
        $v[] = "entity_type_groups.node.$bundle is [" . implode(', ', $have) . '], expected [' . implode(', ', $want) . ']';
      }
      foreach ($want as $group) {
        if (!isset($groups[$group])) {
          $v[] = "group $group for $bundle is not provided by any enabled module";
        }
      }
    }
    break;

  case 'sitemap-settings':
    $layers = $layers();
    if ($layers === NULL || !$on($layers, 'sitemap')) {
      break;
    }
    $roles = $json(2);
    $by_role = $json(3);
    if (!$roles || !$by_role) {
      $v[] = 'semantic_role_by_bundle or sitemap_priority_by_role is missing or empty';
      break;
    }
    foreach ($roles as $bundle => $role) {
      if ($role === 'none') {
        continue;
      }
      if (!isset($by_role[$role])) {
        $v[] = "sitemap_priority_by_role has no entry for role $role";
        continue;
      }
      $settings = $config("simple_sitemap.bundle_settings.default.node.$bundle");
      if ($settings->isNew()) {
        $v[] = "simple_sitemap.bundle_settings.default.node.$bundle does not exist";
        continue;
      }
      if ($settings->get('index') !== TRUE) {
        $v[] = "$bundle: index is not true";
      }
      if (abs((float) $settings->get('priority') - (float) $by_role[$role]['priority']) > 0.0001) {
        $v[] = "$bundle: priority is {$settings->get('priority')}, expected {$by_role[$role]['priority']}";
      }
      if ((string) $settings->get('changefreq') !== (string) $by_role[$role]['changefreq']) {
        $v[] = "$bundle: changefreq is '{$settings->get('changefreq')}', expected '{$by_role[$role]['changefreq']}'";
      }
    }
    break;

  case 'sitemap-served':
    $layers = $layers();
    if ($layers === NULL || !$on($layers, 'sitemap')) {
      break;
    }
    $roles = $json(2);
    $by_role = $json(3);
    if (!$roles || !$by_role) {
      $v[] = 'semantic_role_by_bundle or sitemap_priority_by_role is missing or empty';
      break;
    }
    // Each URL that resolves to a node: [bundle, priority, changefreq].
    $urls = [];
    $queue = ['/sitemap.xml'];
    while ($queue) {
      $path = array_shift($queue);
      [$code, $xml] = $get($path);
      if ($code !== 200) {
        $v[] = "$path returned $code";
        continue;
      }
      $doc = new \DOMDocument();
      if (!@$doc->loadXML($xml)) {
        $v[] = "$path is not XML";
        continue;
      }
      $is_index = $doc->documentElement->localName === 'sitemapindex';
      foreach ($doc->getElementsByTagName($is_index ? 'sitemap' : 'url') as $entry) {
        $loc = trim($entry->getElementsByTagName('loc')->item(0)?->textContent ?? '');
        $parts = parse_url($loc);
        $local = ($parts['path'] ?? '/') . (isset($parts['query']) ? '?' . $parts['query'] : '');
        if ($is_index) {
          $queue[] = $local;
          continue;
        }
        $url = \Drupal::service('path.validator')->getUrlIfValidWithoutAccessCheck($parts['path'] ?? '/');
        if (!$url || !$url->isRouted() || $url->getRouteName() !== 'entity.node.canonical') {
          continue;
        }
        $node = \Drupal::entityTypeManager()->getStorage('node')->load($url->getRouteParameters()['node']);
        if ($node) {
          $urls[] = [
            $node->bundle(),
            trim($entry->getElementsByTagName('priority')->item(0)?->textContent ?? ''),
            trim($entry->getElementsByTagName('changefreq')->item(0)?->textContent ?? ''),
          ];
        }
      }
    }
    foreach (array_unique(array_values($roles)) as $role) {
      if ($role === 'none' || !isset($by_role[$role])) {
        continue;
      }
      $bundles = array_keys($roles, $role, TRUE);
      $of_role = array_filter($urls, fn($u) => in_array($u[0], $bundles, TRUE));
      if (!$of_role) {
        $v[] = "the sitemap lists no URL of role $role (" . implode(', ', $bundles) . ')';
        continue;
      }
      $match = array_filter($of_role, fn($u) => abs((float) $u[1] - (float) $by_role[$role]['priority']) < 0.0001
        && $u[2] === (string) $by_role[$role]['changefreq']);
      if (!$match) {
        $v[] = "no sitemap URL of role $role carries priority {$by_role[$role]['priority']} and changefreq '{$by_role[$role]['changefreq']}'";
      }
    }
    break;

  case 'sitemap-index':
    $layers = $layers();
    if ($layers === NULL || !$on($layers, 'sitemap')) {
      break;
    }
    $want = $json(2);
    if (!is_bool($want)) {
      $v[] = 'sitemap_index is missing or not a boolean';
      break;
    }
    $default = $config('simple_sitemap.sitemap.default');
    if ($default->isNew() || $default->get('status') !== TRUE) {
      $v[] = 'simple_sitemap.sitemap.default is missing or disabled';
    }
    $index = $config('simple_sitemap.sitemap.index');
    if ($index->isNew() || $index->get('type') !== 'index') {
      $v[] = 'simple_sitemap.sitemap.index is missing or not of type index';
    }
    elseif ($index->get('status') !== $want) {
      $v[] = 'simple_sitemap.sitemap.index status is ' . var_export($index->get('status'), TRUE) . ', expected ' . var_export($want, TRUE);
    }
    break;

  case 'robots':
    $layers = $layers();
    if ($layers === NULL || !$on($layers, 'robotstxt')) {
      break;
    }
    $content = $json(2);
    $remove_static = $json(3);
    if (!is_string($content) || !is_bool($remove_static)) {
      $v[] = 'robotstxt_content or robotstxt_remove_static_scaffold is missing';
      break;
    }
    [$code, $body] = $get('/robots.txt');
    $normal = fn(string $s) => trim(str_replace("\r\n", "\n", $s));
    if ($code !== 200) {
      $v[] = "/robots.txt returned $code";
    }
    elseif ($normal($body) !== $normal($content)) {
      $v[] = '/robots.txt does not equal robotstxt_content';
    }
    if ($remove_static && file_exists(DRUPAL_ROOT . '/robots.txt')) {
      $v[] = 'the static robots.txt still exists at ' . DRUPAL_ROOT . '/robots.txt';
    }
    break;

  case 'pathauto':
    $layers = $layers();
    if ($layers === NULL || !$on($layers, 'pathauto')) {
      break;
    }
    $by_bundle = $json(2);
    $by_vocabulary = $json(3);
    if ($by_bundle === NULL || $by_vocabulary === NULL || (!$by_bundle && !$by_vocabulary)) {
      $v[] = 'pathauto_patterns_by_bundle and pathauto_patterns_by_vocabulary are missing or both empty';
      break;
    }
    $generator = \Drupal::service('pathauto.generator');
    $fixtures = [];
    foreach ($by_bundle as $bundle => $pattern) {
      $fixtures[] = ['node', 'node_type', $bundle, ['type' => $bundle, 'title' => "aida verify $bundle", 'status' => 0], $pattern];
    }
    foreach ($by_vocabulary as $vocabulary => $pattern) {
      $fixtures[] = ['taxonomy_term', 'taxonomy_vocabulary', $vocabulary, ['vid' => $vocabulary, 'name' => "aida verify $vocabulary"], $pattern];
    }
    foreach ($fixtures as [$entity_type, $bundle_type, $bundle, $values, $pattern]) {
      if (!\Drupal::entityTypeManager()->getStorage($bundle_type)->load($bundle)) {
        $v[] = "$entity_type bundle $bundle does not exist";
        continue;
      }
      $entity = \Drupal::entityTypeManager()->getStorage($entity_type)->create($values);
      try {
        $generator->resetCaches();
        $found = $generator->getPatternByEntity($entity);
        if (!$found) {
          $v[] = "no pathauto pattern applies to a new $entity_type of $bundle";
        }
        elseif ($found->getPattern() !== $pattern) {
          $v[] = "a new $entity_type of $bundle gets pattern {$found->getPattern()}, expected $pattern";
        }
        $entity->save();
        if ($alias('/' . $entity->toUrl()->getInternalPath(), $entity->language()->getId()) === '') {
          $v[] = "a saved $entity_type of $bundle got no alias";
        }
      }
      finally {
        if (!$entity->isNew()) {
          $entity->delete();
        }
      }
    }
    break;

  case 'redirect-config':
    $layers = $layers();
    if ($layers === NULL || !$on($layers, 'redirect')) {
      break;
    }
    $redirect = $json(2);
    if (!is_array($redirect)) {
      $v[] = 'redirect is missing';
      break;
    }
    foreach (['redirect', 'redirect_404'] as $module) {
      if (!\Drupal::moduleHandler()->moduleExists($module)) {
        $v[] = "$module is not enabled";
      }
    }
    $settings = $config('redirect.settings');
    if ($settings->get('auto_redirect') !== (bool) ($redirect['auto_redirect'] ?? NULL)) {
      $v[] = 'redirect.settings auto_redirect is ' . var_export($settings->get('auto_redirect'), TRUE);
    }
    if ((int) $settings->get('default_status_code') !== (int) ($redirect['default_status_code'] ?? 0)) {
      $v[] = 'redirect.settings default_status_code is ' . var_export($settings->get('default_status_code'), TRUE);
    }
    if ($config('redirect_404.settings')->get('suppress_404') !== (bool) ($redirect['suppress_404'] ?? NULL)) {
      $v[] = 'redirect_404.settings suppress_404 is ' . var_export($config('redirect_404.settings')->get('suppress_404'), TRUE);
    }
    break;

  case 'redirect-fixture':
    $layers = $layers();
    if ($layers === NULL || !$on($layers, 'redirect')) {
      break;
    }
    $redirect = $json(2);
    $by_bundle = $json(3);
    if (!is_array($redirect) || !$by_bundle) {
      $v[] = 'redirect or pathauto_patterns_by_bundle is missing or empty';
      break;
    }
    if (!\Drupal::moduleHandler()->moduleExists('redirect')) {
      $v[] = 'redirect is not enabled';
      break;
    }
    $titled = array_filter($by_bundle, fn($pattern) => str_contains($pattern, '[node:title]'));
    if (!$titled) {
      $v[] = 'no pattern in pathauto_patterns_by_bundle uses [node:title], so a title change cannot move an alias';
      break;
    }
    $bundle = array_key_first($titled);
    $repository = \Drupal::service('redirect.repository');
    $node = \Drupal::entityTypeManager()->getStorage('node')->create(['type' => $bundle, 'title' => 'aida verify redirect first', 'status' => 0]);
    try {
      $node->save();
      $langcode = $node->language()->getId();
      $old = $alias('/node/' . $node->id(), $langcode);
      $node->setTitle('aida verify redirect second')->save();
      $new = $alias('/node/' . $node->id(), $langcode);
      if ($old === '' || $old === $new) {
        $v[] = "a node of $bundle did not change alias when its title changed ('$old' to '$new')";
      }
      else {
        $found = array_filter($repository->findBySourcePath(ltrim($old, '/')),
          fn($r) => ($r->getRedirect()['uri'] ?? '') === 'internal:/node/' . $node->id());
        if (!$found) {
          $v[] = "no redirect from $old to /node/{$node->id()} after its alias changed";
        }
        foreach ($found as $r) {
          if ((int) $r->getStatusCode() !== (int) ($redirect['default_status_code'] ?? 0)) {
            $v[] = "the redirect from $old has status {$r->getStatusCode()}";
          }
        }
      }
    }
    finally {
      if (!$node->isNew()) {
        foreach ($repository->findByDestinationUri(['internal:/node/' . $node->id(), 'entity:node/' . $node->id()]) as $r) {
          $r->delete();
        }
        $node->delete();
      }
    }
    break;

  case 'google-tag':
    $layers = $layers();
    if ($layers === NULL || !$on($layers, 'google_tag')) {
      break;
    }
    if (!\Drupal::moduleHandler()->moduleExists('google_tag')) {
      $v[] = 'google_tag is not enabled';
    }
    if (!in_array('google_tag', \Drupal\Core\Site\Settings::get('config_exclude_modules', []), TRUE)) {
      $v[] = "google_tag is not in \$settings['config_exclude_modules']";
    }
    break;

  case 'excluded':
    $excluded = $json(1);
    if (!is_array($excluded)) {
      $v[] = 'excluded_vocabularies is missing';
      break;
    }
    $handler = \Drupal::moduleHandler();
    foreach ($excluded as $vocabulary) {
      if ($handler->moduleExists('pathauto') && $handler->moduleExists('taxonomy')) {
        $generator = \Drupal::service('pathauto.generator');
        $generator->resetCaches();
        $term = \Drupal::entityTypeManager()->getStorage('taxonomy_term')->create(['vid' => $vocabulary, 'name' => 'aida verify']);
        if ($pattern = $generator->getPatternByEntity($term)) {
          $v[] = "pathauto pattern {$pattern->id()} applies to excluded vocabulary $vocabulary";
        }
      }
      foreach (["simple_sitemap.bundle_settings.default.taxonomy_term.$vocabulary", "metatag.metatag_defaults.taxonomy_term__$vocabulary"] as $name) {
        if (!$config($name)->isNew()) {
          $v[] = "$name exists for excluded vocabulary $vocabulary";
        }
      }
    }
    break;

  default:
    throw new \InvalidArgumentException("unknown check '$check'");
}

foreach ($v as $line) {
  echo $line, "\n";
}
if ($v) {
  throw new \RuntimeException(count($v) . ' violation(s)');
}
```

## References

### Guides

| Guide | Status | Used for |
|---|---|---|
| `drupal/seo-geo/overview` | ✅ exists | Module landscape; entry point |
| `drupal/seo-geo/seo-recipe-baseline` | ✅ exists | Drupal CMS recipe selection in Phase 3 |
| `drupal/seo-geo/metatag-architecture` | ✅ exists | Cascade order (global → entity → bundle) the chain follows |
| `drupal/seo-geo/core-meta-tags` | ✅ exists | Foundation tags written in steps 2–3 |
| `drupal/seo-geo/open-graph` | ✅ exists | og:* tags in per-bundle defaults; og:type-per-bundle (`og_type_by_bundle`); article:published_time/modified_time (`date_fields_by_bundle`) |
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

### Related recipes

- `configure_pathauto_alias_pattern` — the narrow "just give this one bundle a clean URL pattern" case. Route there when the task is aliases only, not a full SEO foundation; this recipe owns pathauto as one of many layers behind the full SEO input contract.
