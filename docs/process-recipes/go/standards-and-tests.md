---
# Routing block — an orchestrator reads to here and decides.
name: go_implement_standards_and_tests
capability: implement
description: Use when a Go project enters the implementation phase holding a test that already fails, and must turn it green under the toolchain's standards — applies gofmt as a non-negotiable, keeps the table-driven subtest as the default case shape, reviews a testdata/ golden as code, makes the race detector part of the ordinary test command, and treats randomized map iteration and unstable sorts as plain correctness bugs rather than trivia. Which level the test sits at and how it is written belong to the test-authoring recipe.
# Metadata — read only after a match.
label: Go standards and tests
recipe_schema_version: 1.0.0
version: 0.5.0
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
framework: go
assumes:
  - go-modules
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Hold Go implementation-phase code to the standard it must meet before it can be reviewed: formatting applied rather than debated, a test that arrived red turned green without weakening it, the race detector part of the ordinary test command rather than a special one, errors wrapped so they can be matched structurally, and the two ordering traps the language deliberately builds in caught as correctness bugs before they reach a reviewer. The judgement of which standard applies is the recipe's; the mechanical enforcement is the toolchain's, and in Go the toolchain is unusually capable of it. Choosing and writing the test is `go/test-authoring.md`'s.

The plugin owns the generic mechanism — when the implement phase runs, the test-first gate that blocks completion, the oracle-tamper guard that stops a builder weakening a measurement file, and how findings are recorded against the task. This recipe owns the part the stack-neutral mechanism cannot know: what "formatted" means when the formatter has no options, what `t.Parallel()` costs the production code around it, and which two Go behaviours produce tests that pass nine times out of ten while the code is wrong.

## Opinion

**The test is written first, and it is seen to fail.** No production code is written until a test for the behaviour exists and has been run to confirm it fails (RED) for the right reason — the behaviour is absent. Not a typo in the test, and not working code you broke or reverted to produce the failure; that proves the test is sensitive, never that it came first (see `development/tdd-spec-driven/what-a-failing-test-proves`). Then the minimum code to pass (GREEN), then refactoring under a green bar (REFACTOR). A test that passes on its first run is suspect: it is probably asserting nothing. Go makes this cheap — a test file is a sibling of the code, `go test` needs no configuration — so there is no setup cost to hide behind.

**`gofmt` is not a preference and there is nothing to configure.** The formatter deliberately ships with no style options, which means formatting is not a decision the project makes, not a thing a reviewer comments on, and not a per-file argument. It is applied — by the editor on save, and by `gofmt -w` when it was not. Add `-s` to simplify while you are there. Two consequences worth stating because they are the ones people get wrong: a project that layers a stricter formatter on top (`gofumpt`) has made a **project-level** choice which is fine, but that does not reopen the per-file conversation; and `gofmt -l` **exits 0 even when it lists unformatted files**, so any check that trusts its exit code is a gate that can never fail. Assert on empty output instead.

**Table-driven subtests are the default shape, and a non-table test needs a reason.** The default is a slice of anonymous-struct cases with a `name` field, ranged over into `t.Run(tt.name, …)`. This is not stylistic: subtests give each case its own name in the failure output, make `-run` able to select one case, and let one case fail without hiding the rest. Depart from it when the arrangement genuinely differs per case — when the table would fill with fields most rows leave zero, the table has stopped being a table and a few explicit tests are clearer. Since Go 1.22 the loop variable is per-iteration, so the old advice to shadow `tt` inside the loop is obsolete; code still doing it is copying a workaround for a bug the language fixed.

**A golden file is reviewed as code.** Where goldens live is stated in `go/test-authoring.md`, beside the reader that writes them. What matters to this reader is what happens when one changes. The conventional `-update` flag that rewrites the goldens is genuinely useful and genuinely dangerous, and the danger is the whole reason this appears here: **a `-update` run whose diff nobody reads is how wrong output gets frozen into the expectations forever**, and every subsequent run then proves the bug still reproduces. So the rule is that a golden regeneration is a diff to be read line by line in review, exactly like a source change — and a golden file that changed in a commit that was not *supposed* to change output is a finding, not a formality.

**`t.Parallel()` is worth it, and it makes shared state a bug rather than a smell.** Marking tests parallel is how a suite stays fast as it grows, but it converts anything process-global from a latent hazard into an actual flake. What it rules out — `t.Setenv`, `t.Chdir`, and a package-level variable a test mutates — is stated in `go/test-authoring.md`, beside the reader that would write one. What it means for **production** code is the part that belongs here: package-level mutable state is what makes those rules bite at all, so new code carries none, and configuration is a parameter rather than an environment read. Concurrency that involves waiting is better tested with the standard library's testing/synctest bubble and its fake clock than with a `time.Sleep` tuned until CI stops complaining.

**`-race` belongs in the normal test command, not a nightly job.** The race detector only reports races on code paths that actually execute during the run, so its coverage is exactly the coverage of the tests it runs under — which means running it once a night against the same tests finds nothing that running it every time would not have found sooner and cheaper. `go test -race ./...` is *the* test command. It costs roughly an order of magnitude in time and memory, and that is the correct trade at the size of a test suite. Two companions belong in the same habit: `-shuffle=on`, which randomises test order and is **off by default**, catching tests that only pass because an earlier test left state behind; and `-count=1` when you need to defeat the test result cache and force a real run.

**Errors are wrapped on the way up with `%w`, so they can be matched structurally.** A sentinel or a typed error the design exported only survives the call stack if every layer wraps rather than reformats, and an error rebuilt with `fmt.Errorf("...: %v", err)` has thrown the match away. `errors.Join` is the tool when a single operation genuinely produces several failures worth reporting together. How a **test** asserts on one — `errors.Is` for a sentinel, `errors.As` for a typed error, never message text — is stated in `go/test-authoring.md`.

**Ranging over a map to build output is a correctness bug the tests will usually pass.** Map iteration order in Go is deliberately randomized, and the "usually" is what makes this dangerous rather than merely known: with a small map the randomization frequently lands on the same order several runs in a row — a five-key map in a quick check here produced the keys in sorted order in three of six iterations — so a test written against one run's output passes, passes again, passes in CI, and then fails once a fortnight on a machine that hashed differently. Anywhere iteration order reaches the outside world — JSON, a report, a generated file, a diff, a log line consumed by anything — collect the keys into a slice, sort it, and range the slice. This is not a testing tip; it is the code being wrong.

**`sort.Slice` and `slices.SortFunc` are not stable, so a partial sort key produces arbitrary output.** Both document explicitly that equal elements may be reordered. When the comparison function only looks at some of what distinguishes two records, every tie is resolved arbitrarily and the output changes between runs and between Go versions — the same shape of bug as the map one, with the same nine-times-out-of-ten test. The fix to prefer is **making the sort key total**: add a tiebreaker (an ID, a name, the source order captured as a field) so no two elements compare equal. Reach for `sort.SliceStable` or `slices.SortStableFunc` only when preserving the *input* order of ties is genuinely the intended behaviour — stability preserves whatever order the input happened to have, which is a weaker guarantee than a key that has one right answer.

**Coverage that runs against something already built does not count toward the test-first requirement.** A Playwright suite or a snapshot baseline, where a project has one, cannot drive a design decision and is written after the behaviour exists. Report it separately. Which levels *are* inside the loop — every one of them, including the subprocess level, because the line is authoring order and not whether a process is spawned — is stated in `go/test-authoring.md`.

**A regenerated golden has stopped being a test, which is why the oracle table halts on one.** That a golden is a specification only if it was authored from the contract rather than generated from the program's output is stated in `go/test-authoring.md`, beside the reader that writes one. What belongs here is the consequence for a builder: the halt on a golden modification is not about carelessness, it is that regenerating a golden to make a red gate green replaces the expectation with the behaviour and every later run then proves the bug still reproduces.

**Adding a test is not automatically progress.** The loop's requirement for a change is one specification per behaviour it creates, at the level `go/test-authoring.md` chose, each seen to fail first *because the behaviour it names did not exist yet*. Past that, more tests make the change harder to review without specifying anything new. The full set of excess cases belongs to `development/tdd-spec-driven` and is cited, not restated, and the Go-specific forms are stated in `go/test-authoring.md` beside the reader that would write them.

**The toolchain runs the standards; there is no plugin to defer to here.** Unlike the PHP CLI recipe, this one does not hand linting to the `code-quality-tools` plugin — that plugin detects Drupal and Next.js projects and lints PHP and JavaScript extensions, and has no Go arm. It does not need one: `gofmt`, `go vet`, `go test -race`, and `go mod tidy -diff` ship with the toolchain and run from the module root with no configuration, and the optional layer (`golangci-lint`, which as of v2 embeds the full staticcheck rule set) is a single binary with a committed config. Run them here as you write, and again as gates in review.

## Preconditions

- A Go project with a `go.mod` at the module root and a toolchain the go command can resolve, so `go vet` and `gofmt` run without setup. Both conditions carry machine-readable entries in the `test-execution` recipe for this framework, which owns the commands they are conditions of.
- The design phase has produced an architecture decision (see the architecture recipe under this framework): the `internal/`-versus-exported boundary, the `run(ctx, …)` entry point below each command, the exit-code contract, and the exported error surface are known, so this phase builds against a plan rather than improvising structure.
- Where the project uses `golangci-lint`, its config is committed at the module root, so the same rule set runs locally and in review.
- The plugin's generic implement phase is present: the test-first gate, the oracle-tamper guard, and the task record. This recipe supplies the Go-specific standards-and-tests method; it does not recreate the gate.

All four stay prose here. The module and toolchain claims are checkable, and their entries — with the honest limitation that `go version` is both the check and its own subject — moved to the `test-execution` recipe alongside the commands that need them. The remaining three are design-artifact and plugin-availability conditions with no argv-safe filesystem probe.

```yaml
preconditions: []
```

## Input contract

Source-agnostic, supplied by the caller (the orchestrator at the implement phase, or a human operator).

```yaml
code_path: string             # absolute path to the Go module root (the dir with go.mod)
component: string             # the unit being implemented (a package, a command, a type…)
behavior: string              # the specific behaviour to test-drive and build
test_tier: string             # the level the test-authoring recipe chose, carried through
architecture_ref: string      # optional; pointer to the design decision this implements
```

## Sequence

If invoked in dry-run mode, perform all reads and emit a standards plan (what the code must do to turn the test green, the golden files involved, the ordering sweep to run) instead of writing production code. Dry-run is required.

1. **Take the failing test.** The level, the file, the package declaration, the test name and the criterion it carries are `go/test-authoring.md`'s, and it hands them over red. Confirm the failure is an assertion that ran and did not hold rather than a package that never compiled or a selector that matched nothing — `go/test-execution.md` declares how to tell those apart, and all three exit statuses lie about which one happened. A behaviour arriving with no failing test does not enter this phase; send it back.

2. **Confirm the red is the right red.** The behaviour is absent — not a failure produced by breaking or reverting working code, which proves the test is sensitive and never that it came first. A test that passed on arrival is not a starting point; return it. Once a test is committed, who may change or delete it is the mutability matrix's answer in `development/tdd-spec-driven`, not this phase's — and this phase changes none.

3. **Write the minimum code to pass (GREEN).** Implement only what the tests demand. As you write, hold the design's boundary: new packages under `internal/` unless the design promoted them, the command a shim over the entry point, `ctx` first on anything that blocks, errors wrapped with `%w`, no `init` side effects, no package-level mutable state, and `os.Exit` confined to `main`. Run `go test ./...` to green.

4. **Sweep the two ordering traps before the unit is called done.** Search the new code for a `range` over a map whose iteration reaches output, and for a `sort.Slice` or `slices.SortFunc` whose comparison does not fully distinguish two elements. Fix the first by collecting keys, sorting the slice, and ranging that; fix the second by making the sort key total with a tiebreaker (reaching for the stable variant only where preserving input order of ties is the actual requirement). A behaviour whose order is part of the contract needs a test that pins it — one that would fail against the unsorted version, which for the map case means asserting the full sequence rather than set membership. That test is authored by `go/test-authoring.md` and arrives red like any other; where the sweep finds an ordering bug no test pins, report it as a gap rather than writing one here.

5. **Apply the formatting and the vet floor.** Run `gofmt -l .` and confirm it lists nothing, remembering that it exits 0 either way, so the assertion is on empty output; run `gofmt -s -w` on anything it named. Run `go vet ./...` over the whole module — not just the changed package, and not relying on `go test` to have done it, because `go test` runs only a high-confidence subset of the analyzers and several of the ones that matter most here are outside that subset.

6. **Run the real test command.** `go test -race ./...`, with `-shuffle=on` at least once before handing back, and `-count=1` where the result cache would otherwise hide a real run. A race the detector reports is fixed now — it is a real data race that happened, not a warning.

7. **Refactor under green (REFACTOR).** With tests green, improve structure without changing behaviour — collapse duplication, narrow a consumer-side interface to what the consumer actually calls, tighten a value type. Re-run `go test -race ./...`; it stays green or the refactor is reverted.

8. **Confirm the module manifest and hand back.** Run `go mod tidy -diff`, which prints the changes tidy would make and exits non-zero when there are any, so a requirement added or orphaned during the work is caught here rather than in review. Return the test results, the ordering-trap sweep, the formatting and vet outcome, the race-detector result, and the tidy result to the caller; the plugin's implement phase records them against the task and owns the completion gate. The recipe writes production code for the component, changes no test, and writes no task record of its own.

## Data flow

```
input: code_path, component, behavior, test_tier (optional), architecture_ref (optional)

reads project state:
       architecture decision (internal/ boundary · run(ctx,…) entry point ·
                              exit-code contract · exported error surface)
       go.mod (the `go` language line, the require closure, tool directives)
       the existing package tree and the tests beside it
       testdata/ (the golden files the component's output is pinned against)
       .golangci.yml where the project commits one

applies opinion:
       the test arrives red and is not rewritten (GREEN→REFACTOR) · gofmt is not a
       preference and `gofmt -l` exits 0 regardless · table-driven subtests as the
       default shape · a golden is reviewed as code, never regenerated unread ·
       no mutable package-level state · errors wrapped with %w · -race in the
       ordinary command, plus -shuffle=on · map-range order is a correctness bug ·
       unstable sorts need a total key · the toolchain runs the standards, there is
       no Go arm in code-quality-tools

references origin (never duplicated):
       the go command    — go test / go vet / go mod tidy -diff, run from the module root
       gofmt             — the formatter, applied not configured
       the architecture recipe — the boundary, the entry point, the error surface

emits (to the caller; the recipe writes no task record):
       tests:      the test(s) it received red, now green and unchanged
       code:       the minimum production code that turns them green, design boundary held
       ordering:   the map-range and unstable-sort sweep result + the tests that pin order
       toolchain:  gofmt (empty list) · go vet ./... · go test -race ./... · -shuffle=on ·
                   go mod tidy -diff
```

## State-awareness contract

The recipe reads existing state before writing. The architecture decision, the current package tree, the tests already beside the code, the golden files under `testdata/`, and the `go.mod` require closure are read so new code extends the design and a golden file is recognised as an existing expectation rather than a blank to fill. The method writes production code for the component under implementation, changes no test, adds no requirement of its own beyond what the design named, and writes no task record — the results are returned to the caller, which owns recording them and gating completion.

Idempotent at the discipline level: re-running on a component whose tests already pass under `-race`, whose formatting is already clean, and whose `go mod tidy -diff` is empty produces no new change. A change on re-run means a regression was found or the behaviour moved. One qualification specific to Go: a re-run with `-shuffle=on` uses a different order and can legitimately surface a failure the previous run did not — that is the flag doing its job on a test suite with hidden order coupling, and the correct response is to fix the coupling, not to drop the flag.

## Verifier

After the recipe runs, verify:

1. Every implemented behaviour arrived with a test that had been seen to fail *because the behaviour was absent* — not because working code was broken or reverted, and no test passed on arrival unexamined. The level that test sits at is `go/test-authoring.md`'s choice, verified there.
2. Tests are table-driven subtests unless a recorded reason says otherwise, and no test shadows the loop variable to work around a language behaviour fixed in Go 1.22.
3. New code carries no mutable package-level state, so nothing a parallel test touches is shared, and every error it returns is wrapped with `%w` rather than reformatted, so the sentinels and types the design exported survive to the assertion.
5. Any golden file under `testdata/` that changed was reviewed as a diff, and a golden that moved in a change that was not meant to alter output is raised as a finding rather than accepted.
6. The ordering sweep ran: no `range` over a map reaches output without the keys being collected and sorted first, and every `sort.Slice` / `slices.SortFunc` comparison either distinguishes all elements or has a recorded reason for using the stable variant — with a test pinning the resulting order.
7. `gofmt -l .` lists nothing (asserted on empty output, not on the exit code), and `go vet ./...` is clean over the whole module rather than left to the reduced analyzer subset `go test` runs.
8. `go test -race ./...` is green, has been run at least once with `-shuffle=on`, and no reported race was left unfixed.
9. `go mod tidy -diff` exits zero — no requirement was added, orphaned, or left un-tidied by the work.
10. No test in the change was written after the code it covers — a test that cannot name a behaviour is measuring or ratifying, and does not count toward item 1. This phase wrote none of them.
11. Every new table row reaches a branch or boundary no other row reaches; rows differing only in input formatting are duplication, not coverage.
13. Every pre-existing test the change modified or deleted was changed by a role the mutability matrix permits — the only rows that may delete are a feature removal taking its own tests in the same commit; RED authoring is the only row that writes an assertion, and GREEN, REFACTOR and a bug fix change none. A reviewer that wanted a test changed filed a finding instead. See `development/tdd-spec-driven`.
12. The results were returned to the caller for the plugin's implement phase to record — the recipe wrote no task record of its own.

This recipe ships no executable verifier of its own — the checks above are the agent-driven protocol, and every one of them is a command the Go toolchain already provides; the plugin's implement phase owns the test-first completion gate.
## Oracle files

A measurement oracle is a file the gates read to decide pass or fail — a linter config, a test, an expected-output fixture. An autonomous builder must never weaken one to make a red gate go green: only adding tests or fixing code is allowed, never suppressing a finding or rewriting an expectation. The plugin's deterministic oracle-tamper guard enforces this at the review/critique rung, but the guard itself is framework-agnostic — it carries no Go knowledge and monitors only the file list it is handed. This section is that list for a Go project: the caller reconstructs it from here on every run (so there is no persistent project file a builder could empty to switch monitoring off) and hands it to the guard.

Each rule names the change kinds it watches (A added, M modified, D deleted), the oracle class the change touches, and a severity. A **halt** is terminal tamper unless the work-order's `oracle_update` field explicitly exempts that class; a **flag** is recorded and the work ships flagged, never blocked.

The class names match the work-order `oracle_update` exemption vocabulary, so a human-authored exemption lines up with what the guard sees.

| Oracle file | Watches | Class | Severity | Why |
|---|---|---|---|---|
| Test files (`*_test.go`, anywhere in the module) | delete | test-delete | halt | Deleting a test removes the behaviour it guards — the builder must add tests, never drop them, to pass. |
| Golden files under any `testdata/` directory | modify / delete | golden-update | halt | A golden file *is* the expected output. Regenerating it is the one edit that turns a failing assertion green while leaving the bug in place, and it is invisible in a summary — the diff must be read by a human, so an autonomous regeneration halts. |
| `.golangci.yml` / `.golangci.yaml` / `.golangci.toml` | modify | lint-config | flag | The linter config sets which linters run and which paths and rules are excluded — a change can quietly lower the bar; recorded for review. |
| `go.mod` | modify | dependency-manifest | flag | The manifest carries the language version and the require closure — lowering the `go` line or adding a requirement changes what the gates compile and analyse; recorded for review. |
| CI workflow files (`.github/workflows/*.yml`, `.github/workflows/*.yaml`) | modify | coverage-threshold | flag | Go ships no coverage-threshold config of its own, so a project's gate thresholds and its `-race` / `-shuffle` flags live in the workflow — a change there can disable a gate without touching a line of Go; recorded for review. |

The caller emits this list as the oracle-tamper guard's JSON input. The two columns the guard needs beyond the table are the path globs and the watched-change set:

```json
[
  { "type": "test_delete",        "globs": ["**/*_test.go"],                                        "changes": ["D"],     "oracle_class": "test-delete",         "severity": "halt" },
  { "type": "golden_update",      "globs": ["**/testdata/**"],                                      "changes": ["M","D"], "oracle_class": "golden-update",       "severity": "halt" },
  { "type": "lint_config",        "globs": [".golangci.yml", ".golangci.yaml", ".golangci.toml"],   "changes": ["M"],     "oracle_class": "lint-config",         "severity": "flag" },
  { "type": "dependency_manifest","globs": ["go.mod"],                                              "changes": ["M"],     "oracle_class": "dependency-manifest", "severity": "flag" },
  { "type": "coverage_threshold", "globs": [".github/workflows/*.yml", ".github/workflows/*.yaml"], "changes": ["M"],     "oracle_class": "coverage-threshold",  "severity": "flag" }
]
```

Two of these differ from the PHP CLI and Drupal lists in a way worth stating, because the difference is what makes them worth declaring rather than copying. Go has **no static-analysis baseline file** — there is no equivalent of a phpstan baseline to append a new finding to, so that halt rule has no Go counterpart and its absence here is deliberate rather than an omission. In its place, Go has an oracle the other stacks do not: the **golden file**, which is the expected output itself, and which a `-update` run rewrites wholesale. That is the highest-risk tamper surface in a Go project and it is why it is a halt rather than a flag. A project that declares no oracle files at all is an honest "no oracle configured" state: the guard reports it ran with nothing to watch, rather than reporting a pass it never checked.

## References

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| The go command (`go test`, `go vet`, `go mod tidy -diff`, `go help testflag`) | The test runner every tier executes against, the analyzer floor, the manifest check, and the flag semantics behind `-race`, `-shuffle`, and `-count` — including that `go test` runs only a high-confidence subset of vet's analyzers |
| `gofmt` | The formatter with no style options — applied, not configured; and the `-l` behaviour (it exits 0 even when it lists files) that a check must assert around |
| The `testing` package (`t.Parallel`, `t.TempDir`, `t.Setenv`, `t.Chdir`, `t.Context`, `t.Run`) | The test shape and the documented parallelism restrictions the tier decisions rest on |
| testing/synctest (Go 1.25+) | The bubble and fake clock used to test concurrency that involves waiting, in place of a tuned `time.Sleep` |
| The `errors` package and `fmt.Errorf` | The `%w` wrapping and the `errors.Is` / `errors.As` / `errors.Join` matching that replaces message-text comparison |
| The `sort` and `slices` package documentation | The explicit non-stability of `sort.Slice` and `slices.SortFunc`, and the stable variants — the basis for preferring a total sort key |
| The Go language specification | Map iteration order being unspecified and randomized, which is why ranging a map into output is a correctness bug rather than a style issue |
| `golangci-lint` (v2) | The optional linter layer above the toolchain floor, whose `staticcheck` linter embeds the full staticcheck rule set as of v2 — a single binary with a committed config, not a plugin dependency |

### Sibling process recipes

| Recipe | What it holds |
|---|---|
| `go/test-authoring.md` | Which level a behaviour belongs at, where the file goes and what the test function is called, how a criterion is traced to a test, and what a Go test may not do — the half of the cycle that ends at red |
| `go/test-execution.md` | The command at each scope, its cost, the conditions for running one, and how to read what came back |

### Plugin-side generic mechanism (ai-dev-assistant)

The stack-neutral implement phase this recipe binds Go into — when implementation runs, the test-first gate that blocks completion, the oracle-tamper guard that reads the list above, and how the results are recorded against the task — is documented in the plugin itself, not duplicated here. The recipe supplies only the Go-specific method it owns: `gofmt` as a non-negotiable, table-driven subtests as the default case shape, a golden reviewed as code and never regenerated unread, no mutable package-level state, errors wrapped with `%w`, `-race` in the ordinary command, and the map-iteration and unstable-sort traps.

Unlike the PHP CLI recipe under this root, this one does **not** defer linter execution to the `code-quality-tools` plugin: that plugin detects Drupal and Next.js projects and lints PHP and JavaScript file extensions, and has no Go arm. The Go toolchain runs its own standards from the module root, which is why the commands above are named directly rather than delegated.
