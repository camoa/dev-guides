---
# Routing block — an orchestrator reads to here and decides.
name: drupal_implement_standards_and_tests
capability: implement
description: Use when a Drupal project enters the implementation phase and must hold code to Drupal/PHP coding standards, the implementation-time security rules, and test-first discipline — applies the no-static-service rule and Form-API / Twig / parameterized-query guarantees, selects the right PHPUnit test tier per unit of logic, and shapes each test Red-Green-Refactor before any production code is written. Defers linter execution to the code-quality-tools plugin.
# Metadata — read only after a match.
label: Coding standards and test discipline (Drupal)
recipe_schema_version: 1.0.0
version: 0.4.0
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

Hold Drupal implementation-phase code to the standard it must meet before it can be reviewed: Drupal/PHP coding standards applied as the code is written, the implementation-time security rules guaranteed (Form API tokens, Twig auto-escaping, parameterized queries, no static service access in new code), and every unit of logic covered by a PHPUnit test written test-first at the right tier. The judgement of *which* standard applies and *which* test tier fits is the recipe's; running the linters is the code-quality-tools plugin's.

The plugin owns the generic mechanism — when the implementation phase runs, the test-first gate that blocks completion, and how findings are recorded against the task. This recipe owns the part the stack-neutral mechanism cannot know: how Drupal coding standards are actually applied, what the Drupal security rules are at implementation time, and how the PHPUnit test tiers are selected and shaped.

## Opinion

**The test is written first, and it is seen to fail.** No production code is written until a test for the behaviour exists and has been run to confirm it fails (RED) for the right reason — a missing implementation, not a typo in the test. Then the minimum code to pass (GREEN), then refactoring under a green bar (REFACTOR). A test that passes on its first run is suspect: it is probably asserting nothing. "Too simple to test" is not a reason to skip; simple now is complex later.

**No static `\Drupal::` in new code.** New code names every collaborator it needs by constructor injection — `\Drupal::service(...)`, `\Drupal::entityTypeManager()`, and friends are a hidden, untestable dependency and are blocking in the service layer. Static `\Drupal::` is tolerated only in procedural `.module` glue and in code Drupal does not let you inject into, never in a class this phase writes. This is the implementation-time twin of the architecture phase's service rule, and it is what makes the code unit-testable in the first place.

**Security is a property of the code, not a later audit.** Four guarantees hold at implementation time: Form API builds and validates every data-entry form so its CSRF token is present and checked; output is escaped — Twig auto-escaping is left on and never defeated with `|raw` or an unsanitised render-array `#markup`; database access is parameterized through the query builder or placeholders, never string-concatenated user input; and access checks are present on every route and operation. A security issue found here is fixed here, not deferred.

**The test tier matches the dependency surface, not habit.** Pure logic with no Drupal bootstrap is a Unit test; logic that needs the container, entities, or the database is a Kernel test; behaviour that needs a full request and a rendered page is a Functional test (`BrowserTestBase` — runs no JavaScript); behaviour that needs JavaScript executed in the browser (Ajax forms, JS-driven UI) is a FunctionalJavascript test (`WebDriverTestBase`/`FunctionalJavascriptTestBase`). Pushing a Kernel concern into a slow Functional test, faking a container in a Unit test that really needs one, or testing an Ajax behaviour in a non-JS Functional test that silently cannot exercise it, are all tier mismatches — name the tier deliberately.

**All four PHPUnit tiers are the TDD loop; Playwright and visual regression are not.** Each tier above is written before the code and run red then green — FunctionalJavascript included, which drives a real browser and is still inside the loop. The Playwright/ATK suite the `e2e-setup` recipe configures and the snapshot baselines the `visual-regression` recipe configures are outer verification: they run against a site that already stands, they cannot drive a design decision, and they are written after the behaviour exists. Their coverage neither substitutes for a tier chosen here nor counts toward the test-first requirement. "The e2e suite covers it" is not an answer to "which tier specifies this behaviour".

**Adding a test is not automatically progress.** The loop's requirement for a change is one specification per behaviour the change creates, at the smallest tier that answers the question, each seen to fail first — and past that, more tests make the change harder to review without specifying anything new. The full set of cases (a test written after the code, a duplicate one tier up, an assertion on an unpromised surface) belongs to `development/tdd-spec-driven` and is cited, not restated. What is Drupal-specific is the local form the last case takes: a Functional test asserting on rendered markup that no template or API contract pins is the common one here, and the repair is a Kernel test against the service that produced the value, not a stricter string match.

**Standards are applied by judgement; linters are run by the tooling.** This recipe decides what Drupal coding standards mean for the code in front of it — PSR-12/Drupal layout, docblocks on classes and public methods, type hints, no deprecated APIs, PascalCase classes / camelCase methods. The *execution* of `phpcs --standard=Drupal,DrupalPractice` and `phpstan` is the code-quality-tools plugin's job; this recipe references that plugin for the run and does not re-author the linter invocation.

**Mechanics are referenced, not re-authored.** *How* a PHPUnit test base is extended, how a Kernel test installs its schema, how Twig escaping or the Form API token actually work, and what the house conventions are belong to the knowledge guides. This recipe references `drupal/tdd`, `drupal/testing`, `drupal/security`, and `drupal/best-practices/camoa` for those mechanics and stays focused on the discipline applied on top of them.

**The recipe enforces and writes code under discipline; it does not own the gate.** Recording pass/fail against the task and blocking task completion is the plugin's implementation phase. This recipe supplies the Drupal method the gate evaluates.

## Preconditions

- A Drupal 10.3+ or 11.x project, Composer-managed, with a DDEV environment and a configured PHPUnit runner — a `ddev phpunit` custom command (or `ddev exec vendor/bin/phpunit`) with `SIMPLETEST_DB` set, plus `SIMPLETEST_BASE_URL` and `BROWSERTEST_OUTPUT_DIRECTORY` for the Functional/FunctionalJavascript tiers (see `drupal/testing` for the runner config) — so the tests and the code-quality-tools linters can run.
- The design phase has produced an architecture decision (see the `architecture` recipe) — the services, Drush commands, forms, and storage to implement are known, so this phase tests and builds against a plan rather than improvising structure.
- The code-quality-tools plugin is available for linter execution (`phpcs --standard=Drupal,DrupalPractice`, `phpstan`); this recipe does not bundle or re-author those runners.
- The plugin's generic implementation phase is present: the test-first gate and the task record. This recipe supplies the Drupal-specific standards-and-tests method; it does not recreate the gate.

The first bullet is the one the engine can check, so it is also declared in machine-readable form below. The rest stay prose: they are design-artifact and plugin-availability conditions with no argv-safe filesystem probe.

preconditions:
  - id: test-runner
    what: a PHPUnit runner whose failure the RED step can observe
    check: test -x vendor/bin/phpunit
    owner: code-quality-tools:setup

## Input contract

Source-agnostic, supplied by the caller (the orchestrator at the implementation phase, or a human operator).

```yaml
code_path: string             # absolute path to the Drupal project root
component: string             # the unit being implemented (a service, form, Drush command…)
behavior: string             # the specific behaviour to test-drive and build
test_tier: string             # optional; unit | kernel | functional | functional-javascript —
                              #   if absent, derived from the dependency surface
architecture_ref: string      # optional; pointer to the design decision this implements
```

## Sequence

If invoked in dry-run mode, perform all reads and emit a test-and-standards plan (the tier choice, the test shape, the standards/security checklist) instead of writing any test or production code. Dry-run is required.

1. **Select the test tier.** From `behavior` and the component's dependency surface, choose the tier: **Unit** (`tests/src/Unit/`) for pure logic with no Drupal bootstrap; **Kernel** (`tests/src/Kernel/`) for services, entities, or database access against a minimal container; **Functional** (`tests/src/Functional/`) for full page requests and rendered output with no JavaScript; **FunctionalJavascript** (`tests/src/FunctionalJavascript/`) for behaviour that needs JavaScript executed in the browser (Ajax, JS-driven UI). Use `test_tier` if supplied; otherwise derive it. The mechanics of each base class are referenced to `drupal/testing`, not restated here.

2. **Write the failing test (RED).** Author the test before any production code, shaped Arrange-Act-Assert against the `Drupal\Tests\{module}\{Type}` namespace. Run it (`ddev phpunit --testsuite {tier}` or the test path — `--testsuite`, not `--filter`, since `--filter` matches the test identifier regex and would catch the wrong tier) and confirm it fails for the right reason — a missing implementation, not a broken test. A test that passes immediately is rejected and rewritten. TDD-cycle detail is referenced to `drupal/tdd`. Rewriting *this* test is the author's own move, made before the production code exists; once a test is committed, who may change or delete it is the mutability matrix's answer in `development/tdd-spec-driven`, not this phase's.

3. **Write the minimum code to pass (GREEN).** Implement only what the test demands — no extra features, no premature optimisation, no "while I'm here" additions. As you write, hold the standards inline: constructor-inject every dependency (no static `\Drupal::` in the new class), docblocks on the class and public methods, type hints on parameters and returns, no deprecated APIs, Drupal layout and naming. Run the test to green.

4. **Apply the implementation security rules.** Before the unit is considered done, confirm the four guarantees against `drupal/security`: Form API builds/validates every data-entry form (CSRF token present and checked); output is escaped (Twig auto-escaping intact, no unsanitised `|raw` or `#markup`); all database access is parameterized (query builder / placeholders, never concatenated user input); and access checks cover every route and operation. Any gap is fixed now, with a test that proves the fix where the behaviour is testable.

5. **Refactor under green (REFACTOR).** With tests green, improve structure without changing behaviour — extract duplication into a service or trait, lean on Drupal base classes, align with the house conventions in `drupal/best-practices/camoa`. Re-run the tests; they stay green or the refactor is reverted.

6. **Defer the linters to the tooling, then hand back.** Invoke the code-quality-tools plugin to run `phpcs --standard=Drupal,DrupalPractice` and `phpstan` over the changed files — this recipe judges what the standards mean but does not re-author or replace that run. Return the test results, the tier choices, the security-rule confirmation, and the linter outcome to the caller; the plugin's implementation phase records them against the task and owns the completion gate. The recipe writes test and production code for the component, but writes no task record of its own.

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
       tests:        the test(s) per component, at the chosen tier, seen to fail then pass
       code:         the minimum production code that turns them green
       security:     confirmation of the four implementation-time guarantees
       linting:      the code-quality-tools run outcome over the changed files
```

## State-awareness contract

The recipe reads existing state before writing. The architecture decision, the current module layout (`src/`, `*.services.yml`, `*.routing.yml`), and any existing tests for the component are read so new code extends the design and new tests extend the suite rather than colliding with or duplicating them. The method writes test and production code for the component under implementation, but installs nothing and writes no task record — the results are returned to the caller, which owns recording them and gating completion.

Idempotent at the discipline level: re-running on a component whose tests already pass and whose standards and security rules already hold produces no new change — the tests stay green, the linters stay clean, nothing is rewritten. A change on re-run means a regression was found or the behaviour moved, which is the method reflecting current reality, not non-determinism.

## Verifier

After the recipe runs, verify:

1. Every implemented behaviour has a PHPUnit test at a deliberately chosen tier (Unit / Kernel / Functional / FunctionalJavascript), and each test was seen to fail before the code existed — no test passed on its first run unexamined.
2. No new class reaches for a static `\Drupal::` service; every dependency is constructor-injected.
3. The four security guarantees hold: Form API on every data-entry form (token present and checked), Twig auto-escaping intact (no unsanitised `|raw`/`#markup`), all database access parameterized, access checks on every route and operation.
4. New code carries docblocks on classes and public methods, type hints on parameters and returns, no deprecated APIs, and Drupal layout/naming — and the code-quality-tools `phpcs --standard=Drupal,DrupalPractice` and `phpstan` run over the changed files is clean (or its findings are recorded for the gate).
5. The tests are green and the refactor (if any) left them green; the results were returned to the caller for the plugin's implementation phase to record — the recipe wrote no task record of its own.
6. Each test names the behaviour it specifies, and no test in the change was written after the code it covers — a test that cannot name a behaviour is measuring or ratifying, and does not count toward item 1.
7. No test asserts on rendered markup, a log line, or a message string that no template or API contract pins; assertions land on returned values, entity or state changes, response codes, or thrown exception types.
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

### Plugin-side tooling (referenced, not authored here)

| Source | Used for |
|---|---|
| code-quality-tools (plugin) | Execution of `phpcs --standard=Drupal,DrupalPractice` and `phpstan` over the changed files — the linter run this recipe defers to rather than re-authoring |

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| PHPUnit / DDEV (`ddev phpunit`) | The test runner the Unit / Kernel / Functional tiers execute against |

### Plugin-side generic mechanism (ai-dev-assistant)

The stack-neutral implementation phase this recipe binds Drupal into — when implementation runs, the test-first gate that blocks completion, and how the results are recorded against the task — is documented in the plugin itself, not duplicated here. The recipe supplies only the Drupal-specific standards-and-tests method (coding-standard application, the implementation-time security rules, and PHPUnit tier selection with the test-first shape) on top of that mechanism.
