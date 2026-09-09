---
# Routing block — an orchestrator reads to here and decides.
name: go_test_execution
capability: test-execution
description: Use when anything needs to run a Go test — the failing-test step watching one case, a baseline taken before code exists, a build check running the suite, or a fixer running the tests over its change — and needs the command, its cost, and how to tell a failed assertion from a package that never compiled.
# Metadata — read only after a match.
label: Test execution (Go)
recipe_schema_version: 1.0.0
version: 0.1.0
requires_guides:
  - development/tdd-spec-driven
# Process-recipe routing keys, enforced by validate_recipes.py for any recipe
# under docs/process-recipes/. `capability` above doubles as the phase; there is
# no separate applies_to_phase. `framework` is the second routing dimension.
recipe_class: process
framework: go
assumes:
  - go-modules
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Answer one question for a Go module: what command runs a test, at each of the scopes something actually asks for — the whole module, one file, one case, the tests covering a change, and the cheapest thing that proves the toolchain works at all. Carry the traps that make a Go test command select more or fewer tests than it reads as, what the race detector costs, and the output that separates a failed assertion from a package that never compiled.

This recipe runs nothing and judges nothing. It is read by whatever is about to run a test, and the callers differ: the author watching one case fail, the baseline taken before any code exists, each build check, and the fixer running the tests over its own change. One answer, four callers.

## Opinion

**A command is argv, never a shell string.** Each row below is a list of tokens executed directly. A token that is exactly a named placeholder is replaced whole, and the substituted value never reaches a shell. Go makes this easy to get wrong in one specific way: `./...` looks like a glob and is not — it is a literal package pattern the go command expands itself, so a shell that expanded it first would pass something else entirely.

**`-run` is an unanchored regular expression, so it over-selects by default.** `-run TestAdd` also runs `TestAddBar` — observed, not inferred. Anchor both ends: `-run '^TestAdd$'`. For one case inside a table, the pattern is a slash-separated path, `-run '^TestSub$/^one_case$'`, and Go matches either the subtest's written name or the underscored form it reports.

**A `-run` that matches nothing exits zero.** The output says `[no tests to run]` and the exit status is success, so a mistyped test name is indistinguishable from a passing run by exit code alone. A package with no test files says `[no test files]` and also exits zero. Both are silence, and silence is not green.

**The exit code does not separate a failed assertion from a package that would not build.** Both are 1 — observed on go1.27.1. The distinguisher is the output marker: `--- FAIL: TestName` is a test that ran and asserted; `FAIL <package> [build failed]` is a compiler error, which says nothing about behaviour. Anything reading only the exit status treats a broken build as a failing test and reports a red that proves nothing.

**`-race` belongs in the suite command, and its cost is real.** It costs roughly an order of magnitude in time and memory, which is the correct trade at the end of a task and the wrong one on every keystroke. `-shuffle=on` is off by default and catches order coupling; `-count=1` defeats the result cache when a real run is needed rather than a remembered one.

**Go's unit of test selection is the package, not the file.** A `_test.go` file cannot be run on its own without naming every other file its package needs on the same command line. That is why the file row below is answered with absence and a package-scoped nearest form, rather than with a command that pretends otherwise.

## Preconditions

- A Go module: a `go.mod` at the module root, so the go command resolves packages at all.
- A Go toolchain the go command can resolve, so `go test` runs without setup.

Both are checkable and are declared in machine-readable form below. Both name an owner, and the owner is the operator rather than a plugin — a Go toolchain is installed by whoever set the machine up, and nothing in this catalog installs one. Recording that is the point: an entry with no owner and an entry nobody owns are different states, and leaving the key off makes them look the same.

One honest limitation, recorded rather than hidden. `go version` is both the check and its own subject, so with no toolchain installed it exits 127 and the engine records `unknown / check_command_not_found` — a missing checker says nothing about the precondition, applied to the case where the missing checker *is* the finding. That is weaker than `unmet`, but it is not `met`. The module-root check has no such ambiguity: `test` is always available, so it answers either way.

```yaml
preconditions:
  - id: go-module
    what: a go.mod at the module root, so the go command resolves packages at all
    check: test -f go.mod
    owner: operator
  - id: go-toolchain
    what: a Go toolchain the go command can resolve, so go test runs without setup
    check: go version
    owner: operator
```

## Input contract

Source-agnostic, supplied by the caller.

```yaml
code_path: string             # absolute path to the module root (the dir with go.mod)
scope: string                 # suite | file | test | changed | smoke — the row to resolve
package: string               # optional; one package pattern, e.g. ./internal/store
test_id: string               # optional; one anchored -run pattern
packages: [string]            # optional; the package patterns a change is scoped to
```

## Test commands

Five rows. Each is a command or a named statement that Go has none. `{package}` is one package pattern, `{test_id}` one anchored `-run` pattern, and `{packages}` a list that expands to one token per element.

```yaml
test_commands:
  - id: suite
    argv: ["go", "test", "-race", "./..."]
    cost: end-of-task
    trap: >-
      `-race` costs roughly an order of magnitude in time and memory. Run with
      `-shuffle=on` at least once before handing back, and add `-count=1` where the
      result cache would otherwise return a remembered pass instead of a real run.
  - id: file
    absent: >-
      Go compiles and runs tests per package, not per file. Naming one `_test.go`
      file requires naming every other file its package needs on the same command
      line, which is not a selection mechanism.
    nearest: ["go", "test", "-race", "{package}"]
  - id: test
    argv: ["go", "test", "-race", "{package}", "-run", "{test_id}"]
    id_form: >-
      An anchored regular expression, `^TestName$`, or for one table case
      `^TestName$/^case_name$`. Go matches either the subtest's written name or the
      underscored form it reports, so a name with spaces works in both forms.
    cost: every-attempt
    trap: >-
      `-run` is unanchored, so `-run TestAdd` also runs `TestAddBar`. A pattern that
      matches nothing prints `[no tests to run]` and exits 0, so a mistyped name
      reports success — read the output, not the status.
  - id: changed
    absent: >-
      The go command maps no set of changed files to the tests covering them. The
      caller derives the packages containing the changed files and passes those.
    nearest: ["go", "test", "-race", "{packages}"]
  - id: smoke
    argv: ["go", "test", "-run", "^$", "./..."]
    cost: every-attempt
    trap: >-
      Compiles every test binary in the module and runs no test. It proves the
      toolchain, the module graph and every test file compile; it proves nothing
      about behaviour, and it exits 0 on a module whose every test would fail.
```

**What each row costs.** Go has no test tiers, so the cost is set by the flags and the breadth, not by a tier name.

| Command | Cost | Run it |
|---|---|---|
| `go test -run '^$' ./...` | compile only | every build attempt |
| `go test -race <package> -run <one test>` | one package, one case | every build attempt |
| `go test -race <packages>` | the changed packages | every build attempt |
| `go test -race ./...` | the whole module, roughly ten times the un-raced cost | once, at the end of a task |

**Telling a failed assertion from harness noise.** Go's exit code carries less information than it appears to, so the marker in the output is what decides.

```yaml
failure_signal:
  assertion: >-
    Exit 1 with a `--- FAIL: TestName` line — the test ran and its assertion did not
    hold. This is the only outcome that proves a behaviour is absent.
  harness: >-
    Exit 1 with `FAIL <package> [build failed]` — the package or its test file did
    not compile, so nothing was asserted. Observed on go1.27.1: a compile error and a
    failed assertion produce the same exit status and differ only in this marker.
  silent_pass: >-
    Exit 0 with `[no tests to run]` (a `-run` pattern matched nothing) or
    `? <package> [no test files]` (a package has no tests). Both report success
    while proving nothing, so the output must be read before a green is believed.
```

## Sequence

If invoked in dry-run mode, resolve and return the command without executing it. Dry-run is required.

1. **Resolve the row.** Take `scope` and select the matching row above. A row answered with `absent:` returns that statement and its `nearest:` form; it does not fall through to a wider command.

2. **Substitute the placeholders.** Replace each placeholder token whole. A list placeholder expands to one token per element. `./...` and any package pattern are passed as written — the go command expands them, not a shell.

3. **Apply the cost label.** Return the row's `cost` with the command, so a caller running on every build attempt does not receive the full raced suite.

4. **Return the command, the cost, and the failure signal.** The caller runs it. This recipe neither executes it nor judges its output.

5. **Read the result against the failure signal.** Whatever ran the command checks for `[build failed]`, `[no tests to run]` and `[no test files]` before believing either a red or a green, because all three are reported with the exit status of something else.

## Data flow

```
input: code_path, scope, package / test_id / packages (optional)

reads project state:
       go.mod (the module root the commands run from)
       the package tree, to map a changed file to the package that holds it

applies opinion:
       argv, never a shell string · ./... is a package pattern, not a glob ·
       -run is unanchored and over-selects · a pattern matching nothing exits 0 ·
       a build failure and a failed assertion share exit 1 and differ by marker ·
       -race in the suite command, at roughly ten times the cost

references origin (never duplicated):
       the go command — go test and its flags, run from the module root

emits (to the caller; the recipe runs nothing):
       command:  the argv token list for the requested row, placeholders substituted
       cost:     every-attempt | end-of-task
       signal:   how to read the output — assertion, build failure, or nothing ran
```

## State-awareness contract

The recipe reads. It writes no file, runs no command, and records nothing against the task. Resolving the same row with the same input returns the same command; what the command then does depends on the module's state, which is the caller's to observe.

## Verifier

After the recipe runs, verify:

1. The returned command is a token list, and every placeholder was substituted as a whole token — nothing was concatenated into a token and nothing reached a shell.
2. The row requested was the row returned. The file row returned absence and a package-scoped nearest form, not a command claiming to run one file.
3. Any `-run` pattern was anchored at both ends, and a table case was selected with the slash-separated form.
4. The cost label travelled with the command, and no caller running on every build attempt received the full `-race ./...` suite.
5. Any result reported as red was checked for `[build failed]` first, and any result reported as green was checked for `[no tests to run]` and `[no test files]`.
6. Where the suite ran as the end-of-task gate, it ran at least once with `-shuffle=on`, and `-count=1` was used wherever a cached result would otherwise stand in for a real run.

This recipe ships no executable verifier of its own — it produces a command and the means to read the result, and the phase that runs it owns the gate.

## References

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| The go command (`go test` and its flags) | Every command in this recipe, run from the module root |
| `development/tdd-spec-driven` | What a failing test proves, and why a run that asserted nothing is neither red nor green |

### Plugin-side generic mechanism (ai-dev-assistant)

The phases that run these commands — the failing-test step, the baseline, the build checks, the fixer — are the plugin's, along with whatever records their results. This recipe supplies only what Go cannot be guessed at: the command per scope, its cost, and how to read what came back.
