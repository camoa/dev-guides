---
# Routing block — an orchestrator reads to here and decides.
name: php_cli_implement_standards_and_tests
capability: implement
description: Use when a PHP CLI project (a Composer library or application whose interface is one or more CLI binaries) enters the implementation phase holding a test that already fails, and must turn it green under PHP/PSR standards — applies PSR-12 with declare(strict_types=1) and readonly value objects, confirms every CLI flag and exit code the change touches is covered, and syntax-checks every shipped binary including extensionless ones. Which level the test sits at and how it is written belong to the test-authoring recipe; linter execution is deferred to the code-quality-tools plugin.
# Metadata — read only after a match.
label: PHP CLI standards and tests
recipe_schema_version: 1.0.0
version: 0.6.0
# Machine-readable dependency declaration (recipe-loader resolves these
# without parsing prose). The test-mutability rule is stack-neutral: it is
# cited here, never restated per framework.
requires_guides:
  - development/tdd-spec-driven
# Process-recipe routing keys, enforced by validate_recipes.py for any recipe
# under docs/process-recipes/. `capability` above doubles as the phase (the
# lifecycle moment the orchestrator resolves on); there is no separate
# applies_to_phase. `framework` is the second routing dimension.
recipe_class: process
framework: php-cli
assumes:
  - composer
  - phpunit
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Hold PHP CLI implementation-phase code to the standard it must meet before it can be reviewed: PHP/PSR coding standards applied as the code is written, a test that arrived red turned green without weakening it, and the coverage the contract requires confirmed present — every CLI flag and exit code exercised, and a check-style unit carrying its negative case. The judgement of *which* standard applies is the recipe's; running the linters is the code-quality-tools plugin's; choosing and writing the test is `php-cli/test-authoring.md`'s.

The plugin owns the generic mechanism — when the implement phase runs, the test-first gate that blocks completion, the oracle-tamper guard that stops a builder weakening a measurement file, and how findings are recorded against the task. This recipe owns the part the stack-neutral mechanism cannot know: how PHP coding standards are applied to a CLI library, why a CLI's end-to-end coverage is a test level rather than a phase, and the extensionless-binary trap a naive syntax-check glob walks straight into.

## Opinion

**The test is written first, and it is seen to fail.** No production code is written until a test for the behaviour exists and has been run to confirm it fails (RED) for the right reason — the behaviour is absent. Not a typo in the test, and not working code you broke or reverted to produce the failure; that proves the test is sensitive, never that it came first (see `development/tdd-spec-driven/what-a-failing-test-proves`). Then the minimum code to pass (GREEN), then refactoring under a green bar (REFACTOR). A test that passes on its first run is suspect: it is probably asserting nothing. "Too simple to test" is not a reason to skip; a CLI flag or an exit code is exactly the kind of one-liner that silently regresses.

**PSR-12, strict types everywhere, readonly value objects across seams.** Every file carries `declare(strict_types=1)` and conforms to PSR-12 layout, PascalCase classes / camelCase methods, docblocks on classes and public methods, and type hints on every parameter and return. Data carried between layers — from the thin binary into the library, from one collaborator to the next — travels as a `readonly` value object, not a loose array, so the shape is explicit and cannot be mutated behind a caller's back. No deprecated APIs reach the diff.

**The level, the file and the test's name are not decided here.** Which level a behaviour belongs at, where the test file goes, what the class and method are called, how the criterion it specifies is traced to it, and what a PHPUnit test may not do are `php-cli/test-authoring.md`'s. That reader writes the test and stops at red; this one takes the red test and makes it green. The rules are stated once, there, because a reader that may not write production code cannot be handed this file.

**Every CLI flag and exit code needs a test, and a check-style unit needs a negative case.** Each flag the binary accepts and each exit code it can return is a behaviour with a contract, and each gets a test that pins it — a flag that changes output, a bad-input path that returns the documented non-zero code. A **check-style** unit — one whose job is to *report problems* (a linter rule, a scanner, a validator) — additionally needs a **negative case**: an assertion that correct input produces **no** output and no finding. Without the negative case the check cannot be tuned — a rule that flags everything and a rule that flags nothing both pass a suite that only ever feeds them bad input.

**Fixture-driven end-to-end IS the CLI's e2e, and it is not a phase.** "No e2e" for a PHP CLI means no *browser* e2e — it does not mean the tool has no end-to-end shape. The plugin's e2e-setup machinery is Playwright-shaped and does not fit a tool with no rendered surface, so that coverage never becomes an `e2e-setup` binding: it is a test level, chosen in `php-cli/test-authoring.md` and checked at `review` like any other.

**That fixture tier is inside the TDD loop; a browser suite would not be.** The distinction is not whether a subprocess or a browser is involved, it is whether the test was written before the code and run red. The fixture-driven CLI test is written from the flag-and-exit-code contract before the flag exists, so it constrains the design. Visual regression and browser E2E, where a project has them, run against something already built, cannot drive a design decision, and do not count toward the test-first requirement here.

**Adding a test is not automatically progress.** The loop's requirement for a change is one specification per behaviour the change creates, at the level `php-cli/test-authoring.md` chose, each seen to fail first *because the behaviour it names did not exist yet*. Past that, more tests make the change harder to review without specifying anything new. The full set of excess cases belongs to `development/tdd-spec-driven` and is cited, not restated, and the PHP-CLI-specific forms are stated in `php-cli/test-authoring.md` beside the reader that would write them. What belongs here is what a prose-only surface means for the **code**: where a behaviour a user depends on can only be observed by reading the tool's own wording, give it an exit code or a machine-readable mode. That is a change to the tool, made in this phase.

**Syntax-check and lint every shipped binary, including the extensionless ones.** A Composer CLI's binaries are conventionally extensionless — `bin/<tool>`, not a `.php` file — so a naive `find -name '*.php'` syntax-check glob silently skips the very entrypoints a user runs. Enumerate the binaries to check from the `bin` array in composer.json instead of globbing by extension, and syntax-check (and hand to the linters) every one of them, extensionless included. A binary that never gets linted is the file most likely to ship a fatal parse error.

**Standards are applied by judgement; the linters are run by the tooling.** This recipe decides what PSR-12, strict types, and the house conventions mean for the code in front of it. The *execution* of `phpcs` and `phpstan` over the changed files is the code-quality-tools plugin's job; this recipe references that plugin for the run and does not re-author or replace the linter invocation. Standards live in judgement here; their mechanical enforcement lives in the tooling.

## Preconditions

- A PHP project, Composer-managed. The condition for *running* a test — a configured PHPUnit runner against a committed `phpunit.xml` or `phpunit.xml.dist` — is declared by the `test-execution` recipe for this framework, which is where the commands that need it live.
- The design phase has produced an architecture decision (see the architecture recipe under this framework): the library boundary, the thin-binary contract, the exit-code semantics, and the component map are known, so this phase tests and builds against a plan rather than improvising structure.
- The code-quality-tools plugin is available for linter execution (`phpcs`, `phpstan` at the project's declared level); this recipe does not bundle or re-author those runners.
- The plugin's generic implement phase is present: the test-first gate, the oracle-tamper guard, and the task record. This recipe supplies the PHP-CLI-specific standards-and-tests method; it does not recreate the gate.

All four stay prose. They are design-artifact and plugin-availability conditions with no argv-safe filesystem probe, and the one condition that did carry a machine-readable entry — the PHPUnit runner — moved to the `test-execution` recipe, which owns the commands it is a condition of.

```yaml
preconditions: []
```

## Input contract

Source-agnostic, supplied by the caller (the orchestrator at the implement phase, or a human operator).

```yaml
code_path: string             # absolute path to the PHP project root
component: string             # the unit being implemented (a service, a command, a rule…)
behavior: string             # the specific behaviour to test-drive and build
test_tier: string             # the level the test-authoring recipe chose, carried through
architecture_ref: string      # optional; pointer to the design decision this implements
```

## Sequence

If invoked in dry-run mode, perform all reads and emit a standards plan (what the code must do to turn the test green, the flag and exit-code coverage to confirm, the binaries to syntax-check) instead of writing production code. Dry-run is required.

1. **Take the failing test.** The level, the file, the class and method names and the criterion each carries are `php-cli/test-authoring.md`'s, and it hands them over red. Confirm the failure is an assertion that ran and did not hold rather than a harness error or a run that selected nothing — `php-cli/test-execution.md` declares how to tell those apart. A behaviour arriving with no failing test does not enter this phase; send it back.

2. **Confirm the red is the right red, and that the coverage the contract needs arrived with it.** The behaviour is absent — not a failure produced by breaking or reverting working code, which proves the test is sensitive and never that it came first (see `development/tdd-spec-driven/what-a-failing-test-proves`). Confirm the set covers every CLI flag and exit code the component touches, and that a check-style unit brought its **negative case** — correct input yields no output and no finding. A gap in that coverage goes back to test authoring; it is not filled here. A test that passed on arrival is not a starting point; return it. Once a test is committed, who may change or delete it is the mutability matrix's answer in `development/tdd-spec-driven`, not this phase's — and this phase changes none.

3. **Write the minimum code to pass (GREEN).** Implement only what the tests demand — no extra features, no premature optimisation. As you write, hold the standards inline: `declare(strict_types=1)` at the top of every file, PSR-12 layout, docblocks and type hints, PascalCase classes / camelCase methods, and `readonly` value objects for data crossing the binary/library seam or passed between collaborators rather than loose arrays. Keep the binary thin — arg parsing and wiring only, logic in the library (the boundary the architecture recipe fixed). Run the tests to green.

4. **Apply and confirm the standards inline.** Before the unit is considered done, confirm no deprecated APIs entered the diff, every new file declares strict types, and the layer boundary held (no business logic leaked into `bin/`). Any gap is fixed now. Where the fix needs a test to prove it, that test is authored by `php-cli/test-authoring.md` and arrives red like any other; this phase does not write it.

5. **Syntax-check every shipped binary, extensionless included.** Enumerate the binaries from the `bin` array in composer.json — not from a `*.php` glob, which skips the extensionless ones — and syntax-check every entry (`php -l` per binary). An extensionless `bin/<tool>` is checked exactly like a `.php` file. A binary that fails the syntax check is fixed before the phase hands back.

6. **Refactor under green (REFACTOR).** With tests green, improve structure without changing behaviour — extract duplication into the library, lean on interfaces at the extension seams the design named, tighten the value objects. Re-run the tests; they stay green or the refactor is reverted.

7. **Defer the linters to the tooling, then hand back.** Invoke the code-quality-tools plugin to run `phpcs` and `phpstan` over the changed files, binaries included — this recipe judges what the standards mean but does not re-author or replace that run. Return the test results, the flag and exit-code coverage confirmation, the binary syntax-check outcome, and the linter outcome to the caller; the plugin's implement phase records them against the task and owns the completion gate. The recipe writes production code for the component, changes no test, and writes no task record of its own.

## Data flow

```
input: code_path, component, behavior, test_tier (optional), architecture_ref (optional)

reads project state:
       architecture decision (the library boundary + thin-binary + exit-code contract)
       composer.json (the bin array — the authoritative list of shipped binaries)
       existing library + entrypoints (src/, bin/) and existing tests (tests/)

applies opinion:
       test-first (RED→GREEN→REFACTOR) · PSR-12 + declare(strict_types=1) + readonly
       value objects · the test arrives red and is not rewritten · every flag + exit code
       tested · check-style unit needs a negative case · fixture-driven CLI e2e lives
       here · syntax-check every binary incl. extensionless · standards by judgement,
       linters by tooling

references origin (never duplicated):
       PHPUnit                     — the test runner every tier executes against
       code-quality-tools (plugin) — phpcs + phpstan execution over the changed files
       the architecture recipe     — the library boundary, thin-binary, exit-code contract

emits (to the caller; the recipe writes no task record):
       tests:        the test(s) per component at the chosen tier, seen to fail on an
                     absent behaviour then pass,
                     incl. flag/exit-code contract tests + fixture-based CLI e2e
       code:         the minimum production code that turns them green, standards held inline
       binaries:     the per-binary syntax-check outcome (extensionless included)
       linting:      the code-quality-tools run outcome over the changed files
```

## State-awareness contract

The recipe reads existing state before writing. The architecture decision, the current library layout (`src/`, `bin/`), the `bin` array in composer.json, and any existing tests under `tests/` are read so new code extends the design and the binary list is enumerated from source of truth rather than guessed. The method writes production code for the component under implementation, changes no test, installs nothing and writes no task record — the results are returned to the caller, which owns recording them and gating completion.

Idempotent at the discipline level: re-running on a component whose tests already pass, whose standards already hold, and whose binaries already syntax-check produces no new change — the tests stay green, the linters stay clean, nothing is rewritten. A change on re-run means a regression was found or the behaviour moved, which is the method reflecting current reality, not non-determinism.

## Verifier

After the recipe runs, verify:

1. Every implemented behaviour arrived with a PHPUnit test that had been seen to fail *because the behaviour was absent* — not because working code was broken or reverted, and no test passed on arrival unexamined. The level that test sits at is `php-cli/test-authoring.md`'s choice, verified there.
2. Every check-style unit carries a negative case — an assertion that correct input produces no output and no finding — so the check can be tuned, not just fired.
3. Every CLI flag and every exit code the component touches is covered, and fixture-based CLI end-to-end coverage exists that drives the built binary against a fixture tree and asserts on stdout / stderr / exit code.
4. No test in the change was written after the code it covers — a test that cannot name a behaviour is measuring or ratifying, and does not count toward item 1. This phase wrote none of them.
6. Every shipped binary — enumerated from the `bin` array in composer.json, extensionless entries included — was syntax-checked and passes; none was skipped by an extension-only glob.
7. New code carries `declare(strict_types=1)` in every file, PSR-12 layout, docblocks and type hints, `readonly` value objects across the seams, no deprecated APIs, and no business logic in `bin/`.
8. The code-quality-tools `phpcs` and `phpstan` run over the changed files (binaries included) is clean, or its findings are recorded for the gate; this recipe did not re-author that run.
9. The tests are green and the refactor (if any) left them green; the results were returned to the caller for the plugin's implement phase to record — the recipe wrote no task record of its own.
10. Every pre-existing test the change modified or deleted was changed by a role the mutability matrix permits — the only rows that may delete are a feature removal taking its own tests in the same commit; RED authoring is the only row that writes an assertion, and GREEN, REFACTOR and a bug fix change none. A reviewer that wanted a test changed filed a finding instead. See `development/tdd-spec-driven`.

This recipe ships no executable verifier of its own — the checks above are the agent-driven protocol; the linter execution is the code-quality-tools plugin's, and the plugin's implement phase owns the test-first completion gate.
## Oracle files

A measurement oracle is a file the gates read to decide pass or fail — a static-analysis baseline, a test, a coverage config. An autonomous builder must never weaken one to make a red gate go green: only adding tests or fixing code is allowed, never suppressing a finding. The plugin's deterministic oracle-tamper guard enforces this at the review/critique rung, but the guard itself is framework-agnostic — it carries no PHP knowledge and monitors only the file list it is handed. This section is that list for a PHP CLI project: the caller reconstructs it from here on every run (so there is no persistent project file a builder could empty to switch monitoring off) and hands it to the guard.

Each rule names the change kinds it watches (A added, M modified, D deleted), the oracle class the change touches, and a severity. A **halt** is terminal tamper unless the work-order's `oracle_update` field explicitly exempts that class; a **flag** is recorded and the work ships flagged, never blocked.

The class names match the work-order `oracle_update` exemption vocabulary, so a human-authored exemption lines up with what the guard sees.

| Oracle file | Watches | Class | Severity | Why |
|---|---|---|---|---|
| `phpstan-baseline.neon` | add / modify | phpstan-baseline | halt | The phpstan baseline suppresses known findings — adding to it hides a *new* static-analysis error instead of fixing it. |
| `phpstan.neon` / `phpstan.neon.dist` | modify | phpstan-baseline | flag | The phpstan config sets the rule level and paths — a change can quietly lower the bar; recorded for review. |
| `phpunit.xml` / `phpunit.xml.dist` | modify | coverage-threshold | flag | The PHPUnit config carries coverage thresholds and the suite definition — a change can relax the coverage gate; recorded for review. |
| PHPUnit test files (`*Test.php` under a `tests/` or `test/` tree, at any depth) | delete | test-delete | halt | Deleting a test removes the behaviour it guards — the builder must add tests, never drop them, to pass. |

The caller emits this list as the oracle-tamper guard's JSON input. The two columns the guard needs beyond the table are the path globs and the watched-change set:

```json
[
  { "type": "phpstan_baseline",  "globs": ["phpstan-baseline.neon"],            "changes": ["A","M"], "oracle_class": "phpstan-baseline",   "severity": "halt" },
  { "type": "phpstan_config",    "globs": ["phpstan.neon", "phpstan.neon.dist"],"changes": ["M"],     "oracle_class": "phpstan-baseline",   "severity": "flag" },
  { "type": "coverage_threshold","globs": ["phpunit.xml", "phpunit.xml.dist"],  "changes": ["M"],     "oracle_class": "coverage-threshold", "severity": "flag" },
  { "type": "test_delete",       "globs": ["**/tests/**/*Test.php", "**/test/**/*Test.php"], "changes": ["D"], "oracle_class": "test-delete",   "severity": "halt" }
]
```

Two things about the test glob are deliberate, and both were established by running the guard's own
glob translation rather than by reading it.

**The `**/` prefix is required.** The guard anchors a glob at both ends and expands `**/` to an
*optional* path prefix, so `tests/**/*Test.php` matches a test tree at the repository root and
nothing else — any package whose tests sit below the root, such as a nested or multi-package layout,
fails it. `**/tests/**/*Test.php` covers both the nested layout and the root one, which is why it is
the only `tests/` glob needed here.

**`test/` singular is a real convention, not a typo.** Across 139 Composer packages declaring a
dev-autoload test path, 60 use `tests/` and 13 use `test/`. A PHP CLI project is as likely to be one
of the latter, and a delete guard that watches only `tests/` silently watches nothing on it — the
same failure mode as a missing prefix, which is why both are declared.

These are the standards-and-tests oracle files — the same set a standalone PHP CLI project carries as a Drupal one, since the measurement surface (the phpstan baseline, the phpstan config, the PHPUnit config, and the test files) is identical. A `php-cli` project binds no visual-regression or e2e-setup phase, so it declares no further oracle files from those recipes; the caller still unions declarations across every recipe that applies before handing the combined list to the guard. A project that declares no oracle files at all is an honest "no oracle configured" state: the guard reports it ran with nothing to watch, rather than reporting a pass it never checked.

## References

### Sibling process recipes

| Recipe | What it holds |
|---|---|
| `php-cli/test-authoring.md` | Which level a behaviour belongs at, where the file goes and what the class and method are called, how a criterion is traced to a test, and what a PHPUnit test may not do — the half of the cycle that ends at red |
| `php-cli/test-execution.md` | The command at each scope, its cost, the condition for running one, and how to read what came back |

### Plugin-side tooling (referenced, not authored here)

| Source | Used for |
|---|---|
| code-quality-tools (plugin) | Execution of `phpcs` and `phpstan` over the changed files, binaries included — the linter run this recipe defers to rather than re-authoring |

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| PHPUnit (`php vendor/bin/phpunit`) | The test runner every tier — plain unit, unit-with-collaborators, integration, and the fixture-driven CLI end-to-end — executes against |
| Composer (composer.json `bin` array) | The authoritative list of shipped binaries the syntax-check enumerates, so extensionless entrypoints are not skipped by an extension-only glob |

### Plugin-side generic mechanism (ai-dev-assistant)

The stack-neutral implement phase this recipe binds PHP CLI into — when implementation runs, the test-first gate that blocks completion, the oracle-tamper guard that reads the list above, and how the results are recorded against the task — is documented in the plugin itself, not duplicated here. The recipe supplies only the PHP-CLI-specific method it owns on top of that mechanism: PSR-12 with strict types and readonly value objects, the flag-and-exit-code coverage confirmation, and the extensionless-binary syntax check.
