---
# Routing block — an orchestrator reads to here and decides.
name: site_template_publishing
capability: drupal-site-template-publishing
description: Use when turning a working Drupal CMS site into a standalone, marketplace-compliant site template (recipe.yml type Site) produced by exporting a disposable scratch install, not by hand-copying config.
# Metadata — read only after a match.
label: Site template publishing
recipe_schema_version: 1.0.0
version: 0.2.0
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
requires_guides:
  - drupal/recipes
  - drupal/config-management
  - drupal/tdd/phpunit-configuration
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
- DDEV runs the consumer site for steps 6 to 8, and step 8 needs `npx` with a Chrome driver. The verifier reads files only and needs `jq`.

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
  package_path: string         # the exported package, recipes/<machine_name> in the scratch
                               # codebase; absolute, or relative to where the verifier runs
  consumer_root: string        # the consumer codebase's project root, given the same way
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

6. **Prove via a fresh consumer.** Create a new distro codebase at `verify.consumer_root`; add the package via a path repo (`symlink: false`); because the template carries pre-stable deps, set `composer config minimum-stability dev` + `prefer-stable true` first — play `drupal/best-practices/camoa/pre-stable-template-consumer-minimum-stability`. Run `ddev drush site:install recipes/<name> --yes` in `verify.consumer_root` and record its exit code, which must be 0. Render-check every `verify.pages` route (200s, brand-string count 0, expected sections present). For each page, fetch it from the consumer's DDEV URL with `curl -sS -o <file> -w '%{http_code}'`, then count each `brand.string_replacements` `from` string in it with `grep -cF`. Record the HTTP status, the brand count and whether the expected sections are present, per page.

7. **Run the scaffold's PHPUnit tests.** With drupal/core-dev in the consumer codebase and `SIMPLETEST_*` env set, copy `web/core/phpunit.xml.dist` to `phpunit.xml` at the consumer's project root, rewrite its paths for the docroot, and run `vendor/bin/phpunit -c phpunit.xml recipes/<name>/tests` — see `drupal/tdd/phpunit-configuration`; `-c web/core` runs core's own contrib-wide suite instead. InstallTest (installs from the recipe), ValidationTest (applies via the recipe CLI AND asserts every Canvas component used by shipped content exists as `canvas.component.*` config), RequirementsTest. Handle pre-stable minimum-stability for the test codebase the same way as the consumer. Note: PHPUnit 11 boolean flags (`--fail-on-warning`, `--display-deprecations`) take no value. The recipe CLI path (not `site:install`) is what catches a desynced Canvas `active_version` — treat a ValidationTest hash failure as the Canvas raw-edit trap. Record the PHPUnit status line verbatim; only a line starting `OK (` passes. Skip this step when `verify.run_scaffold_tests` is `false`.

8. **axe-core WCAG scan.** Run an axe-core scan over the rendered `verify.pages`; zero critical and zero serious violations is the bar. Per page, run `npx --yes @axe-core/cli <url> --stdout` and count the violations whose `impact` is `critical` or `serious`. A run that returns no results is a failure, not a zero. Skip this step when `verify.run_axe_scan` is `false`.

9. **Emit summary.** Package identity, export warnings captured, post-export patches applied, compliance-grep counts, install exit code, per-page HTTP status, brand count and expected sections present, the PHPUnit status line, per-page axe critical and serious counts, and confirmation that the seed/theme source repos are zero-diff. Report a skipped step 7 or 8 as skipped.

## Data flow

```
input: seed (recipe_path, distro, required_theme)
       package (machine_name, composer_name, label, license)
       brand (neutral_identity, string_replacements, brand_assets)
       verify (package_path, consumer_root, run_scaffold_tests, run_axe_scan, pages)

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

proves (verifier, static reads of the package):
       structure · compliance · brand-count 0 · post-export patches

reports (steps 6-8, run by the agent):
       fresh consumer site:install exit 0 · pages 200 · brand-count 0 ·
       PHPUnit InstallTest/ValidationTest/RequirementsTest green ·
       axe 0 critical / 0 serious
```

## State-awareness contract

The scratch and consumer sites are **disposable** — the recipe mutates them freely and tears them down; it must NOT mutate the seed/theme source repos (zero-diff guarantee — verified by `git status` at the end). The shipped package is regenerated wholesale by each export, so genericization is idempotent at the source (same replacements on the same seed state produce the same export), while the post-export patches (step 4) are **not** captured by the DB and MUST be re-applied every export — the recipe treats them as standing, documented steps, not one-shot edits. A re-export followed by re-patch + re-verify is the supported update loop.

## Verifier

Each entry is one command, run from the project root after the recipe ran. It is split on spaces and never run through a shell. A non-zero exit fails the entry, whatever `pass` says. `stdout empty` reads standard output only. Every entry calls `.aida/site-template-publishing/verify.sh`, the script in `## Files`. It prints one line per violation and exits non-zero when it printed any.

verifier:
  - id: package-structure
    kind: config-assert
    run: bash .aida/site-template-publishing/verify.sh structure {verify.package_path} {package.machine_name}
    pass: stdout empty
  - id: compliance
    kind: config-assert
    run: bash .aida/site-template-publishing/verify.sh compliance {verify.package_path}
    pass: stdout empty
  - id: no-brand-strings
    kind: config-assert
    run: bash .aida/site-template-publishing/verify.sh brand {verify.package_path} {brand.string_replacements:json}
    pass: stdout empty
  - id: post-export-patches
    kind: config-assert
    run: bash .aida/site-template-publishing/verify.sh patches {verify.package_path} {brand.brand_assets:json}
    pass: stdout empty

What the entries do not prove, and where the proof is:

- The entries read the exported package's files at `verify.package_path` and nothing else. They install nothing and need no DDEV. A missing path prints a violation.
- No entry installs the package, renders a page, runs the scaffold tests or scans accessibility. A verifier entry is always a command, with no kind for an instruction the agent follows. Sequence steps 6 to 8 carry those checks, and step 9 reports their results.
- `package-structure` reads the prefix rule from the name in the generated `composer.json` and from `package.machine_name`.
- `compliance` fails a `patches` or `patches-file` key anywhere in `composer.json`, and any `require` value that does not start with `^`. It does not check "no install-profile dependency": the recipe names no file or key that would carry one.
- `no-brand-strings` scans `recipe.yml`, `composer.json`, `config/` and `content/` for each `from` string, case-sensitive, skipping binary files. Canvas `default_value` strings re-seeded from the theme's SDC `examples:` live in `config/`, so this entry covers them too. An absent or empty `brand.string_replacements` fails it, because an empty scan proves nothing.
- `post-export-patches` checks that each `schemadotorg.schemadotorg_mapping.<entity>.*.yml` lists `schemadotorg.schemadotorg_mapping_type.<entity>` in `dependencies.config`. It reads the default theme from `config/system.theme.yml`, or else from the `system.theme` action in `recipe.yml`. That theme's settings must carry `use_default: false` under `logo` for a `logo-light` or `logo-dark` asset, and under `favicon` for a `favicon` asset. An absent or empty `brand.brand_assets` skips the theme check. The script reads the YAML as Drupal exports it, by indentation, not with a YAML parser.
- No entry checks that the seed and theme repos are unchanged. Rule 7 bars a `git status` check in a recipe that ships `## Files`, and the Input contract has no path for the theme repo. Sequence step 9's summary carries that confirmation.

## Files

One script, which the consumer writes before the verifier runs and removes after it. Do not edit it or commit it. `bash` runs it from the project root.

```sh .aida/site-template-publishing/verify.sh
# Verifier checks for site-template-publishing.
# bash verify.sh structure <package> <machine_name>
#              | compliance <package>
#              | brand <package> <string_replacements JSON>
#              | patches <package> <brand_assets JSON>
# <package> is the exported package directory. Reads files only. Prints one
# line per violation and exits 1 when it printed any; exits 2 on a usage error.
# Needs jq; uses the grep on PATH with POSIX ERE only.
check=${1:-}
a=${2:-}
b=${3:-}
v=0
say() { printf '%s\n' "$*"; v=1; }
# Prints each line of $1 as a violation.
each() {
  [ -n "$1" ] || return 0
  while IFS= read -r line; do say "$check: $line"; done <<EOF
$1
EOF
}
finish() { [ $v -eq 0 ] || exit 1; exit 0; }

case $check in
  structure|compliance|brand|patches) ;;
  *) echo "usage: verify.sh structure|compliance|brand|patches <args>" >&2; exit 2 ;;
esac
command -v jq >/dev/null || { echo "verify.sh needs jq" >&2; exit 2; }

[ -n "$a" ] || { say "$check: verify.package_path is missing"; finish; }
[ -d "$a" ] || { say "$check: verify.package_path $a is not a directory"; finish; }

# Sets $froms to the `from` strings of $1, one per line.
read_froms() {
  case $1 in ''|null) say "$check: brand.string_replacements is missing"; return 1 ;; esac
  froms=$(printf '%s' "$1" | jq -r '.[] | .from // empty') || exit 2
  [ -n "$froms" ] || { say "$check: brand.string_replacements is empty, so there is no old identity to scan for"; return 1; }
}

case $check in
structure)
  case $b in
    '') say "structure: package.machine_name is missing" ;;
    drupal_cms_*|drupal-cms-*) say "structure: package.machine_name $b starts with a drupal_cms_ prefix" ;;
  esac
  if [ -f "$a/recipe.yml" ]; then
    grep -Eq "^type:[[:space:]]*[\"']?Site[\"']?[[:space:]]*$" "$a/recipe.yml" || say "structure: $a/recipe.yml has no top-level type: Site"
  else
    say "structure: $a/recipe.yml is missing"
  fi
  out=$(jq -r '
    (if .type != "drupal-recipe" then "composer.json type is \(.type), not drupal-recipe" else empty end),
    (if .license != "GPL-2.0-or-later" then "composer.json license is \(.license), not GPL-2.0-or-later" else empty end),
    ((.name // "") | split("/") | last | if startswith("drupal_cms_") or startswith("drupal-cms-") then "composer.json name \(.) starts with a drupal_cms_ prefix" else empty end)
  ' "$a/composer.json" 2>/dev/null) || say "structure: $a/composer.json is missing or not JSON"
  each "$out" ;;

compliance)
  out=$(jq -r '
    (paths | map(tostring) | select(.[-1] == "patches" or .[-1] == "patches-file") | "composer.json carries a \(.[-1]) key at \(join("."))"),
    ((.require // {}) | to_entries[] | select(.value | tostring | startswith("^") | not) | "composer.json requires \(.key) at \(.value), not a caret range")
  ' "$a/composer.json" 2>/dev/null) || say "compliance: $a/composer.json is missing or not JSON"
  each "$out" ;;

brand)
  read_froms "$b" || finish
  while IFS= read -r from; do
    out=$(cd "$a" && grep -rlIF -e "$from" -- recipe.yml composer.json config content 2>/dev/null)
    [ -n "$out" ] || continue
    while IFS= read -r file; do say "brand: $a/$file carries '$from'"; done <<EOT
$out
EOT
  done <<EOF
$froms
EOF
  ;;

patches)
  for f in "$a"/config/schemadotorg.schemadotorg_mapping.*.yml; do
    [ -e "$f" ] || continue
    rest=${f##*/schemadotorg.schemadotorg_mapping.}
    want=schemadotorg.schemadotorg_mapping_type.${rest%%.*}
    awk -v want="$want" '
      /^dependencies:/ { d = 1; next }
      d && /^[^[:space:]]/ { d = 0 }
      d && /^  config:/ { c = 1; next }
      d && c && /^  [a-z]/ { c = 0 }
      d && c && /^ *- / { item = $0; sub(/^ *- */, "", item); gsub(/["\047[:space:]]/, "", item); if (item == want) found = 1 }
      END { exit !found }
    ' "$f" || say "patches: $f does not list $want in dependencies.config"
  done
  case $b in '') say "patches: brand.brand_assets is missing"; finish ;; null) finish ;; esac
  roles=$(printf '%s' "$b" | jq -r '.[].role') || exit 2
  [ -n "$roles" ] || finish
  theme=
  if [ -f "$a/config/system.theme.yml" ]; then
    theme=$(sed -n "s/^default:[[:space:]]*[\"']\{0,1\}\([a-z0-9_]*\).*/\1/p" "$a/config/system.theme.yml")
  elif [ -f "$a/recipe.yml" ]; then
    theme=$(awk '
      /^[[:space:]]+system\.theme:[[:space:]]*$/ { match($0, /^[[:space:]]+/); ind = RLENGTH; inb = 1; next }
      inb && /[^[:space:]]/ { match($0, /^[[:space:]]*/); if (RLENGTH <= ind) inb = 0 }
      inb && /^[[:space:]]+default:/ { t = $0; sub(/^[[:space:]]+default:[[:space:]]*/, "", t); gsub(/["\047[:space:]]/, "", t); print t; exit }
    ' "$a/recipe.yml")
  fi
  [ -n "$theme" ] || { say "patches: neither config/system.theme.yml nor a system.theme action in recipe.yml names the default theme"; finish; }
  settings=$a/config/$theme.settings.yml
  [ -f "$settings" ] || { say "patches: $settings is missing, so no brand asset overrides the theme's"; finish; }
  for role in $roles; do
    case $role in
      logo-light|logo-dark) key=logo ;;
      favicon) key=favicon ;;
      *) say "patches: brand asset role $role is not logo-light, logo-dark or favicon"; continue ;;
    esac
    awk -v k="$key" '
      $0 ~ "^" k ":" { b = 1; next }
      b && /^[^[:space:]]/ { b = 0 }
      b && /^[[:space:]]+use_default:[[:space:]]*false[[:space:]]*$/ { f = 1 }
      END { exit !f }
    ' "$settings" || say "patches: $settings $key does not carry use_default: false"
  done ;;
esac

finish
```

## References

### Atomic guides cited

| Guide | Used for |
|---|---|
| `drupal/recipes` | Recipe structure, `type: Site`, flat `install:` vs composed `recipes:`, config actions, import ordering |
| `drupal/config-management` | Active config export, config→action rewrite, dependencies, `core.extension` handling |
| `drupal/tdd/phpunit-configuration` | The consumer's `phpunit.xml` at the project root, its rewritten paths, and why `-c web/core` is wrong |

### Plays applied

| Play | Source |
|---|---|
| DDEV + Composer path repo for drupal-recipe packages | `drupal/best-practices/camoa/ddev-composer-path-repo-drupal-recipe` |
| Ship `search_index` view mode defensively (Haven pattern) | `drupal/best-practices/camoa/ship-search-index-view-mode-defensively` |
| schemadotorg `mapping_type` dependency enrichment post-export | `drupal/best-practices/camoa/schemadotorg-mapping-type-deps-post-export` |
| Pre-stable template deps require consumer `minimum-stability` | `drupal/best-practices/camoa/pre-stable-template-consumer-minimum-stability` |
| Rebrand a required theme without forking | `drupal/best-practices/camoa/rebrand-required-theme-without-forking` |
| Canvas versioned-config raw-edit trap | `drupal/best-practices/camoa/canvas-versioned-config-raw-edit-trap` |
