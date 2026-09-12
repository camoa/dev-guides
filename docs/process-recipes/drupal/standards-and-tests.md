---
# Routing block — an orchestrator reads to here and decides.
name: drupal_implement_standards_and_tests
capability: implement
description: Use when a Drupal project enters the implementation phase holding a test that already fails, and must turn it green under Drupal/PHP coding standards and the implementation-time security rules — applies the no-static-service rule and the Form-API / Twig / parameterized-query guarantees, then refactors under a green bar. Which tier the test sits at and how it is written belong to the test-authoring recipe; linter execution is deferred to the code-quality-tools plugin.
# Metadata — read only after a match.
label: Coding standards and test discipline (Drupal)
recipe_schema_version: 1.0.0
version: 0.6.0
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
requires_guides:
  - development/tdd-spec-driven
  - drupal/tdd
  - drupal/testing
  - drupal/security
  - drupal/best-practices/camoa
# Process-recipe routing keys, enforced by validate_recipes.py for any recipe
# under docs/process-recipes/. `capability` above doubles as the phase (the
# lifecycle moment the orchestrator resolves on); there is no separate
# applies_to_phase. `framework` is the second routing dimension.
recipe_class: process
framework: drupal
drupal_compatibility: "^10.3 || ^11"
assumes:
  - composer
  - ddev
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Hold Drupal implementation-phase code to the standard it must meet before it can be reviewed: Drupal/PHP coding standards applied as the code is written, the implementation-time security rules guaranteed (Form API tokens, Twig auto-escaping, parameterized queries, no static service access in new code), and a test that arrived red turned green without weakening it. The judgement of *which* standard applies is the recipe's; running the linters is the code-quality-tools plugin's; choosing and writing the test is `drupal/test-authoring.md`'s.

The plugin owns the generic mechanism — when the implementation phase runs, the test-first gate that blocks completion, and how findings are recorded against the task. This recipe owns the part the stack-neutral mechanism cannot know: how Drupal coding standards are actually applied, and what the Drupal security rules are at implementation time.

## Opinion

**The test is written first, and it is seen to fail.** No production code is written until a test for the behaviour exists and has been run to confirm it fails (RED) for the right reason — the behaviour is absent. Not a typo in the test, and not working code you broke or reverted to produce the failure; that proves the test is sensitive, never that it came first (see `development/tdd-spec-driven/what-a-failing-test-proves`). Then the minimum code to pass (GREEN), then refactoring under a green bar (REFACTOR). A test that passes on its first run is suspect: it is probably asserting nothing. "Too simple to test" is not a reason to skip; simple now is complex later.

**No static `\Drupal::` in new code.** New code names every collaborator it needs by constructor injection — `\Drupal::service(...)`, `\Drupal::entityTypeManager()`, and friends are a hidden, untestable dependency and are blocking in the service layer. Static `\Drupal::` is tolerated only in procedural `.module` glue and in code Drupal does not let you inject into, never in a class this phase writes. This is the implementation-time twin of the architecture phase's service rule, and it is what makes the code unit-testable in the first place.

**Security is a property of the code, not a later audit.** Four guarantees hold at implementation time: Form API builds and validates every data-entry form so its CSRF token is present and checked; output is escaped — Twig auto-escaping is left on and never defeated with `|raw` or an unsanitised render-array `#markup`; database access is parameterized through the query builder or placeholders, never string-concatenated user input; and access checks are present on every route and operation. A security issue found here is fixed here, not deferred.

**The tier, the file and the test's name are not decided here.** Which tier a behaviour belongs at, where the test file goes, what it is called, how the criterion it specifies is traced to it, and what a Drupal test may not do are the `test-authoring` recipe's — `drupal/test-authoring.md`. That reader writes the test and stops at red; this one takes the red test and makes it green. The rules are stated once, there, because a reader that may not write production code cannot be handed this file.

**Coverage that runs against a site already standing does not count toward the test-first requirement.** The Playwright/ATK suite the `e2e-setup` recipe configures and the snapshot baselines the `visual-regression` recipe configures are outer verification: they cannot drive a design decision, and they are written after the behaviour exists. Report them separately. Which tiers *are* inside the loop is stated in `drupal/test-authoring.md`.

**Adding a test is not automatically progress.** The loop's requirement for a change is one specification per behaviour the change creates, at the tier `drupal/test-authoring.md` chose, each seen to fail first *because the behaviour it names did not exist yet* — and past that, more tests make the change harder to review without specifying anything new. The full set of cases (a test written after the code, a duplicate one tier up, an assertion on an unpromised surface) belongs to `development/tdd-spec-driven` and is cited, not restated, and the Drupal-specific forms are stated in `drupal/test-authoring.md` beside the reader that would write them.

**Standards are applied by judgement; linters are run by the tooling.** This recipe decides what Drupal coding standards mean for the code in front of it — PSR-12/Drupal layout, docblocks on classes and public methods, type hints, no deprecated APIs, PascalCase classes / camelCase methods. The *execution* of `phpcs --standard=Drupal,DrupalPractice` and `phpstan` is the code-quality-tools plugin's job; this recipe references that plugin for the run and does not re-author the linter invocation.

**Mechanics are referenced, not re-authored.** *How* a PHPUnit test base is extended, how a Kernel test installs its schema, how Twig escaping or the Form API token actually work, and what the house conventions are belong to the knowledge guides. This recipe references `drupal/tdd`, `drupal/testing`, `drupal/security`, and `drupal/best-practices/camoa` for those mechanics and stays focused on the discipline applied on top of them.

**The recipe enforces and writes code under discipline; it does not own the gate.** Recording pass/fail against the task and blocking task completion is the plugin's implementation phase. This recipe supplies the Drupal method the gate evaluates.

## Preconditions

- A Drupal 10.3+ or 11.x project, Composer-managed, with a DDEV environment. The conditions for *running* a test — the runner reachable through the project's documented invocation, and the environment each tier needs — are declared by the `test-execution` recipe for this framework, which is where the commands that need them live.
- The design phase has produced an architecture decision (see the `architecture` recipe) — the services, Drush commands, forms, and storage to implement are known, so this phase tests and builds against a plan rather than improvising structure.
- The code-quality-tools plugin is available for linter execution (`phpcs --standard=Drupal,DrupalPractice`, `phpstan`); this recipe does not bundle or re-author those runners.
- The plugin's generic implementation phase is present: the test-first gate and the task record. This recipe supplies the Drupal-specific standards-and-tests method; it does not recreate the gate.

All four stay prose. They are design-artifact and plugin-availability conditions with no argv-safe filesystem probe, and the one condition that did carry a machine-readable entry — the PHPUnit runner — moved to the `test-execution` recipe, which owns the commands it is a condition of. Its check moved with a correction: `test -x vendor/bin/phpunit` reported `met` with DDEV stopped and nothing set, because Composer installs that binary regardless.

```yaml
preconditions: []
```

## Input contract

Source-agnostic, supplied by the caller (the orchestrator at the implementation phase, or a human operator).

```yaml
code_path: string             # absolute path to the Drupal project root
component: string             # the unit being implemented (a service, form, Drush command…)
behavior: string             # the specific behaviour to test-drive and build
test_tier: string             # the tier the test-authoring recipe chose, carried through
architecture_ref: string      # optional; pointer to the design decision this implements
```

## Sequence

If invoked in dry-run mode, perform all reads and emit a standards-and-security plan (what the code must do to turn the test green, and the standards and security checklist it must hold) instead of writing production code. Dry-run is required.

1. **Take the failing test.** The tier, the file, the namespace, the test name and the criterion it carries are `drupal/test-authoring.md`'s, and it hands them over red. Confirm the failure is an assertion that ran and did not hold rather than a harness error or a run that selected nothing — `drupal/test-execution.md` declares how to tell those apart. A behaviour arriving with no failing test does not enter this phase; send it back.

2. **Confirm the red is the right red.** The behaviour is absent — not a broken test, and not working code broken or reverted to force the failure, which proves the test is sensitive and never that it came first (see `development/tdd-spec-driven/what-a-failing-test-proves`). A test that passed on arrival is not a starting point; return it. Once a test is committed, who may change or delete it is the mutability matrix's answer in `development/tdd-spec-driven`, not this phase's — and this phase changes none.

3. **Write the minimum code to pass (GREEN).** Implement only what the test demands — no extra features, no premature optimisation, no "while I'm here" additions. As you write, hold the standards inline: constructor-inject every dependency (no static `\Drupal::` in the new class), docblocks on the class and public methods, type hints on parameters and returns, no deprecated APIs, Drupal layout and naming. Run the test to green.

4. **Apply the implementation security rules.** Before the unit is considered done, confirm the four guarantees against `drupal/security`: Form API builds/validates every data-entry form (CSRF token present and checked); output is escaped (Twig auto-escaping intact, no unsanitised `|raw` or `#markup`); all database access is parameterized (query builder / placeholders, never concatenated user input); and access checks cover every route and operation. Any gap is fixed now. Where the fix needs a test to prove it, that test is authored by `drupal/test-authoring.md` and arrives red like any other; this phase does not write it.

5. **Refactor under green (REFACTOR).** With tests green, improve structure without changing behaviour — extract duplication into a service or trait, lean on Drupal base classes, align with the house conventions in `drupal/best-practices/camoa`. Re-run the tests; they stay green or the refactor is reverted.

6. **Defer the linters to the tooling, then hand back.** Invoke the code-quality-tools plugin to run `phpcs --standard=Drupal,DrupalPractice` and `phpstan` over the changed files — this recipe judges what the standards mean but does not re-author or replace that run. Return the test results, the security-rule confirmation, and the linter outcome to the caller; the plugin's implementation phase records them against the task and owns the completion gate. The recipe writes production code for the component, changes no test, and writes no task record of its own.

## Data flow

```
input: code_path, component, behavior, test_tier (optional), architecture_ref (optional)

reads project state:
       architecture decision (the design being implemented)
       existing custom module: src/, *.services.yml, tests/src/, *.routing.yml
       existing tests for the component (to extend, not duplicate)

applies opinion:
       test-first (RED→GREEN→REFACTOR) · no static \Drupal:: in new code ·
       Form-API tokens · Twig auto-escaping · parameterized queries ·
       access checks · tier matched to dependency surface ·
       standards by judgement, linters by tooling

references origin (never duplicated):
       drupal/tdd                  — Red-Green-Refactor cycle and test-first discipline
       drupal/testing              — Unit / Kernel / Functional / FunctionalJavascript base classes and mechanics
       drupal/security             — Form API tokens, output escaping, query parameterization, access
       drupal/best-practices/camoa — house coding conventions
       code-quality-tools (plugin) — phpcs --standard=Drupal,DrupalPractice + phpstan execution

emits (to the caller; the recipe writes no task record):
       tests:        the test(s) per component, at the chosen tier, seen to fail on an
                     absent behaviour then pass
       code:         the minimum production code that turns them green
       security:     confirmation of the four implementation-time guarantees
       linting:      the code-quality-tools run outcome over the changed files
```

## State-awareness contract

The recipe reads existing state before writing. The architecture decision, the current module layout (`src/`, `*.services.yml`, `*.routing.yml`), and the tests that arrived for the component are read so new code extends the design rather than colliding with it. The method writes production code for the component under implementation, changes no test, installs nothing and writes no task record — the results are returned to the caller, which owns recording them and gating completion.

Idempotent at the discipline level: re-running on a component whose tests already pass and whose standards and security rules already hold produces no new change — the tests stay green, the linters stay clean, nothing is rewritten. A change on re-run means a regression was found or the behaviour moved, which is the method reflecting current reality, not non-determinism.

## Verifier

After the recipe runs, verify:

1. Every implemented behaviour arrived with a PHPUnit test that had been seen to fail *because the behaviour was absent* — not because working code was broken or reverted, and no test passed on arrival unexamined. The tier that test sits at is `drupal/test-authoring.md`'s choice, verified there.
2. No new class reaches for a static `\Drupal::` service; every dependency is constructor-injected.
3. The four security guarantees hold: Form API on every data-entry form (token present and checked), Twig auto-escaping intact (no unsanitised `|raw`/`#markup`), all database access parameterized, access checks on every route and operation.
4. New code carries docblocks on classes and public methods, type hints on parameters and returns, no deprecated APIs, and Drupal layout/naming — and the code-quality-tools `phpcs --standard=Drupal,DrupalPractice` and `phpstan` run over the changed files is clean (or its findings are recorded for the gate).
5. The tests are green and the refactor (if any) left them green; the results were returned to the caller for the plugin's implementation phase to record — the recipe wrote no task record of its own.
6. No test in the change was written after the code it covers — a test that cannot name a behaviour is measuring or ratifying, and does not count toward item 1. This phase wrote none of them.
8. Where the project has Playwright/ATK e2e or visual-regression coverage, it is reported separately and is not counted toward the test-first requirement in item 1.
9. Every pre-existing test the change modified or deleted was changed by a role the mutability matrix permits — the only rows that may delete are a feature removal taking its own tests in the same commit; RED authoring is the only row that writes an assertion, and GREEN, REFACTOR and a bug fix change none. A reviewer that wanted a test changed filed a finding instead. See `development/tdd-spec-driven`.

This recipe ships no executable verifier of its own — the checks above are the agent-driven protocol; the linter execution is the code-quality-tools plugin's, and the plugin's implementation phase owns the test-first completion gate.
## Oracle files

A measurement oracle is a file the gates read to decide pass or fail — a static-analysis baseline, a test, a coverage config. An autonomous builder must never weaken one to make a red gate go green: only adding tests or fixing code is allowed, never suppressing a finding. The plugin's deterministic oracle-tamper guard enforces this at the review/critique rung, but the guard itself is framework-agnostic — it carries no Drupal knowledge and monitors only the file list it is handed. This section is that list for Drupal: the caller reconstructs it from here on every run (so there is no persistent project file a builder could empty to switch monitoring off) and hands it to the guard.

Each rule names the change kinds it watches (A added, M modified, D deleted), the oracle class the change touches, and a severity. A **halt** is terminal tamper unless the work-order's `oracle_update` field explicitly exempts that class; a **flag** is recorded and the work ships flagged, never blocked.

The class names match the work-order `oracle_update` exemption vocabulary, so a human-authored exemption lines up with what the guard sees.

| Oracle file | Watches | Class | Severity | Why |
|---|---|---|---|---|
| `phpstan-baseline.neon` | add / modify | phpstan-baseline | halt | The phpstan baseline suppresses known findings — adding to it hides a *new* static-analysis error instead of fixing it. |
| `phpstan.neon` / `phpstan.neon.dist` | modify | phpstan-baseline | flag | The phpstan config sets the rule level and paths — a change can quietly lower the bar; recorded for review. |
| `phpunit.xml` / `phpunit.xml.dist` | modify | coverage-threshold | flag | The PHPUnit config carries coverage thresholds and the suite definition — a change can relax the coverage gate; recorded for review. |
| PHPUnit test files (`*Test.php` under the test tree) | delete | test-delete | halt | Deleting a test removes the behaviour it guards — the builder must add tests, never drop them, to pass. |

The caller emits this list as the oracle-tamper guard's JSON input. The two columns the guard needs beyond the table are the path globs and the watched-change set:

```json
[
  { "type": "phpstan_baseline",  "globs": ["phpstan-baseline.neon"],            "changes": ["A","M"], "oracle_class": "phpstan-baseline",   "severity": "halt" },
  { "type": "phpstan_config",    "globs": ["phpstan.neon", "phpstan.neon.dist"],"changes": ["M"],     "oracle_class": "phpstan-baseline",   "severity": "flag" },
  { "type": "coverage_threshold","globs": ["phpunit.xml", "phpunit.xml.dist"],  "changes": ["M"],     "oracle_class": "coverage-threshold", "severity": "flag" },
  { "type": "test_delete",       "globs": ["**/tests/**/*Test.php"],             "changes": ["D"],     "oracle_class": "test-delete",        "severity": "halt" }
]
```

The test glob **must** carry the `**/` prefix. The guard anchors a glob at both ends and expands
`**/` to an optional path prefix, so `tests/**/*Test.php` matches a test tree at the repository root
and nothing else. A Drupal custom module keeps its tests at
`web/modules/custom/<module>/tests/src/<Tier>/<Name>Test.php`, which that pattern does not match — on
its own it would leave the delete guard watching nothing on a real project. `**/tests/**/*Test.php`
covers the nested layout *and* the root one, since the prefix is optional, so it is the only glob
needed. Do not drop the prefix.

These are the standards-and-tests oracle files. A Drupal project that also set up visual-regression or E2E testing has further oracle files — the VR snapshot baselines and the E2E spec files — declared by those setup recipes; the caller unions the declarations across every recipe that applies to the project before handing the combined list to the guard. A project that declares no oracle files at all is an honest "no oracle configured" state: the guard reports it ran with nothing to watch, rather than reporting a pass it never checked.

## References

### Drupal guides (referenced, not authored here)

| Source | Used for |
|---|---|
| `drupal/tdd` | The Red-Green-Refactor cycle and test-first discipline this recipe enforces |
| `drupal/testing` | The Unit / Kernel / Functional base classes and PHPUnit mechanics behind the tier choice |
| `drupal/security` | Form API tokens, output escaping, query parameterization, and access checks — the implementation-time security rules |
| `drupal/best-practices/camoa` | The house Drupal coding conventions the refactor step aligns to |

### Sibling process recipes

| Recipe | What it holds |
|---|---|
| `drupal/test-authoring.md` | Which tier a behaviour belongs at, where the test file goes and what it is called, how a criterion is traced to a test, and what a Drupal test may not do — the half of the cycle that ends at red |
| `drupal/test-execution.md` | The command at each scope, its cost, the conditions for running one, and how to read what came back |

### Plugin-side tooling (referenced, not authored here)

| Source | Used for |
|---|---|
| code-quality-tools (plugin) | Execution of `phpcs --standard=Drupal,DrupalPractice` and `phpstan` over the changed files — the linter run this recipe defers to rather than re-authoring |

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| PHPUnit / DDEV (`ddev phpunit`) | The test runner the Unit / Kernel / Functional tiers execute against |

### Plugin-side generic mechanism (ai-dev-assistant)

The stack-neutral implementation phase this recipe binds Drupal into — when implementation runs, the test-first gate that blocks completion, and how the results are recorded against the task — is documented in the plugin itself, not duplicated here. The recipe supplies only the Drupal-specific method it owns on top of that mechanism: coding-standard application and the implementation-time security rules, applied to code written against a test that arrived red.
