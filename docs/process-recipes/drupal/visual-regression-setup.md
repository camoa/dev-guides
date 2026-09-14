---
# Routing block, first and in this order. Whoever is resolving reads to here and decides.
name: drupal_visual_regression_setup
capability: visual-regression
description: Use when a Drupal project on DDEV sets up visual regression testing with Playwright. Says what to install, which files to write, which viewports to start from, and how the suite finds its surfaces and names each baseline.
# Metadata, read only after a match.
label: Visual-regression setup (Drupal)
recipe_schema_version: 1.0.0
version: 0.3.0
recipe_class: process
framework: drupal
drupal_compatibility: "^10.3 || ^11"
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Give a Drupal site a visual-regression suite that review can run: Playwright on the host and one
suite under `tests/visual/` that reads the project's surfaces and viewports from
`.visual-review/surfaces.json` at run time, captures each enabled surface at each viewport, and
compares it with a committed baseline named from the two. Once it is set up, review runs the
`visual-regression` row from `drupal/checks.md`, `## Surface commands`, and a person accepts
changed baselines through the `visual-regression-accept` row.

One recipe per kind. This one is the `visual-regression` point; `drupal/e2e-setup-atk.md` is the
`e2e-setup` point, and the two share no file. A project may set up one and never the other.

## Opinion

**The suite is generated from the surface file, at run time.** There is no spec per surface to
write or to keep in step. `surfaces.spec.ts` reads `.visual-review/surfaces.json`, takes every
surface whose `enabled` is true and whose `kinds` include `visual-regression`, and declares one
test per surface and viewport. A surface that is disabled is not a test, so its id never reaches
the output, and review records it as not run from the file rather than reading a pass off a
skipped line. Adding a surface is a `register`, not a file.

**Every test title begins with its surface id, and the id names the baseline.** Review reads the
`list` reporter's output and reads a surface as unmet when its id is absent, so the reporter is part
of the config. The title is `<id> at <viewport>`, and the baseline is
`tests/visual/baselines/<id>-<viewport>.png`, set by `snapshotPathTemplate`. There is no platform
or project segment in the name: baselines are taken on one platform and committed, and a second
platform re-baselines rather than doubling the set. The accept row's `--grep` matches ids against
titles, so `front|about` rewrites those two surfaces at every viewport and no other.

**A missing baseline is a failure, and it writes the baseline.** Playwright prints
`A snapshot doesn't exist`, saves the actual image at the baseline path, and exits 1. The next run
compares against it. So the first run after a `register` is the capture, a person looks at the
image, and the accept row is for a baseline that exists and should change.

**Masks hide what churns; they cost what they cover.** A mask is a CSS selector painted over
before the comparison, and a listing that changes on every publish needs one. But a mask over a
listing hides the listing, which may be what the surface exists to protect. Discovery below says
how a mask is detected and how its cost is counted, and a person confirms each one with that count
in front of them.

**Full page, settled.** A viewport-only capture watches what sits above the fold. The suite
captures the full page, waits for network idle and `document.fonts.ready`, and walks the page once
before the shot, because a full-page capture does not scroll and an image loaded lazily below the
fold would otherwise be missing from it. Animations are disabled and the caret hidden for the
comparison. Page height is therefore part of the comparison: an unbounded listing that grows a row
fails as a size mismatch before any pixel is compared, and that is a listing to bound in its View,
not a tolerance to raise.

**The address is never written down.** The config reads `use.baseURL` from
`PLAYWRIGHT_BASE_URL`, the variable the caller exports for the row, and no file in `## Files` holds
an address.

**Anonymous surfaces only, today.** The surface file carries no authentication field, and nothing
reads one, so a surface behind login is not registered here. A page that redirects anonymous users
to `/user/login` would baseline the login form. When the surface file gains an authentication
context, this recipe gains the login step; until then the boundary is stated rather than worked
around.

**Pixels here, behaviour in e2e.** The suite asserts rendered appearance. Navigation, forms and
login state belong to the e2e kind.

## Preconditions

- Drupal 10.3 or 11, Composer-managed, with the site reachable at an address the caller can export.
- Node 20 or later and `npm` on the host.
- Chromium's system libraries present on the host. `npx playwright install chromium` downloads the
  browser only; on a host missing a library the first run says which, and
  `npx playwright install-deps chromium` installs them with the person's consent.
- The code tree is a git repository with a clean working tree; the consumer commits what the
  install writes, and later the baselines.

## Input contract

The recipe takes nothing from a caller at install. What varies is supplied at run time.

```yaml
PLAYWRIGHT_BASE_URL: string   # exported by the caller for each row; the site's address
.visual-review/surfaces.json: # written by the consumer's install and register steps
  viewports:                  #   from ## Viewports, or the person's --viewport list
    - {name: string, width: integer, height: integer}
  surfaces:
    - id: string              #   kebab case; the title and the baseline name begin with it
      url: string             #   a path under the base URL
      kinds: [visual-regression]
      enabled: boolean        #   a disabled surface has no test
      masks: [string]         #   CSS selectors hidden before the comparison
```

## Sequence

1. **Show.** The consumer prints this recipe's `## Install` lines, the paths under `## Files`, the
   `## Viewports` list, the `## Surfaces` seed and the `## Discovery` prose. A person reads them
   before anything runs.

2. **Install.** The consumer runs each `## Install` line as arguments from the code tree, in
   order, and refuses a line carrying a shell character. Then it writes each `## Files` block where
   the file is absent, and writes the `## Viewports` list into the surface file when the file has
   no viewports; a person's `--viewport <name>=<w>x<h>` list replaces it. A file that exists with
   different content stops the whole install before any command runs, and nothing is overwritten.

3. **Discover and register.** Read the theme's breakpoints and the site's routes, views and
   content types as data (see `## Discovery`), propose surfaces from the `## Surfaces` seed, and
   for each confirmed surface fetch it once and propose masks with the element count each hides.
   A person edits the list; the consumer registers each surface with `kinds` including
   `visual-regression` and its masks, disabled until the person enables it.

4. **Take first baselines.** Run the `visual-regression` row from `drupal/checks.md`. Every
   enabled surface fails with `A snapshot doesn't exist` and writes its image under
   `tests/visual/baselines/`. A person looks at each image, then commits them.

5. **Run the suite.** Run the row again. Every surface passes against its baseline; a changed
   surface fails with the number of differing pixels and writes the actual and diff images under
   `tests/visual/test-results/`.

6. **Accept a change.** When a difference is intended, run the `visual-regression-accept` row with
   the ids to rewrite; it re-captures those surfaces and no other. Commit the new baselines.

## Data flow

```
input at run time: PLAYWRIGHT_BASE_URL, .visual-review/surfaces.json

reads at discovery (as data):
       the default theme's *.breakpoints.yml
       views.view.* config, and each View's pager type
       node.type.* config, the /admin/* structural routes
       each confirmed surface, rendered once, for the mask signals

writes at install:
       host:   @playwright/test in package.json, Chromium downloaded
       tree:   tests/visual/playwright.config.ts, tests/visual/surfaces.spec.ts,
               tests/visual/.gitignore
       file:   viewports into .visual-review/surfaces.json, when it has none

writes at run:
       tests/visual/baselines/<id>-<viewport>.png   committed
       tests/visual/test-results/                   ignored; actual and diff images on a failure

review runs (drupal/checks.md, ## Surface commands):
       visual-regression         → one titled test per enabled surface and viewport
       visual-regression-accept  → the same, --update-snapshots --grep <ids joined by |>
```

## State-awareness contract

Every `## Install` line is safe to run twice: `npm install` and `playwright install` are no-ops when
satisfied. Every `## Files` block is written only where the file is absent, and a file that exists
with different content stops the install before any command runs, so a person's edit to the config
or the suite is never lost and never silently kept either: the consumer names the file and stops.
The viewport list is written into the surface file only when it has none.

Baselines are the suite's memory. They are committed, named from the surface id and the viewport,
and rewritten only by the accept row for the ids a person named, or by a run that found none. A
surface renamed in the surface file orphans its baselines, exactly as a new id would; nothing
here renames an image. `tests/visual/test-results/` is ignored by the `.gitignore` the recipe
writes.

## Verifier

After the install, in the code tree with `PLAYWRIGHT_BASE_URL` exported and at least one surface
registered and enabled:

1. `npx playwright test --config tests/visual/playwright.config.ts` on a surface with no baseline
   exits 1, prints `A snapshot doesn't exist`, and leaves `tests/visual/baselines/<id>-<viewport>.png`
   for every enabled surface and viewport. A disabled surface's id is absent from the output.
2. The same command exits 0 and prints `<id> at <viewport>` once per baseline.
3. After a change to a page, the command exits 1 for that surface with
   `N pixels (ratio R of all image pixels) are different`, and every other surface passes. A
   surface whose churning region is masked passes across reloads.
4. `npx playwright test --config tests/visual/playwright.config.ts --update-snapshots --grep '<id>|<id>'`
   runs only those surfaces' tests, exits 0, and the next plain run passes.
5. `git status` shows the baselines and no `test-results/`.

Observed on 2026-09-13 with Playwright 1.63.0 and Node 22.14: steps 1 to 4 on a served page
with a clock masked and a second page changed (429 pixels, ratio 0.01), and step 1 then 2 against a
fresh Drupal 11 standard install on DDEV 1.25.4.

## Install

Playwright on the host. `npm install` creates `package.json` when the project has none, and adds
to it when it does; no `## Files` block writes that file.

```sh
npm install --save-dev @playwright/test
npx playwright install chromium
```

## Files

```ts tests/visual/playwright.config.ts
import { defineConfig, devices } from '@playwright/test';

// The address comes from the run, never from this file.
const baseURL = process.env.PLAYWRIGHT_BASE_URL ?? '';

export default defineConfig({
  testDir: '.',
  testMatch: /surfaces\.spec\.ts/,
  outputDir: './test-results',
  // Review reads each test's title off standard output; `list` prints every one, passing or failing.
  reporter: 'list',
  // One file per surface and viewport, named by the suite. No platform or project segment:
  // baselines are taken on one platform and committed, and a second platform re-baselines.
  snapshotPathTemplate: '{testDir}/baselines/{arg}{ext}',
  use: { ...devices['Desktop Chrome'], baseURL },
  expect: { toHaveScreenshot: { animations: 'disabled', caret: 'hide' } },
});
```

```ts tests/visual/surfaces.spec.ts
import { test, expect } from '@playwright/test';
import { readFileSync } from 'node:fs';
import path from 'node:path';

// The surface file the surfaces skill writes, read at run time. A surface with enabled false
// is not a test here, so its id never reaches the output and review records it as not run.
type Viewport = { name: string; width: number; height: number };
type Surface = { id: string; url: string; kinds: string[]; enabled: boolean; masks: string[] };
const file = path.resolve(__dirname, '../../.visual-review/surfaces.json');
const doc = JSON.parse(readFileSync(file, 'utf8')) as { viewports: Viewport[]; surfaces: Surface[] };
const surfaces = doc.surfaces.filter((s) => s.enabled && s.kinds.includes('visual-regression'));

for (const surface of surfaces) {
  for (const viewport of doc.viewports) {
    // The title begins with the surface id: review reads the id off this line, and the accept
    // row's --grep selects on it.
    test(`${surface.id} at ${viewport.name}`, async ({ page }) => {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await page.goto(surface.url, { waitUntil: 'networkidle' });
      await page.evaluate(() => document.fonts.ready);
      // A full-page capture does not scroll, so an image loaded lazily below the fold would be
      // missing from it. Walk the page once, then return to the top.
      await page.evaluate(async () => {
        for (let y = 0; y < document.body.scrollHeight; y += window.innerHeight) {
          window.scrollTo(0, y);
          await new Promise((r) => setTimeout(r, 50));
        }
        window.scrollTo(0, 0);
      });
      await expect(page).toHaveScreenshot(`${surface.id}-${viewport.name}.png`, {
        fullPage: true,
        mask: surface.masks.map((selector) => page.locator(selector)),
      });
    });
  }
}
```

```gitignore tests/visual/.gitignore
# Playwright's per-run output: the actual and diff images of a failed comparison.
test-results/
```

## Viewports

The list the surface file starts with. The theme decides the real one: `## Discovery` says how to
read it from the theme's breakpoints, and a person's `--viewport <name>=<w>x<h>` list replaces
these.

```json
[
  {"name": "mobile", "width": 390, "height": 844},
  {"name": "tablet", "width": 768, "height": 1024},
  {"name": "desktop", "width": 1440, "height": 900}
]
```

## Surfaces

Seed rows for discovery, in the surface file's shape: the pages every Drupal site renders. A
person edits the list before anything is registered.

```json
[
  {"id": "front", "url": "/", "kinds": ["visual-regression"]},
  {"id": "login", "url": "/user/login", "kinds": ["visual-regression"]},
  {"id": "not-found", "url": "/this-page-does-not-exist", "kinds": ["visual-regression"]}
]
```

## Discovery

Read these from the code tree and the running site, every one as data.

**Viewports, from the theme.** The default theme's `<theme>.breakpoints.yml`, under
`web/themes/custom/<theme>/` for a built sub-theme. Each top-level key is a breakpoint; read its
`weight` and the `min-width` inside `mediaQuery`. Sort by weight and drop repeated widths. The
lowest-weight breakpoint with no `min-width` is the mobile base; give it the mobile width below.
Radix ships no runtime `breakpoints.yml` of its own, only a starterkit template, so a Radix
sub-theme's file is the one to read, and a theme with none keeps the `## Viewports` list. Propose
one viewport per breakpoint, with a height from the device class (844 for a phone, 1024 for a
tablet, 900 for a desktop), and pass the confirmed list as `--viewport` at install.

**Surfaces, from the site.** One surface per rendering template a person can reach anonymously:
the front page; one node of each content type in `node.type.*`, by its path; each page display of
an enabled View in `views.view.*`, by its `display.<id>.display_options.path`; the `/user/login`
form; and a 404. Propose each with its path as `url`. A path that redirects anonymous users to
login is not a surface here (see Opinion). Say when two candidates render the same template so
the person keeps one.

**Masks, from the rendered page.** Fetch each confirmed surface once and count the elements
matching three selectors Drupal core emits and a theme cannot suppress:

| Selector | Emitted by | What it marks |
|---|---|---|
| `.views-element-container` | `Drupal\views\Element\View`, a `#type: view` embed | a View rendered inside a block, a field formatter or a paragraph |
| `[class*="js-view-dom-id-"]` | `views-view.html.twig`, `dom_id` | the wrapper of every rendered View; match on the prefix, the suffix is a per-render hash |
| `.contextual-region` | the Contextual Links module | a region with edit links; present only for a user who may edit, so a diff source on authenticated captures, none here |

Report, per surface, which selectors matched and how many elements each covered, and propose a
mask only from what was found, with that count beside it: a mask that covers 29 of a page's 29
teaser cards paints over everything the surface exists to protect, and the person decides with
that number in view. Prefer the narrowest selector that still covers the churn, the listing's own
wrapper rather than the section around it. For each View behind a proposed mask, read
`display.<display_id>.display_options.pager.type` in `views.view.<name>`, falling back to the
`default` display, and warn when it is `none`: `some`, `mini` and `full` bound the row count and
`none` does not, so an unbounded listing grows the page when an editor publishes and the
comparison fails as a size mismatch before any mask applies. That is a View to bound, and the
proposal says so. A person confirms every surface and every mask; nothing here is written until
they do.

## References

| Source | Used for |
|---|---|
| Playwright (playwright.dev) | `toHaveScreenshot`, `snapshotPathTemplate` and its `{arg}` slot, `mask`, `fullPage`, `--update-snapshots`, `--grep`, the `list` reporter |
| Drupal core: `Drupal\views\Element\View`, `views-view.html.twig`, the Contextual Links module | The three mask signals above and what each marks |
| Drupal core: the Breakpoint module's `*.breakpoints.yml` | The theme's breakpoints discovery reads for viewports |
| `drupal/checks.md`, `## Surface commands` | The `visual-regression` and `visual-regression-accept` rows review runs over this harness |
| `drupal/e2e-setup-atk.md` | The other kind, under `tests/e2e/`, sharing no file with this one |
