---
# Routing block — an orchestrator reads to here and decides.
name: site_template_publishing
capability: drupal-site-template-publishing
description: Use when turning a working Drupal CMS site into a standalone, marketplace-compliant site template (recipe.yml type Site) produced by exporting a disposable scratch install, not by hand-copying config.
# Metadata — read only after a match.
label: Site template publishing
recipe_schema_version: 1.0.0
version: 0.1.0
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
requires_guides:
  - drupal/recipes
  - drupal/config-management
requires_plays:
  - drupal/best-practices/camoa/ddev-composer-path-repo-drupal-recipe
  - drupal/best-practices/camoa/ship-search-index-view-mode-defensively
  - drupal/best-practices/camoa/schemadotorg-mapping-type-deps-post-export
  - drupal/best-practices/camoa/pre-stable-template-consumer-minimum-stability
  - drupal/best-practices/camoa/rebrand-required-theme-without-forking
  - drupal/best-practices/camoa/canvas-versioned-config-raw-edit-trap
drupal_compatibility: "^11.2"
requires_modules:
  - drupal_cms_helper
invokes_drupal_recipes: []
authors:
  - name: Palcera
license: GPL-2.0-or-later
---

## Goal

Produce a standalone, installable, marketplace-compliant Drupal CMS **site template** — a `type: Site` recipe with a `type: drupal-recipe` composer manifest — from a working seed site, such that a fresh consumer can install it from scratch into a running branded site with demo content, no patches, no version pins, no install-profile dependency, no brand leaks, and proven-clean install + accessibility. The template is **produced by a pipeline, not hand-authored**: a disposable scratch install is genericized in place and exported; the export is the artifact.

## Opinion

**Export from a disposable scratch install, never a long-lived upgraded site.** `drush site:export` reads the LIVE database, so its output is exactly the current state on the current schema. An in-place-upgraded site exports its accumulated cruft — every extension it ever installed lands in the `install:`/`require` lists. Provision a fresh, throwaway drupal/cms install of the seed and export from that. Evidence: the exporter reads the DB against current core/CMS schema by construction; hand-copied YAML goes stale and skips the config→action rewrite.

**Install the seed recipe with `drush site:install <recipe-path>`, not `recipe:apply` on a minimal install.** Core installs Drupal *from* a Site recipe — the canonical path the scaffold's `InstallTest` exercises (it sets `parameters.recipe` and installs from the recipe). Applying a Site recipe onto a bare minimal install is not that supported path.

**Genericize in place, before export — not on the exported YAML.** Because export reads the DB, brand and vertical strings are edited on the running scratch site (content edits + config-level edits + brand-asset overrides). The export inherits a clean state; you never post-edit hundreds of exported files.

**uid1 hygiene: neutralize, don't cancel.** Cancelling uid1 mid-build removes the admin access later steps need. Set uid1 name/mail to neutral placeholders and verify no `user` entities land in `content/`. (Tugboat cancels uid1 *after* install for previews — that is a preview concern, not an export concern.)

**Rebrand a required theme at the template level, never by forking it.** Ship neutral brand assets as managed files and override via theme-settings config; keep the theme a byte-identical caret dependency. Source: play `drupal/best-practices/camoa/rebrand-required-theme-without-forking`.

**Never raw-edit versioned Canvas component configs.** Their `active_version` is a hash of their settings; a raw edit desyncs it. `site:install` masks the break; the recipe CLI validator fails. Source: play `drupal/best-practices/camoa/canvas-versioned-config-raw-edit-trap`.

**Prefer a flat exported recipe over a composed one.** `site:export` emits a flat `install:` list plus full active config, which sidesteps sub-recipe import-ordering traps (e.g. the search view-mode crash). Source: play `drupal/best-practices/camoa/ship-search-index-view-mode-defensively`.

**Post-export patches are standing steps, not one-time edits.** Anything `site:export` regenerates from the DB (schemadotorg mapping deps, Canvas-reseeded brand strings) must be re-applied every export and documented in `AGENTS.md`.

## Preconditions

- Drupal 11.2+ (Canvas requires ^11.2); a drupal/cms `^2.1`-class distro with `drupal_cms_helper` providing `drush site:export`.
- A working seed (config + default content) that installs cleanly from its own Site recipe on the current core/CMS release — provisioned as a **fresh, disposable** scratch install, never the long-lived upgraded site.
- The site-template scaffold (`drupal_cms_site_template_base`) **pre-placed at the export destination** `recipes/<name>/` (it ships unpacked inside the drupal/cms project template; record its provenance from the distro lock). `drush site:export` merges `recipe.yml`/`composer.json` on top of the pre-placed scaffold — there is no `--base` flag.
- DDEV (or equivalent) for the scratch and verify codebases; host Composer available for path-repo require ops (see play `drupal/best-practices/camoa/ddev-composer-path-repo-drupal-recipe`).
- Rights to all shipped imagery (marketplace rule) — provenance documented.
- A consumer codebase for verification, plus drupal/core-dev for the scaffold's PHPUnit tests.

## Input contract

Generic, source-agnostic, supplied by the caller (adapter skill, human operator, or orchestrator).

```yaml
seed:
  recipe_path: string          # path to the seed Site recipe to install FROM
  distro: string               # e.g. drupal/cms:^2.1  (install base)
  required_theme: string       # e.g. vendor/my_theme  (reused unmodified)

package:
  machine_name: string         # e.g. my_site_template  — must NOT be prefixed drupal_cms_ / drupal-cms-
  composer_name: string        # vendor/name  — any Packagist-valid vendor is allowed
  label: string                # human recipe.yml name
  description: string
  license: string              # must be GPL-2.0-or-later

brand:
  neutral_identity: string     # the demo brand to genericize TO (name, vertical, copy tone)
  string_replacements:         # old → new map for content + config leaks
    - from: string
      to: string
  brand_assets:                # neutral logo/favicon to ship as managed files
    - role: string             # logo-light | logo-dark | favicon
      path: string

verify:
  run_scaffold_tests: boolean  # InstallTest / ValidationTest / RequirementsTest (default true)
  run_axe_scan: boolean        # axe-core WCAG scan on rendered pages (default true)
  pages: [string]              # routes to render-check (home, listings, full pages)
```

## Sequence

If invoked in dry-run mode, perform all reads and derivations but emit a preview (planned genericization diff, expected export manifest, compliance-grep plan) instead of mutating any site. Dry-run is required.

1. **Provision the disposable scratch.** Fresh distro codebase (`composer create-project <distro>`), DDEV up. Require the seed sources and the scaffold; on a path repo force `symlink: false` and run require on host Composer (the DDEV container can't resolve a `../sibling` path repo). See play `drupal/best-practices/camoa/ddev-composer-path-repo-drupal-recipe`. Install FROM the seed recipe: `drush site:install <recipe-path>` (never `recipe:apply` on minimal). If the seed applies `drupal_cms_search` on core 11.4, expect and pre-empt the `search_index` view-mode crash — see play `drupal/best-practices/camoa/ship-search-index-view-mode-defensively`.

2. **Genericize in place on the live scratch site.** Apply the brand `string_replacements` across content (nodes, media names/alt, taxonomy terms, Canvas component-tree prop strings) AND config-level leaks (footer region strings, component `default_value` props). For a versioned Canvas config, make the change so Canvas recomputes its `active_version` hash — never raw-edit the hashed settings (play `drupal/best-practices/camoa/canvas-versioned-config-raw-edit-trap`). Ship neutral brand assets as permanent managed files and set theme-settings overrides (play `drupal/best-practices/camoa/rebrand-required-theme-without-forking`). Neutralize uid1 (set name/mail, do not cancel). Resolve any `canvas.*` config carrying `dependencies.content` (export throws otherwise).

3. **Export.** With the scaffold already pre-placed at `recipes/<name>/`, run `drush site:export --destination=recipes/<name>` (the command takes only `--destination`; there is no `--base`). The exporter **merges on top of the pre-placed scaffold** — its CI/Tugboat/tests/`AGENTS.md` are already at the destination — and regenerates `recipe.yml` (flat `install:` list, config→actions, deletes `core.extension`), `composer.json` (`^<installed>` caret constraints, `type: drupal-recipe`, WARNS on non-stable deps), `config/` (full active config as config + actions), and `content/` (core Default Content YAML + binaries, including the shipped brand-asset files). Capture the non-stable-dep warnings verbatim. **Canvas guardrail:** export throws on any `canvas.*` `dependencies.content` and skips `canvas.folder.*`.

4. **Post-export patches (standing, documented in `AGENTS.md`).** Re-apply what export regenerates without: (a) schemadotorg `mapping_type` deps on each mapping — play `drupal/best-practices/camoa/schemadotorg-mapping-type-deps-post-export`; (b) any Canvas component `default_value` re-seeded from the theme's SDC `examples:` (play `drupal/best-practices/camoa/rebrand-required-theme-without-forking`); (c) recipe/composer identity fields (label, description, `finish_url`, composer name/homepage, remove exporter's `_comment`/`version`). Note the exporter drops brand-asset override flags into config as expected — confirm the `use_default: false` overrides landed.

5. **Compliance greps on the GENERATED files.** Fail-closed checks on the export output: no `patches` key; every `require` a caret range (no `==`/exact pins); no install-profile dependency; `type: Site` + `type: drupal-recipe` + `license: GPL-2.0-or-later`; the package name is not prefixed `drupal_cms_`/`drupal-cms-`; zero brand/vertical strings across `config/` + `content/` + manifests (recursive grep of the old identity).

6. **Prove via a fresh consumer.** New distro codebase; add the package via a path repo (`symlink: false`); because the template carries pre-stable deps, set `composer config minimum-stability dev` + `prefer-stable true` first — play `drupal/best-practices/camoa/pre-stable-template-consumer-minimum-stability`. `drush site:install <recipes/<name>>` must exit 0; render-check every `verify.pages` route (200s, brand-string count 0, expected sections present).

7. **Run the scaffold's PHPUnit tests.** With drupal/core-dev in the consumer codebase and `SIMPLETEST_*` env set, run `vendor/bin/phpunit --configuration=web/core recipes/<name>/tests`. InstallTest (installs from the recipe), ValidationTest (applies via the recipe CLI AND asserts every Canvas component used by shipped content exists as `canvas.component.*` config), RequirementsTest. Handle pre-stable minimum-stability for the test codebase the same way as the consumer. Note: PHPUnit 11 boolean flags (`--fail-on-warning`, `--display-deprecations`) take no value. The recipe CLI path (not `site:install`) is what catches a desynced Canvas `active_version` — treat a ValidationTest hash failure as the Canvas raw-edit trap.

8. **axe-core WCAG scan.** Run an axe-core scan over the rendered `verify.pages`; zero critical and zero serious violations is the bar.

9. **Emit summary.** Package identity, export warnings captured, post-export patches applied, compliance-grep counts, install exit code, per-page render/brand-count results, PHPUnit tallies, axe results, and confirmation that the seed/theme source repos are zero-diff.

## Data flow

```
input: seed (recipe_path, distro, required_theme)
       package (machine_name, composer_name, label, license)
       brand (neutral_identity, string_replacements, brand_assets)
       verify (run_scaffold_tests, run_axe_scan, pages)

reads / mutates scratch state:
       live DB of a DISPOSABLE scratch install (content + config)
       theme-settings overrides + permanent managed brand files
       uid1 name/mail (neutralized, not cancelled)

applies opinion (plays):
       ddev-composer-path-repo · ship-search-index-view-mode ·
       schemadotorg-mapping-type-deps · pre-stable-consumer-stability ·
       rebrand-theme-without-forking · canvas-versioned-config-raw-edit-trap

references atomic detail (guides):
       drupal/recipes · drupal/config-management

emits (the shipped package under recipes/<name>/):
       recipe.yml         (type: Site, flat install:, config actions)
       composer.json      (type: drupal-recipe, GPL-2.0-or-later, caret deps)
       config/            (full active config + actions, brand-neutral)
       content/           (core Default Content YAML + brand-asset binaries)
       tests/ + CI + Tugboat + AGENTS.md   (from the pre-placed scaffold)
       screenshot.webp    (neutral demo)

proves (verifier):
       fresh consumer site:install exit 0 · pages 200 · brand-count 0 ·
       PHPUnit InstallTest/ValidationTest/RequirementsTest green ·
       axe 0 critical / 0 serious · source repos zero-diff
```

## State-awareness contract

The scratch and consumer sites are **disposable** — the recipe mutates them freely and tears them down; it must NOT mutate the seed/theme source repos (zero-diff guarantee — verified by `git status` at the end). The shipped package is regenerated wholesale by each export, so genericization is idempotent at the source (same replacements on the same seed state produce the same export), while the post-export patches (step 4) are **not** captured by the DB and MUST be re-applied every export — the recipe treats them as standing, documented steps, not one-shot edits. A re-export followed by re-patch + re-verify is the supported update loop.

## Verifier

Every check is falsifiable and agent-runnable against the generated package and a live consumer install:

1. **Structure (config-assert, no served site):** generated `recipe.yml` has `type: Site`; generated `composer.json` has `type: drupal-recipe` and `license: GPL-2.0-or-later`; package name not prefixed `drupal_cms_`/`drupal-cms-`.
2. **Compliance greps = 0 (config-assert):** no `patches` key; zero exact/`==` version pins (all caret); no install-profile dependency; zero occurrences of the old brand/vertical strings across `config/` + `content/` + manifests.
3. **Post-export patches present (config-assert):** each schemadotorg mapping declares its `mapping_type` in `dependencies.config`; brand-asset overrides carry `use_default: false`; no theme-`examples:`-derived brand string survives.
4. **Install (live-site):** on a fresh consumer with `minimum-stability dev` + `prefer-stable`, `drush site:install <recipes/<name>>` exits 0.
5. **Render (live-site):** every `verify.pages` route returns 200, shows its expected sections, and a brand-string scan of the rendered HTML counts 0.
6. **Scaffold tests (live-site):** InstallTest, ValidationTest, RequirementsTest all pass — a ValidationTest `active_version … does not match hash of settings` failure is a fail-closed signal of the Canvas raw-edit trap, not a skip.
7. **Accessibility (live-site):** axe-core reports 0 critical and 0 serious violations across `verify.pages`.
8. **Source integrity (config-assert):** `git status` on the seed and theme repos is clean.

The recipe ships no verifier *script*, but every check is a runnable method: checks 1–3 and 8 are `config-assert`; checks 4–7 are `live-site` and are **fail-closed, not skipped**, when no served site is available.

## References

### Atomic guides cited

| Guide | Used for |
|---|---|
| `drupal/recipes` | Recipe structure, `type: Site`, flat `install:` vs composed `recipes:`, config actions, import ordering |
| `drupal/config-management` | Active config export, config→action rewrite, dependencies, `core.extension` handling |

### Plays applied

| Play | Source |
|---|---|
| DDEV + Composer path repo for drupal-recipe packages | `drupal/best-practices/camoa/ddev-composer-path-repo-drupal-recipe` |
| Ship `search_index` view mode defensively (Haven pattern) | `drupal/best-practices/camoa/ship-search-index-view-mode-defensively` |
| schemadotorg `mapping_type` dependency enrichment post-export | `drupal/best-practices/camoa/schemadotorg-mapping-type-deps-post-export` |
| Pre-stable template deps require consumer `minimum-stability` | `drupal/best-practices/camoa/pre-stable-template-consumer-minimum-stability` |
| Rebrand a required theme without forking | `drupal/best-practices/camoa/rebrand-required-theme-without-forking` |
| Canvas versioned-config raw-edit trap | `drupal/best-practices/camoa/canvas-versioned-config-raw-edit-trap` |
