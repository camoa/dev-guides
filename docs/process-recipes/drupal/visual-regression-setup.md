---
# Routing block — an orchestrator reads to here and decides.
name: drupal_visual_regression_setup
capability: visual-regression
description: Use when a Drupal project (DDEV and Playwright assumed) needs visual-regression coverage — binds Drupal surface discovery, a theme-aware viewport matrix, and authenticated-surface reach into the plugin's generic baseline-and-gate mechanism.
# Metadata — read only after a match.
label: Visual-regression setup (Drupal)
recipe_schema_version: 1.0.0
version: 0.2.0
# Process-recipe routing keys, enforced by validate_recipes.py for any recipe
# under docs/process-recipes/. `capability` above doubles as the phase; there is
# no separate applies_to_phase. `framework` is the second routing dimension.
recipe_class: process
framework: drupal
drupal_compatibility: "^10.3 || ^11"
requires_modules:
  - qa_accounts
assumes:
  - ddev
  - playwright
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Give a Drupal site visual-regression coverage: a discovered set of surfaces (public and authenticated), a theme-aware viewport matrix, deterministic baselines, and a model-free gate that fails on unexpected pixel drift.

The plugin owns the generic mechanism — the baseline manager, the screenshot store, and the gate verdict, all stack-neutral and deterministic. This recipe owns the thin Drupal binding the mechanism cannot know: which Drupal surfaces exist, which viewports the theme actually declares, and how to reach surfaces that require authentication.

## Opinion

**The recipe is thin; the mechanism is generic.** Baseline capture, the screenshot store, and the pass/fail gate are framework-neutral deterministic kernels that stay in the plugin. This recipe contributes only the Drupal-specific inputs to that machine: surface discovery, the viewport matrix, the auth seam, and baseline migration.

**Authenticated reach is the real Drupal seam.** The generic visual path is anonymous-only — it navigates, waits for network-idle and `document.fonts.ready`, and screenshots. Any Drupal surface behind login (an admin listing, an authored node, a role-gated view) is unreachable without auth. This recipe fills that gap by reusing the e2e auth primitive: a qa_accounts login captured once to a Playwright `storageState`, then replayed so authenticated surfaces can be screenshotted. The qa_accounts role is the auth source. When the recipe seeds the registry it maps that role to the schema's generic `auth_context` field (an opaque storageState reference), so the registry stays stack-neutral; anonymous surfaces get a null `auth_context`.

**One auth context = one storageState = one Playwright project chain.** The plugin's generic seam expects each authenticated context `<ctx>` (the `auth_context` token mapped from a qa_accounts `role`) to drive a deterministic file-and-project layout the recipe must produce *exactly* — this is the binding the mechanism cannot guess:

- **Setup spec** `tests/visual/.auth/<ctx>.setup.ts` — logs in for that role and persists the state. Fills the throwing stub with `loginAsRole(page, '<role>')` — an **ATK** helper, imported from the helper catalog the e2e recipe copies into the project (`tests/e2e/helpers/atk/`), **not** an export of `@lullabot/playwright-drupal` — then `await page.context().storageState({ path: STORAGE_STATE })`. The plugin templates this with two stub tokens the recipe substitutes: `__AUTH_CONTEXT__` → `<ctx>`, `__STORAGE_STATE__` → `tests/visual/.auth/<ctx>.json`.
- **storageState** `tests/visual/.auth/<ctx>.json` — the captured session; gitignored (`tests/visual/.auth/*.json`), never committed.
- **Setup project** `visual-setup-<ctx>` — `testDir: './tests/visual/.auth'`, `testMatch: /<ctx>\.setup\.ts$/`.
- **Authed surface project** `visual-chromium-<vp>-<ctx>` — `testDir: './tests/visual/auth/<ctx>'`, `dependencies: ['visual-setup-<ctx>']`, `storageState: 'tests/visual/.auth/<ctx>.json'`. One project per (viewport `<vp>` × context `<ctx>`).
- **Authed surface spec** `tests/visual/auth/<ctx>/<id>.spec.ts`.
- **Isolation** `testIgnore: ['**/.auth/**', '**/auth/**']` on the anonymous projects, so setup specs and authed specs never run unauthenticated.

Anonymous surfaces keep the plain `visual-chromium-<vp>` project and a null `auth_context`; nothing about the anonymous path changes.

**The baseline filename is load-bearing — do not rename the snapshot.** Baselines embed the Playwright project name, so the two paths differ by exactly the `<ctx>` segment:

- **Anonymous:** `<surface-id>-visual-chromium-<viewport>-linux.png` (project `visual-chromium-<vp>`).
- **Authenticated:** `<surface-id>-visual-chromium-<viewport>-<ctx>-linux.png` (project `visual-chromium-<vp>-<ctx>`).

**There is no ordinal segment.** The capture names its snapshot after the surface id — the plugin's starter spec and the `## Screenshot capture` block below both pass `'<surface-id>.png'` — and Playwright drops a supplied name verbatim into the `{arg}` slot of its path template. That is the contract, and changing the snapshot name orphans every committed baseline for the surface.

**The ordinal is the exception, not the rule.** Playwright derives a name, and only then appends a call index, when the capture passes no name at all: the derived name is the test's title path joined and sanitised, plus that index. Under the shipped template's titles (`describe('<surface-id> visual regression')` / `test('visual regression')`) an anonymous capture writes `<surface-id>-visual-regression-visual-regression-1-visual-chromium-<vp>-linux.png` instead. Any helper that takes no snapshot name — `takeAccessibleScreenshot` among them — puts every surface on that form. Pick one naming mode and stay on it; switching re-baselines the whole suite.

Capture baselines on Linux (CI or a Linux container) so the `-linux` suffix matches: it is `process.platform` at capture time, not a label the recipe chooses.

**Behaviour belongs to e2e, pixels belong here.** Visual regression asserts rendered appearance only. Navigation, form, and auth-state assertions live in the e2e recipe. Do not fold behavioural checks into a visual spec.

**DDEV and Playwright are assumed, not branched.** The recipe targets a DDEV-hosted, Playwright-driven Drupal site and carries no alternative-runtime branches; the agent adapts the runtime at execution time if the host differs.

## Preconditions

- Drupal 10.3+ or 11.x, Composer-managed, with a resolvable `web/` docroot.
- DDEV configured (`.ddev/config.yaml`), with `ddev` and `npm` on PATH; Playwright installable.
- The plugin's generic visual layer is present: the baseline manager, the screenshot store, the visual-regression gate, the Playwright base config template, and the surface registry. This recipe binds Drupal into that layer; it does not recreate it.
- For authenticated surfaces: qa_accounts enabled and ATK's `loginAsRole` helper already present in the project — it ships in ATK's Playwright helper catalog, which the e2e recipe copies to `tests/e2e/helpers/atk/`. Run the e2e setup first, or copy that catalog, before wiring an authenticated context. If only public surfaces are in scope, the auth seam is skipped.
- `@lullabot/playwright-drupal` installed, for the settle helper the `## Screenshot capture` block calls. It is a separate package from ATK and supplies no login.

## Input contract

Source-agnostic, supplied by the caller (the orchestrator at the visual-regression phase, or a human operator).

```yaml
code_path: string             # absolute path to the Drupal project root
surfaces:                     # optional; if absent, discovery proposes them
  - id: string                #   stable surface id (drives the baseline filename)
    url: string               #   path to capture, e.g. /admin/content
    role: string              #   qa_accounts role, or "anonymous"; mapped to the registry's auth_context on seed
    masks:                    #   optional CSS selectors to mask (dynamic regions)
      - string
viewports:                    # optional; if absent, derived from the theme
  - string                    #   e.g. "375", "768", "1280"
migrate_from: string          # optional; a memory-project .screenshots/ source
                              #   to import existing baselines from
```

## Sequence

If invoked in dry-run mode, perform all reads and derivations but emit a preview instead of capturing or writing. Dry-run is required.

1. **Discover Drupal surfaces.** If `surfaces` is not supplied, derive candidates from the site: enabled Views config (`views.view.*`), content-type bundles (`node.type.*`, queried through `ddev drush`), and the standard `/admin/*` structural routes. Propose them as registry surfaces with a `url`. The operator confirms; discovery never overwrites an authored surface.

   Masks are **not** proposed alongside the URL — "any obvious dynamic region" is not a procedure, and on a real Drupal site the churning regions are embedded Views that look like ordinary content. Derive them instead:

   a. **Detect.** Fetch each confirmed surface once and count these three signals, which Drupal core emits and a theme cannot suppress:

      | Selector | Emitted by | What it marks |
      |---|---|---|
      | `.views-element-container` | `Drupal\views\Element\View` (a `#type: view` embed) | a View rendered inside another render array — a block, a field formatter, a paragraph |
      | `[class*="js-view-dom-id-"]` | `views-view.html.twig` (`dom_id`) | the wrapper of **every** rendered View. Match on the prefix: the suffix is a per-render hash, so the literal class is not a stable selector |
      | `.contextual-region` | the `contextual` module | a region carrying contextual links — present only for a user who may edit it, so it is a diff source on authenticated captures only |

      Report, per surface, which selectors matched and how many elements each covered, then propose masks from what was found. `.views-element-container` alone covers the common case (a page embedding one or more Views). Never mask blind.

   b. **State the cost before masking.** A mask suppresses noise, and nothing else asks whether it also suppresses the subject. On the run these instructions come from, the mask that absorbed a churning listing covered **29 of 29 teaser cards** on one surface and 32 of 34 on another — it painted over every component the suite exists to protect. Show the element count with the proposal so the operator sees the coverage being given up, and prefer the narrowest selector that still covers the churn (the listing's own wrapper, not the section around it).

   c. **Check the row bound — a mask does not stabilise height.** The mask paints over a region at whatever size that region currently has. An unbounded listing grows a row when an editor publishes, the page gets taller, and a full-page comparison then fails as a **dimension mismatch**: Playwright sizes the image to `document.scrollHeight`, so a height change is rejected before any pixel tolerance is consulted, and no diff image is produced at all. For each region proposed for masking, read the View's pager in `views.view.<name>` — `display.<display_id>.display_options.pager.type`, falling back to the `default` display — and warn when it is `none`. `some`, `mini`, and `full` all bound the row count; `none` does not. An unbounded listing on a full-page surface is a defect to fix in the View, not a tolerance to tune, and the baseline is what surfaces it.

2. **Derive the viewport matrix from the theme.** The plugin's `derive-viewport-matrix.sh` kernel carries no Drupal knowledge — it does not know the `breakpoints.yml` format. This recipe owns that parse and hands the kernel a neutral `[{name, width}]` list via `--breakpoints-from`; the kernel then applies the canonical height band, dedup, and registry JSON shaping (the recipe never reimplements that). Parsing steps:

   a. Resolve the breakpoints file. Drupal keeps themes under `web/themes/` (or the repo root if there is no `web/` docroot). Prefer the sole custom theme under `themes/custom/<theme>/<theme>.breakpoints.yml` — a built Radix sub-theme carries its own. Radix base ships **no** runtime `breakpoints.yml` of its own (only a starterkit template under `src/kits/`), so there is no contrib-Radix fallback file: if no custom-theme breakpoints file resolves, take no file and let the kernel's CSS `@media` scan handle it (the fallback at the tail of this step).

   b. Parse it into `[{name, width}]`. Each top-level `key:` block names a breakpoint (the `name` is the segment after the last dot, so `mytheme.mobile` → `mobile`); read its `weight:` and the `min-width:` inside `mediaQuery:`. Sort by ascending weight, dedup by resolved width. Map the **mobile-first base** to width `375`: in Drupal that base is expressed as a `max-width`-only or empty `mediaQuery` (e.g. Radix `default.xs` is `(max-width: 575px)`), not a literal `min-width: 0` — so the lowest-weight block carrying no `min-width` becomes the 375 mobile viewport, and any further `min-width`-less blocks are dropped. (A literal `min-width: 0`, if a theme uses one, also maps to `375`.) A portable parser:

      ```bash
      THEME_BP="web/themes/custom/<theme>/<theme>.breakpoints.yml"
      awk '
        function flush() { if (cur != "") print w "\t" mw "\t" nm }
        /^[A-Za-z_][A-Za-z0-9_.-]*:[[:space:]]*$/ {
          flush(); cur = $0; sub(/:[[:space:]]*$/, "", cur)
          n = split(cur, p, "."); nm = p[n]; w = 999; mw = "none"; next
        }
        /^[[:space:]]+weight:[[:space:]]*/ { line=$0; sub(/^[[:space:]]+weight:[[:space:]]*/,"",line); w=line+0; next }
        /^[[:space:]]+mediaQuery:[[:space:]]*/ {
          line=$0; if (match(line,/min-width:[[:space:]]*[0-9]+/)) { seg=substr(line,RSTART,RLENGTH); sub(/min-width:[[:space:]]*/,"",seg); mw=seg+0 }
          next
        }
        END { flush() }
      ' "$THEME_BP" | sort -n -k1,1 | awk -F'\t' '
        $3=="" { next }
        {
          if ($2=="none") { if (basedone) next; w = 375; basedone = 1 }   # lowest-weight max-width-only block = mobile base
          else { w = ($2==0 ? 375 : $2) }
          if (!(w in seen)) { seen[w]=1; printf "%s%s", (c++?",":""), "{\"name\":\"" $3 "\",\"width\":" w "}" }
        }
        END { print "" }
      ' | sed 's/^/[/; s/$/]/' > "$CODE_PATH/.viewports-from-recipe.json"
      ```

   c. Feed the kernel: `derive-viewport-matrix.sh <code_path> --breakpoints-from "$CODE_PATH/.viewports-from-recipe.json"`. Strip the `_source` annotation from its output and write the matrix to the registry's top-level `viewports:` block.

   If no theme breakpoints resolve, skip the parse and let the kernel fall back to its generic CSS `@media` scan (`derive-viewport-matrix.sh <code_path>`, optionally `--css-root <dir>`). An explicit `viewports` input overrides both. Clean up the temp `.viewports-from-recipe.json` after the matrix is written.

3. **Establish authenticated reach (skip if all surfaces are anonymous).** For each distinct qa_accounts `role` in scope, derive an `auth_context` token `<ctx>` and stand up the per-context chain the plugin's seam expects (see Opinion): write the setup spec `tests/visual/.auth/<ctx>.setup.ts` from the plugin's stub, substituting `__AUTH_CONTEXT__` → `<ctx>` and `__STORAGE_STATE__` → `tests/visual/.auth/<ctx>.json` — its body is `loginAsRole(page, '<role>')` then `await page.context().storageState({ path: STORAGE_STATE })`. Register the `visual-setup-<ctx>` setup project and, per viewport, the `visual-chromium-<vp>-<ctx>` authed project (`dependencies: ['visual-setup-<ctx>']`, `storageState: 'tests/visual/.auth/<ctx>.json'`, `testDir: './tests/visual/auth/<ctx>'`). Add `tests/visual/.auth/*.json` to `.gitignore` and `testIgnore: ['**/.auth/**', '**/auth/**']` to the anonymous projects. This per-context capture is the gap the generic anonymous-only path cannot fill on its own; authored setup specs and storageState files are never overwritten when already present.

4. **Seed the surface registry.** Write the confirmed surfaces into the registry with `gates: [visual_regression]`, their `url`, the `auth_context` mapped from the qa_accounts `role` (anonymous surfaces get a null `auth_context`), and `masks`.

   **The gate token is `visual_regression`, not `visual`.** The registry's gate vocabulary is exactly `[e2e, visual_regression, visual_parity]`, and the gate collects only surfaces whose `gates` list contains `visual_regression`. A surface tagged `visual` is schema-invalid and invisible to the gate, which then reports `skipped` — "registry has no visual_regression surfaces" — on every run. A skipped gate reads as a configuration choice rather than a failure, so this hides indefinitely.

   This recipe co-owns the same `.visual-review/registry.yml` as the e2e recipe; whichever runs first writes the header, so when this recipe *creates* the registry it must write a `schema_version` (the schema is invalid without it). **Read the current version from the plugin's surface-registry schema at setup time — do not freeze a literal here.** That schema is versioned independently of this recipe and gains optional fields on every minor bump; a hardcoded number is permanently self-misreporting the moment the schema moves.

   Idempotent: surfaces are matched by id and skipped when present.

5. **Migrate existing baselines (optional).** If `migrate_from` points at a memory-project `.screenshots/` source, hand it to the plugin's migration kernel and pass the matrix derived in step 2 (`--viewports-json`) so the legacy `WIDTHxHEIGHT` keys map onto **this theme's** viewport names by nearest width, instead of the kernel's generic phone/tablet/desktop fallback buckets — a bucket name that does not match a `visual-chromium-<vp>` project leaves the image unreachable.

   The kernel already writes the deterministic `<surface-id>-visual-chromium-<viewport>-linux.png` form. **Do not rename its output.** Renaming into any other form — an ordinal variant in particular — orphans every imported image on arrival, because the named capture never looks for that filename. Flag any image that cannot be mapped to a registered surface rather than guessing.

6. **Capture baselines.** Hand off to the plugin's baseline manager (plan, then confirm, then `npx playwright test --update-snapshots`). The recipe does not re-implement capture — it supplies the surfaces, viewports, and auth state the manager consumes. Capture on Linux so the `-linux` suffix is correct.

7. **Run the gate.** Execute the plugin's visual-regression gate (`npx playwright test`, JSON-reported), which diffs against the baselines and derives a model-free verdict.

8. **Emit summary.** Surfaces discovered / confirmed / seeded, viewports derived, auth states captured, baselines migrated or captured, and any drift the gate reported.

## Data flow

```
input: code_path, surfaces (optional), viewports (optional), migrate_from (optional)

reads project state:
       views.view.* / node.type.* config (via ddev drush)
       views.view.<name> pager.type — the row bound behind a mask
       /admin/* structural routes
       rendered surfaces — dynamic-region signals for mask detection
       active default theme's *.breakpoints.yml (Radix + sub-themes)
       qa_accounts roles (for authenticated surfaces)
       an optional memory-project .screenshots/ source

applies opinion:
       thin binding over a generic mechanism · authenticated reach via
       qa_accounts storageState · deterministic baseline filename ·
       pixels-only · DDEV/Playwright assumed

references origin (never duplicated):
       Playwright snapshot/storageState docs · @lullabot/playwright-drupal
       (waitForAllImages — the lazy-content settle before capture) ·
       ATK helper catalog (loginAsRole)

emits:
       registry:   surfaces (gates: [visual_regression]) with url/auth_context/masks
       viewports:  the theme-derived width matrix
       capture:    the ## Screenshot capture block the plugin substitutes into
                   every generated spec (settled, full-page, named snapshot)
       auth:       per-ctx setup spec tests/visual/.auth/<ctx>.setup.ts +
                   storageState tests/visual/.auth/<ctx>.json (gitignored) +
                   projects visual-setup-<ctx> and visual-chromium-<vp>-<ctx>
       baselines:  anonymous  <id>-visual-chromium-<vp>-linux.png
                   authed     <id>-visual-chromium-<vp>-<ctx>-linux.png
                   (migrated or captured via the plugin baseline manager)
```

## State-awareness contract

The recipe reads existing state before writing. Registry surfaces are matched by id: absent → seed; present and matching → skip; present and differing → conflict, do not overwrite, request operator review. Discovery proposes surfaces but never overwrites an authored one. Migrated baselines are renamed to the deterministic form; an image that maps to no registered surface is flagged, never guessed into place.

The baseline filename contract is invariant: the capture keeps naming its snapshot `<surface-id>.png`, so the baseline stays at `<id>-visual-chromium-<vp>-linux.png` and existing images are never orphaned. The authed variant additionally carries the `-<ctx>` project segment (`<id>-visual-chromium-<vp>-<ctx>-linux.png`); the `<ctx>` token is stable per qa_accounts role, so renaming a role's `auth_context` orphans that context's baselines exactly as renaming the snapshot would. Switching the `## Screenshot capture` block to a helper that passes no snapshot name is the same class of break — it moves the whole suite onto the derived-ordinal form and abandons every committed image. Authored setup specs and captured `storageState` files are read before writing — present and matching → skip, present and differing → conflict, never overwrite. Capture on Linux so the platform suffix matches.

Idempotent: running the recipe twice on identical input and identical project state produces no changes on the second run.

## Verifier

After the recipe runs, verify:

1. The surface registry holds the confirmed surfaces, each with `visual_regression` in its `gates` list, a `url`, and (where applicable) a non-anonymous `auth_context`. No surface carries the token `visual` — the gate would not see it, and the run would report `skipped` rather than fail. The registry's `schema_version` matches the version the plugin's surface-registry schema currently declares.
2. The viewport matrix matches the theme's declared breakpoints (or the explicit `viewports` override).
3. For each authenticated context, `tests/visual/.auth/<ctx>.setup.ts` and a captured `tests/visual/.auth/<ctx>.json` (gitignored) exist, the `visual-setup-<ctx>` and `visual-chromium-<vp>-<ctx>` projects are registered, and the visual run reaches the surface logged in (not the login redirect).
4. Baselines exist for every surface-by-viewport pair, captured on Linux, in the **no-ordinal** form: anonymous at `<surface-id>-visual-chromium-<viewport>-linux.png`, authenticated at `<surface-id>-visual-chromium-<viewport>-<ctx>-linux.png`. A filename carrying an ordinal segment means the capture stopped naming its snapshot — check the `## Screenshot capture` block before re-baselining.
5. Each generated spec carries the recipe's capture, not the plugin's native default: the `## Screenshot capture` import is present, the capture call is the one this recipe declares, and the run records the declared `captured_by` rather than `playwright`.
6. Every surface's masks trace to a detected selector, and no surface masks a region whose View pager is `none` without that being flagged.
7. The plugin's visual-regression gate returns a verdict; an unchanged surface passes; a deliberately altered surface fails the diff.

This recipe ships no executable verifier of its own — the plugin's baseline manager and visual-regression gate are the runtime mechanism; the checks above are the agent-driven protocol.

## Screenshot capture

```
screenshot_import: import { waitForAllImages } from '@lullabot/playwright-drupal';
screenshot_capture: await waitForAllImages(page); await expect(page).toHaveScreenshot('__SURFACE_ID__.png', { fullPage: true, mask: masks });
captured_by: drupal-fullpage-settled
```

The plugin substitutes the import and capture lines into every generated surface spec — anonymous and authenticated alike — in place of its framework-neutral default, and records `captured_by` on the surface. **This block is the recipe's only influence over how a surface is captured.** Everything else the recipe supplies is an input: which surfaces, which viewports, which auth context. Capture extent, the settle sequence, and any stabilisation live here or nowhere; with the block absent the plugin captures viewport-only, records `captured_by: playwright`, and no recipe-side correction is possible. Both names are literal — a misspelling degrades silently to the native default rather than failing.

**Why `waitForAllImages`.** It scrolls the page to force every lazy-loaded image to resolve, then returns to the top. A Drupal page with lazy images below the fold is the standard source of a full-page capture that races its own content; this is the settle step, and it runs before the shot rather than being tuned away with a tolerance afterwards. `page.waitForLoadState('networkidle')` and `document.fonts.ready` already run in the template's `beforeEach`; this completes the sequence.

**Why `fullPage: true`.** A viewport-only capture watches only what sits above the fold, which on a long Drupal node is a small fraction of the template — everything below it can be rewritten with the gate staying green. Full-page watches the whole rendered surface. It costs roughly 150 KB per masked baseline (measured), which is not the constraint it is often assumed to be, but it does make page **height** part of the comparison: see step 1c, and bound the listings you mask.

**Why not `takeAccessibleScreenshot`.** The same package exports it, and it does pair a shot with an axe scan, but it is the wrong fit twice over. It passes **no snapshot name**, so adopting it moves every baseline onto Playwright's derived-ordinal filename (see Opinion) and orphans anything already committed — including everything the step 5 migration imports. And it asserts accessibility violations inside the visual test, which the pixels-only opinion puts in another gate. A project that wants it should adopt it deliberately, on an empty baseline set, not inherit it from this recipe.

## Change-impact globs

The plugin's change-impact classifier ships a framework-neutral floor (stylesheet / plain-script / markup extensions) and asks the active framework's recipes for the stack's own view-layer file types. This section is that declaration for the Drupal visual-regression path: it maps each Drupal view-layer file type to the `visual_regression` gate a change to it could justify — a change there can alter rendered output, so it is worth a re-baseline check. The plugin reconstructs this list on the fly each run and **unions** it onto the neutral floor; it also unions across recipes, so these entries deliberately agree with the `review` recipe's `## Change-impact globs` (`checks.md`) — where a glob overlaps, the gates merge and the duplication is harmless. Nothing here is persisted as a project-local file a builder could edit to drop a gate.

| Glob | Gate | Why |
|---|---|---|
| `**/*.twig` | `visual_regression` | Template — but coverage is not implied. A twig change is only watched where a **registered surface renders that template**, and only in a region no mask paints over. Markup written directly into a template, on a page whose listing region is masked and with no component-library surface registered, changes with nothing looking at it. Treat a match here as "re-baseline if a surface covers this", not as proof one does. |
| `**/*.theme` | `visual_regression` | Theme preprocessing alters render arrays (output). |
| `**/*.css` | `visual_regression` | Stylesheet — a direct change to rendered appearance. |
| `**/*.libraries.yml` | `visual_regression` | Asset wiring — which CSS/JS attach to a surface, so a change alters appearance. |

Machine-readable form the plugin lifts directly into `--rules-from`:

```json
{
  "rules": [
    { "glob": "**/*.twig",          "gates": ["visual_regression"] },
    { "glob": "**/*.theme",         "gates": ["visual_regression"] },
    { "glob": "**/*.css",           "gates": ["visual_regression"] },
    { "glob": "**/*.libraries.yml", "gates": ["visual_regression"] }
  ]
}
```

## References

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| Playwright (playwright.dev) | `toHaveScreenshot` snapshots, the `storageState` auth-replay model, and config |
| `@lullabot/playwright-drupal` | `waitForAllImages(page)` — the lazy-content settle the `## Screenshot capture` block runs before the shot. It also exports `takeAccessibleScreenshot(page, testInfo, options)`, which this recipe deliberately does not use (see that section). It exports **no** role-based login: its `login(page, user)` takes a username or uid via a Drush one-time link. |
| Automated Testing Kit (drupal.org/project/automated_testing_kit) | qa_accounts roles (the auth source mapped to each `auth_context` token) and `loginAsRole(page, '<role>')` — the auth primitive each `<ctx>.setup.ts` calls before persisting `storageState`, imported from the ATK helper catalog the e2e recipe copies to `tests/e2e/helpers/atk/` |

### Plugin-side generic mechanism (ai-dev-assistant)

The stack-neutral visual layer this recipe binds Drupal into — the baseline manager, the screenshot store, the visual-regression gate, the Playwright base config template, and the surface registry — is documented in the plugin itself, not duplicated here. The baseline-filename determinism rule above is load-bearing and is enforced wherever the capture runs.
