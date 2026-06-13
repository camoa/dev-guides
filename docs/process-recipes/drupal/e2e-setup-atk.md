---
# Routing block — an orchestrator reads to here and decides.
name: drupal_e2e_setup_atk
capability: e2e-setup
description: Use when a Drupal project (DDEV and Playwright assumed) needs an end-to-end behavioural test harness — installs Automated Testing Kit plus qa_accounts, scaffolds the Playwright host, and wires authenticated journeys into the plugin's e2e gate.
# Metadata — read only after a match.
label: ATK end-to-end test setup (Drupal)
recipe_schema_version: 1.0.0
version: 0.1.0
# Process-recipe routing keys, enforced by validate_recipes.py for any recipe
# under docs/process-recipes/. `capability` above doubles as the phase (the
# lifecycle moment the orchestrator resolves on); there is no separate
# applies_to_phase. `framework` is the second routing dimension.
recipe_class: process
framework: drupal
drupal_compatibility: "^10.3 || ^11"
requires_modules:
  - automated_testing_kit
  - qa_accounts
assumes:
  - ddev
  - playwright
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Stand up an end-to-end behavioural test harness for a Drupal site: Automated Testing Kit and qa_accounts installed, a Playwright host scaffolded against the DDEV runtime, and authenticated user journeys wired into the plugin's deterministic e2e gate so behaviour is protected against regression.

The plugin owns the generic mechanism — when e2e runs, how it is tracked, and the gate verdict. This recipe owns the part the stack-neutral mechanism cannot know: the Drupal-and-ATK binding (module install, qa_accounts auth, surface discovery, gate wiring) for a DDEV-hosted Drupal project.

## Opinion

**DDEV and Playwright are assumed, not branched.** The recipe targets a DDEV-hosted Drupal site driven by Playwright. It carries no alternative-runtime branches. If the host is not DDEV, the agent adapts the runtime commands at execution time — the recipe does not pre-encode every possible host.

**qa_accounts is the auth source, not the lullabot package.** Authenticated journeys log in through ATK's qa_accounts roles via a `drupal-login.ts` fixture. The `@lullabot/playwright-drupal` package is used only for screenshot-plus-accessibility capture in the visual-regression path; the e2e auth path does not use it.

**Behaviour first, pixels elsewhere.** e2e asserts behaviour — navigation, form submission, auth state, redirects — not rendered pixels. Visual regression is a separate phase and a separate recipe. Keep the two concerns out of one spec.

**Reuse ATK's canned coverage; author only the project-specific.** ATK already ships login, logout, and registration journeys. Reference those rather than reimplementing them; discovery proposes only the journeys specific to this project's routes, forms, and roles.

**The gate stays model-free.** The pass/fail verdict comes from Playwright's exit code and JSON results — no model judges it. `drush atk:preflight` plays two distinct roles: a **non-zero preflight exit gates** — `validate-e2e.sh` short-circuits to `verdict: fail` and exits 1 *before Playwright runs* — while preflight warnings emitted on a clean (zero) exit are **advisory** and do not affect the verdict. So preflight is a hard precondition, not merely advisory; only its warnings are advisory. This keeps the gate a zero-model deterministic kernel.

**Test authoring is referenced, not authored here.** How to write an ATK or Playwright test is ATK's and Playwright's own documentation domain. This recipe references origin (see References) and does not duplicate test-authoring instructions.

## Preconditions

- Drupal 10.3+ or 11.x, Composer-managed, with a resolvable `web/` docroot.
- DDEV configured: `.ddev/config.yaml` exists. `ddev` and `npm` are on PATH.
- Playwright is installable on the host (`npx playwright install --with-deps` can run).
- The plugin's generic e2e layer is present: the `validate-e2e.sh` gate, the surface registry, the Playwright base config template, and the idempotency probe. This recipe binds Drupal into that layer; it does not recreate it.

## Input contract

Source-agnostic, supplied by the caller (the orchestrator at the e2e-setup phase, or a human operator).

```yaml
code_path: string             # absolute path to the Drupal project root
skip_demo_recipe: boolean     # default false; skip ATK demo content recipe
journeys:                     # optional; if absent, discovery proposes them
  - slug: string              #   machine name, snake_case, unique
    title: string
    role: string              #   qa_accounts role to run as (or anonymous)
    route: string             #   path under test, e.g. /node/add/article
    priority: string          #   "high" | "medium" | "low"
qa_accounts:                  # optional; role -> credentials map
                              #   defaults to ATK's seeded qa_accounts
```

## Sequence

If invoked in dry-run mode, perform all reads and the idempotency probe but emit a preview instead of writing or installing anything. Dry-run is required.

1. **Validate preconditions and probe state.** Confirm Drupal version, modules, DDEV config, and PATH tools. Run the idempotency probe (a state read, never a mutation) to classify the project as absent, partial, or complete, so a re-run resumes rather than re-installs.

2. **Phase A — Drupal install.** `ddev composer require 'drupal/automated_testing_kit:^2.0'`; `ddev drush en automated_testing_kit qa_accounts -y`. Unless `skip_demo_recipe`: `ddev composer require 'drupal/automated_testing_kit_demo_recipe:^2.0'`, apply the demo recipe, then `ddev drush cache:rebuild`. Skip any step whose result is already present.

3. **Phase B — Playwright host.** Scaffold `tests/e2e/` (mkdir), `npm init -y`, install `@playwright/test@^1.44`, then `npx playwright install --with-deps`.

4. **Phase C — bind into the gate contract.** Copy ATK's bundled Playwright tests and helper directories from the contrib module into the scaffold (with a symlink-safety check). Write `atk.config.js` (baseURL, `drushCmd: 'ddev drush'`, the qa_accounts map), the `drupal-login.ts` fixture, disabled example specs, and a README. Derive `playwright.config.ts` from the plugin's base config and append a single COMMENTED `e2e-chromium` entry to `projects[]`. Seed the surface registry with the ATK-covered e2e surfaces (login at `/user/login`, homepage at `/`, register at `/user/register`, logout at `/user/logout`, content at `/node/1`), each tagged `gates: [e2e]`. Every write is idempotent (per-file if-not-exists; registry entries matched by id).

5. **Discover project journeys.** Invoke the journey-discovery agent. It reads custom `*.routing.yml`, Form classes' `buildForm`, `node.type` and `field.field` config, `*.permissions.yml`, and live `ddev drush role:list`, and proposes journeys with the canned ATK coverage already flagged. The operator confirms which to author. Discovery proposes only; it never overwrites an authored journey.

6. **Author the confirmed journeys.** Write specs for the project-specific journeys, reusing ATK's canned coverage and authenticating through the qa_accounts fixture. The mechanics of writing an ATK or Playwright test are referenced to origin (see References), not reproduced here.

7. **Run the gate.** Execute the plugin's `validate-e2e.sh`, which runs `ddev drush atk:preflight` then `npx playwright test`. A non-zero preflight exit fails the gate immediately (no Playwright run); on a clean preflight, any warnings are advisory and the verdict derives from Playwright's results.

8. **Emit summary.** What was installed, scaffolded, seeded, proposed, authored, skipped as a no-op, or surfaced as a conflict.

## Data flow

```
input: code_path, skip_demo_recipe, journeys (optional), qa_accounts (optional)

reads project state:
       .ddev/config.yaml  +  ddev / npm on PATH
       custom *.routing.yml, src/Form/*.php (buildForm)
       node.type.* / field.field.node.* / *.permissions.yml config
       live  ddev drush role:list
       ATK's bundled Playwright tests and helper directories (contrib)

applies opinion:
       qa_accounts as the auth source · behaviour-first · canned reuse ·
       model-free gate verdict · DDEV/Playwright assumed

references origin (never duplicated):
       ATK module + test-authoring docs · Playwright test/config/fixtures docs

emits:
       Drupal:    automated_testing_kit + qa_accounts enabled (+ demo recipe)
       host:      tests/e2e/ scaffold, package deps, browsers installed
       contract:  atk.config.js, drupal-login.ts fixture, playwright.config.ts,
                  one commented e2e-chromium projects[] entry,
                  registry e2e surfaces (gates: [e2e])
       journeys:  authored project-specific specs (canned coverage reused)
```

## State-awareness contract

The recipe reads existing state before writing. Module installs skip when already enabled. Each scaffold file is written only when absent; the `projects[]` stub is appended once (matched by its `e2e-chromium` marker); registry surfaces are matched by id and skipped when present. Discovery proposes journeys but never overwrites an authored spec.

Idempotent: running the recipe twice on identical input and identical project state produces no changes on the second run — the plugin's idempotency probe drives the resume, classifying the project absent / partial / complete.

## Verifier

After the recipe runs, verify:

1. `automated_testing_kit` and `qa_accounts` are enabled (`ddev drush pm:list`).
2. `tests/e2e/` exists with `atk.config.js`, the `drupal-login.ts` fixture, and a derived `playwright.config.ts`.
3. The surface registry holds the seeded e2e surfaces, each tagged `gates: [e2e]`.
4. The plugin's `validate-e2e.sh` returns a verdict; a known journey passes; an authenticated journey actually logs in through a qa_accounts role.
5. On a clean preflight, the verdict derives from Playwright's results (preflight warnings are advisory); a non-zero preflight exit fails the gate before Playwright runs.

This recipe ships no executable verifier of its own — the checks above are the agent-driven protocol, and the plugin's `validate-e2e.sh` is the runtime gate.

## References

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| Automated Testing Kit (drupal.org/project/automated_testing_kit) | The module, qa_accounts, the bundled Playwright tests and helpers, `drush atk:preflight`, and how to write an ATK test |
| Playwright (playwright.dev) | Test structure, fixtures, config, and the `projects[]` runtime model |
| `@lullabot/playwright-drupal` | Screenshot and accessibility capture — used by the visual-regression path, not by e2e auth |

### Plugin-side generic mechanism (ai-dev-assistant)

The stack-neutral e2e layer this recipe binds Drupal into — the `validate-e2e.sh` gate, the surface registry, the Playwright base config template, and the idempotency probe — is documented in the plugin itself, not duplicated here. The recipe supplies only the Drupal-and-ATK binding on top of that mechanism.
