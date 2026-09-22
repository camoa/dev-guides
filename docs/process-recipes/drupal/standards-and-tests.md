---
# Routing block — an orchestrator reads to here and decides.
name: drupal_implement_standards_and_tests
capability: implement
description: Use when a Drupal project enters the implementation phase holding a test that already fails, and must turn it green under Drupal/PHP coding standards and the implementation-time security rules — applies the no-static-service rule and the Form-API / Twig / parameterized-query guarantees, then refactors under a green bar. Which tier the test sits at and how it is written belong to the test-authoring recipe; linter execution is deferred to the code-quality-tools plugin.
# Metadata — read only after a match.
label: Coding standards and test discipline (Drupal)
recipe_schema_version: 1.0.0
version: 0.9.0
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
- For a configuration unit only: the worktree site the `worktree-environment` recipe brings up, with the two named snapshots its bring-up leaves in the worktree (that recipe at 0.4.0 or later) and the `project:` token it recorded. The `## Configuration gate` restores the seed by name and imports into that site; without them the gate has nothing to prove against and its first lines say so.

All five stay prose. They are design-artifact and plugin-availability conditions with no argv-safe filesystem probe, and the one condition that did carry a machine-readable entry — the PHPUnit runner — moved to the `test-execution` recipe, which owns the commands it is a condition of. Its check moved with a correction: `test -x vendor/bin/phpunit` reported `met` with DDEV stopped and nothing set, because Composer installs that binary regardless.

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

1. **Take the failing test.** The tier, the file, the namespace, the test name and the criterion it carries are `drupal/test-authoring.md`'s, and it hands them over red. Confirm the failure is an assertion that ran and did not hold rather than a harness error or a run that selected nothing — `drupal/test-execution.md` declares how to tell those apart. A behaviour arriving with no failing test does not enter this phase; send it back. The one exception is a unit whose deliverable is exported site configuration: it arrives with no test and goes to `## Configuration gate`.

2. **Confirm the red is the right red.** The behaviour is absent — not a broken test, and not working code broken or reverted to force the failure, which proves the test is sensitive and never that it came first (see `development/tdd-spec-driven/what-a-failing-test-proves`). A test that passed on arrival is not a starting point; return it. Once a test is committed, who may change or delete it is the mutability matrix's answer in `development/tdd-spec-driven`, not this phase's — and this phase changes none.

3. **Write the minimum code to pass (GREEN).** Implement only what the test demands — no extra features, no premature optimisation, no "while I'm here" additions. A unit whose deliverable is exported configuration is the `## Configuration gate`'s, not this step's. As you write, hold the standards inline: constructor-inject every dependency (no static `\Drupal::` in the new class), docblocks on the class and public methods, type hints on parameters and returns, no deprecated APIs, Drupal layout and naming. Run the test to green.

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
       gate:         for a configuration unit, what the ## Configuration gate lines printed
```

## State-awareness contract

The recipe reads existing state before writing. The architecture decision, the current module layout (`src/`, `*.services.yml`, `*.routing.yml`), and the tests that arrived for the component are read so new code extends the design rather than colliding with it. The method writes production code for the component under implementation, changes no test, installs nothing and writes no task record — the results are returned to the caller, which owns recording them and gating completion.

Idempotent at the discipline level: re-running on a component whose tests already pass and whose standards and security rules already hold produces no new change — the tests stay green, the linters stay clean, nothing is rewritten. A change on re-run means a regression was found or the behaviour moved, which is the method reflecting current reality, not non-determinism.

## Verifier

After the recipe runs, verify:

1. Every implemented behaviour arrived with a PHPUnit test that had been seen to fail *because the behaviour was absent* — not because working code was broken or reverted, and no test passed on arrival unexamined. The tier that test sits at is `drupal/test-authoring.md`'s choice, verified there. A configuration unit is the exception: it arrived with no test, was produced through Drupal and exported, and its `## Configuration gate` lines all exited 0 in the worktree, with line 5 not printing `There are no changes to import`, and the put-back line exited 0 after them.
2. No new class reaches for a static `\Drupal::` service; every dependency is constructor-injected.
3. The four security guarantees hold: Form API on every data-entry form (token present and checked), Twig auto-escaping intact (no unsanitised `|raw`/`#markup`), all database access parameterized, access checks on every route and operation.
4. New code carries docblocks on classes and public methods, type hints on parameters and returns, no deprecated APIs, and Drupal layout/naming — and the code-quality-tools `phpcs --standard=Drupal,DrupalPractice` and `phpstan` run over the changed files is clean (or its findings are recorded for the gate).
5. The tests are green and the refactor (if any) left them green; the results were returned to the caller for the plugin's implementation phase to record — the recipe wrote no task record of its own.
6. No test in the change was written after the code it covers — a test that cannot name a behaviour is measuring or ratifying, and does not count toward item 1. This phase wrote none of them.
8. Where the project has Playwright/ATK e2e or visual-regression coverage, it is reported separately and is not counted toward the test-first requirement in item 1.
9. Every pre-existing test the change modified or deleted was changed by a role the mutability matrix permits — the only rows that may delete are a feature removal taking its own tests in the same commit; RED authoring is the only row that writes an assertion, and GREEN, REFACTOR and a bug fix change none. A reviewer that wanted a test changed filed a finding instead. See `development/tdd-spec-driven`.

This recipe ships no executable verifier of its own — the checks above are the agent-driven protocol; the linter execution is the code-quality-tools plugin's, and the plugin's implementation phase owns the test-first completion gate.

## Configuration gate

A unit whose deliverable is exported site configuration, a field, a display, a view, a content type under the sync folder, is proved by this gate, not by a PHPUnit test. The design recipe sizes such a unit around the Drupal operation and says why a test that reads YAML back proves nothing; this section says how the configuration is produced and what proves it.

**Produce it through Drupal, never by hand.** Make the change in the worktree's site, through the UI or `drush`, then `ddev drush config:export`, and commit what the export wrote. Hand-authored YAML skips what Drupal does when it saves an object: it calculates the dependencies and casts the values to the schema. The export only copies what the site holds and repairs nothing: `config:export` compares data, not bytes, so a file whose data the site already holds is left as written. Two things the unit may not do: carry site configuration in a module's `config/install`, and edit exported YAML by hand after the export.

**"Implement only what the test demands" is about production code.** A configuration unit has no test to demand anything; its done-when lines bind on their own and the gate is how they are proved. The builder runs the gate and reports what it printed.

The gate is one `sh` block, one command per line, each line one command split on spaces and never run through a shell, from the worktree's project root. `{project}` is the `project:` line the `worktree-environment` recipe's `## Address` printed at bring-up, put in before the split, the way that recipe's `## Tear down` line takes it. It is in the snapshot names because a bare name DDEV does not find in the project's own snapshot directory is looked up in every sibling worktree's, and a name that carries the project's own is found in one place or nowhere.

The first three lines keep the worktree's database as the builder left it, under the name `gate-{project}`, and prove that they did. The first removes the copy a previous run or bring-up left, and fails when there is none. The second takes the new copy. Its exit code proves nothing, because a failure inside the snapshot itself prints `Failed to snapshot` and exits 0, so the third line restores the copy just taken: that changes nothing in the database, and it fails with `not found` when the second line kept nothing. The fourth line puts the database back to the seed the `worktree-environment` recipe left in the worktree at bring-up, under the name `seed-{project}`, so the import that follows is a real import of the branch's configuration onto a site that does not have it yet. Without that line the database already holds the change the builder made, `config:import` prints `There are no changes to import` before it validates anything, and the gate proves nothing. The restore discards everything written to the worktree's database since bring-up that the export does not carry: every node, term, user, path alias, file entity and setting, the content an earlier order's fixtures made, and anything a person changed through the UI. The seed is the main checkout's database at bring-up, and the branch's content lives nowhere else, which is why the copy is kept and proved before the seed is restored. Every line must exit 0 for the gate to pass; the consumer stops at the first non-zero line, and that line is the finding.

```sh
ddev snapshot --cleanup --name gate-{project} --yes
ddev snapshot --name gate-{project} --yes
ddev snapshot restore gate-{project}
ddev snapshot restore seed-{project}
ddev drush config:import --yes
ddev drush config:export --yes
git add --intent-to-add --no-all .
git diff --exit-code --stat HEAD
```

**Put the site back.** After a gate that reached its fourth line stops, at its last line or at the first non-zero one, the consumer runs this line from the same directory. It restores the database the gate kept, so the site holds what the builder had, content and hand edits included, and the seed stays the seed. The snapshot stays too: it is what the next gate's first line removes. The line restores the database only, so a rewrite the last gate line found stays in the sync folder, as the evidence the finding names. A gate that stopped at its first or second line, or at its third with `not found`, changed nothing and kept nothing, so there is nothing to put back and the line is not run; it would print `not found`.

```sh
ddev snapshot restore gate-{project}
```

After a gate that restored the seed, and until this line has run, the site holds the seed's content, with the branch's export on top when the import ran, and a look at its pages, an end-to-end run against its address, or a person's check would judge stale pages. On one observed run a gate that restored the seed and stopped there discarded a week of fixture content and an alias, and a person repaired the site by hand before its pages showed the branch's content again. The third gate line restored this same snapshot minutes before, so a non-zero exit here is the environment's; the database is whatever the failed restore left, and not the builder's, until a person runs the line again.

What a failure of each gate line means:

1. `not found` after `gate-{project}`: the worktree holds no snapshot by that name, and the gate stops with the database untouched. The environment's defect. When an earlier gate stopped after its first line and before its fourth, a person puts the name back with `ddev snapshot --name gate-{project} --yes` in the worktree, which copies the database as it stands. When the worktree was brought up by a `worktree-environment` recipe older than 0.4.0, or not by that recipe at all, the seed is missing too, and item 4 is the remedy. No project resolving from the directory fails here too.
2. Exits non-zero when no project resolves from the directory, or when the project was not running and DDEV could not start it, or could not return it to the state it found it in. A failure inside the snapshot itself exits 0, as above, and the next line is what catches it.
3. `not found` after `gate-{project}`: the second line kept nothing, and the gate stops before anything has changed the database. The environment's defect, and the second line's output says which.
4. `not found` after `seed-{project}`: the worktree holds no seed by that name. It was brought up by a `worktree-environment` recipe older than 0.4.0, which kept no named seed, or not by that recipe at all, or bring-up's snapshot of it failed inside itself, which shows only in that recipe's verifier listing. The environment's defect. The seed exists only as the main checkout's database, so the way to that name is that recipe's `## Bring up` again, which replaces the worktree's database with the main checkout's and loses the branch's content. That is a person's call, never the consumer's, and the gate stopped before the database changed.
5. `config:import` refused the export, and its message names the reason. `Configuration X depends on the Y configuration that will not exist after import` is the sizing defect: the order ships a file whose dependency it does not ship, or deletes a file that another still lists. On core 11.4.6, an order that deleted a field's two files and left the three displays that list it to other orders was refused with one such line per display. `Invalid data type in config ... Duplicate key` is a YAML file nobody exported. A line that prints `There are no changes to import` and exits 0 is a finding for a configuration unit, not a pass: its export changes nothing against the seed, so either the unit built nothing or line 4 did not restore. Exit codes are the consumer's to judge; this string is the reviewer's. The builder reports the gate's output with the order, and a review that finds the string there refuses the order.
6. `config:export` could not write the sync folder. The environment's defect.
7. `git add --intent-to-add --no-all .` marks files the export created so the last line sees them, and nothing else: `--no-all` leaves a deleted file to the diff instead of staging its removal. It fails only when the worktree is not a git checkout.
8. The export does not match the commit: the export rewrote, added or removed a file, and `--stat` names it. Drupal completed on save what the committed YAML lacked, or the operation touched a file the order did not commit. Diffing against `HEAD` is what makes a deletion show; a plain `git diff` misses a removed file once anything stages it. In the observed runs the import refused first and this line never failed; it stands for the YAML an import accepts and Drupal then completes.

The three lines that keep and prove the copy, the seed restore by name and the put-back line were added on 2026-09-22 from DDEV 1.25.4's source and are not yet run; `drupal/worktree-environment.md` records what was read. The observed runs above are of the gate before them, whose first line was the seed restore by `--latest`.

Why the other candidates lost: `config:status` returns rows or nothing and exits 0 either way, and Drush's own usage pipes it through `grep "No differences"` for CI, so it cannot be a line a reader judges by exit code. `config:import --diff` only changes the preview; the refusal is the same. `config:inspect` belongs to the contrib `config_inspector` module and is not assumed on a project.

What the plugin does with it: an order the design marks `proof: gate` is frozen with zero tests, its build runs the gate lines as the order's own check, records the output, and runs the put-back line after a gate that reached its fourth line; no test author is dispatched for it, and a `proof: gate` order in a project whose recipe has no `## Configuration gate` is refused at design. Reading the block, deciding the posture and recording the output are the plugin's; the lines and their meaning are this recipe's.

## Unit declaration

A Drupal module or theme exists when its `<name>.info.yml` exists, and the test harness reads nothing else to decide that: a kernel test enables its `$modules` in `setUp()` through an extension scan for info files, and a module the scan does not find stops the run there with `Unavailable module:` and the name, before any assertion runs. The run prints `ERRORS!`, the `harness:` marker of `drupal/test-execution.md`, with an assertion count of zero on that run, so by that recipe it is a setup gap and not a red. For a new module it is one of the two reds that can exist before the module does, and the other is a PHP fatal: with no info file, nothing registers the module's `Drupal\Tests\<module>\` namespace, so a test that extends a base class in that namespace stops at autoload with `Fatal error`, `not found` and the class name, exit 255 and no counts line, also a `harness:` marker of `drupal/test-execution.md`. Nothing in a build writes the info file before the tests are frozen, and a test author may not scaffold one to watch its assertions fail, because that is a production write.

```yaml
unit_declaration:
  globs:
    - "**/*.info.yml"
```

An order whose owned files match a glob here is a new unit. `checks.md` carries the same glob under `## Change-impact globs`, as the row that says which review checks a change to an info file triggers; that table answers what to re-run when the file changes, not what makes a unit exist, and a consumer asking the second question reads this block.

What the plugin does with it: at the tests freeze, a red file that holds the `harness:` marker and no `assertion:` marker is a setup gap and is refused, unless the order's owned files match a glob here, in which case the file is accepted as the new unit's red with the reason that nothing can fail an assertion before the unit exists. Deciding that is the plugin's; the glob and what it means are this recipe's.

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
| `drupal/architecture.md` | Sizes a configuration unit around the Drupal operation and names the critic's check on it; the gate here is what proves that unit |
| `drupal/worktree-environment.md` | Seeds the worktree's database from the checkout before the order, and leaves it under the name `seed-{project}`, which is what makes the gate's import a real one |

### Plugin-side tooling (referenced, not authored here)

| Source | Used for |
|---|---|
| code-quality-tools (plugin) | Execution of `phpcs --standard=Drupal,DrupalPractice` and `phpstan` over the changed files — the linter run this recipe defers to rather than re-authoring |

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| PHPUnit / DDEV (`ddev exec vendor/bin/phpunit -c phpunit.xml`) | The test runner the Unit / Kernel / Functional tiers execute against |

### Plugin-side generic mechanism (ai-dev-assistant)

The stack-neutral implementation phase this recipe binds Drupal into — when implementation runs, the test-first gate that blocks completion, and how the results are recorded against the task — is documented in the plugin itself, not duplicated here. The recipe supplies only the Drupal-specific method it owns on top of that mechanism: coding-standard application and the implementation-time security rules, applied to code written against a test that arrived red.
