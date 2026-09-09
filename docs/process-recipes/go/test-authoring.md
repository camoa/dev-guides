---
# Routing block — an orchestrator reads to here and decides.
name: go_test_authoring
capability: test-authoring
description: Use when a context is about to write the tests for one unit of work on a Go module, before any production code exists, and needs to know which level the behaviour belongs at, which package the test file declares, what the test function is called, how the criterion it specifies is traced to it, and what a Go test may not do.
# Metadata — read only after a match.
label: Test authoring (Go)
recipe_schema_version: 1.0.0
version: 0.1.0
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
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

Answer four questions for whoever is about to write a Go test: which level the behaviour belongs at,
where the file goes and what the test function is called, how the criterion it specifies is
recoverable from it, and what a Go test may not do.

**This recipe stops at red.** Its reader writes the test, watches it fail, and stops. It does not
write the code that turns the test green, and nothing here tells it to. The green and refactor half
of the cycle belongs to `go/standards-and-tests.md`, read by a different context. Running the test
belongs to `go/test-execution.md`, which several callers share.

The reader also cannot open the production source of anything already built. Every rule below is
therefore decidable from the behaviour the test must observe and from the names the package exports.
Go is unusually friendly to that constraint, and the next section says why.

## Opinion

**Declare the test file in the external test package, `package <pkg>_test`.** A test file in the same
directory may declare either the package under test or that package plus the `_test` suffix, and the
second one can only reach the exported surface — the compiler rejects a reference to an unexported
name with `undefined`, verified on Go 1.27. That makes the external package the natural default for
this reader: the boundary it must respect stops being a promise and becomes a build error. Declare
the internal package instead only when the behaviour genuinely has no exported surface, and treat
that as a finding about the design rather than a routine choice.

**The level follows the dependency surface, decided from the behaviour and not from the code.**

| Level | Where the file goes | Choose it when the behaviour needs | Cost |
|---|---|---|---|
| plain unit | `<name>_test.go` beside `<name>.go` | a function over its arguments and nothing else | microseconds |
| unit with collaborators wired | the same file | its collaborators — real ones where they are cheap and deterministic, a consumer-declared interface satisfied by a local fake only at a boundary that must be isolated | milliseconds |
| golden | the same file, expected output under `testdata/` | output large or structured enough that an inline literal would be unreadable | milliseconds |
| entry point | beside the `run(ctx, args, stdin, stdout, stderr) error` function the design put below `cmd/` | anything the command exposes: flag parsing, the exit-code mapping, the stdout and stderr split | milliseconds |
| subprocess | the same file | only what exists at the process boundary: the exit status the process really returns, signal handling, stdin arriving from a real pipe | a build per run |

The entry-point level is the default for CLI behaviour, and the subprocess level is the exception
reserved for those three things. Tests live beside the code they test; the go tool ignores any
directory named `testdata`, which is what makes it the place for goldens.

**All five levels are written before the code. A browser suite and a snapshot baseline are not.**
Those run against something already built, cannot drive a design decision, and never substitute for
a level chosen here.

**A golden file is a specification only if it was written first.** Author the expected file from the
contract and watch the test fail against it. Generate it from the program's own output with the
conventional `-update` flag and it can never contradict the code — it ratifies whatever was produced,
including a bug. This reader never runs `-update`.

**One test per behaviour the criterion names, and no more.** A table row earns its place by reaching
a branch or a boundary no other row reaches. Rows that differ only in input formatting are
duplication wearing a table's clothes. The stack-neutral statement of this belongs to
`development/tdd-spec-driven` and is cited, not restated.

## Preconditions

This phase writes files and runs nothing itself, so it declares no machine-checkable environment
condition of its own. The conditions for running a Go test — a `go.mod` at the module root and a
toolchain the go command can resolve — are declared by `go/test-execution.md`, beside the commands
they are conditions of. The step that watches a test fail reads them there.

```yaml
preconditions: []
```

## Input contract

```yaml
code_path: string             # absolute path to the module root (the dir with go.mod)
package: string               # the package the behaviour belongs to
criterion_id: string          # the identifier of the criterion this test specifies
behavior: string              # what the test must observe, in a sentence
interface: string             # the names the package exports, and the names its dependencies declare
test_level: string            # optional; unit | unit-with-collaborators | golden | entrypoint | subprocess
```

`interface` is the only thing this reader gets about code that already exists, and it is a
declaration rather than source. Where it is empty, the behaviour must be observable from the
package's exported surface alone.

## Sequence

If invoked in dry-run mode, emit the level choice, the file path, the package declaration, the test
names and the table cases planned, and write nothing. Dry-run is required.

1. **Select the level.** From `behavior` and the dependency surface it implies, using the table in
   Opinion. Use `test_level` if supplied. If the behaviour cannot be placed without opening the code,
   stop and report that rather than guessing: the choice belongs earlier.

2. **Place the file and declare the package.** `<name>_test.go` in the same directory as the code it
   tests, declaring `package <pkg>_test`. Goldens go under `testdata/` beside it. The authoritative
   file pattern is declared once, in `go/standards-and-tests.md` under `## Oracle files`, and is not
   repeated here.

3. **Name the test function.** `func TestXxx(t *testing.T)`, and the letter after `Test` must not be
   lowercase — this is enforced rather than conventional: `go vet` reports `has malformed name` and,
   because `go test` runs vet by default, the package fails to build rather than quietly skipping the
   test. The default case shape — a table of named cases ranged into `t.Run`, and when to depart
   from it — is stated once in `go/standards-and-tests.md` and is not repeated here.

4. **Name the criterion in the test.** The criterion identifier goes at the end of the name and
   nothing follows it — `TestDecodesTheHeaderC3` for a plain test, and the row name
   `decodes_header_c3` for a table case. That makes the criterion selectable, with the qualification
   that decides whether the selection is right: `-run` takes an **unanchored regular expression**, so
   `-run C3` also selects `TestDecodesTheHeaderC30`, and only `-run 'C3$'` selects the one test. For
   a table case the pattern splits on `/`, so `-run 'TestDecodesTheHeader/c3$'` selects the one row.
   Both forms were checked on Go 1.27 against a deliberate `c30` sibling. A test that specifies two
   criteria carries both, in order.

5. **Write the test.** Assert errors with `errors.Is` for a sentinel and `errors.As` for a typed
   error, against the names the design exported. Where the behaviour is safe to parallelise call
   `t.Parallel()`, and then the constraints in Verifier apply. Assert on what the criterion names,
   and nothing else.

6. **Watch it fail.** Run it through `go/test-execution.md` and read the failure signal declared
   there, never the exit status alone — a package that never compiled and an assertion that did not
   hold both exit 1, and a selector that matched nothing exits 0. Only an assertion that ran and did
   not hold is a red run. A test that passes immediately is rewritten once; if it still passes with
   no code behind it, stop and report it as proving nothing.

7. **Stop.** Return the level, the path, the test names, the criterion each carries, and the failure
   output for each. Write no production code.

## Data flow

Input: one criterion, the behaviour it names, the exported interface, the package.
Output: one or more `_test.go` files and any golden files under `testdata/`, and for each test the
criterion it carries and the output of the run that failed.
Boundaries: reads no production source; writes only test files and goldens; runs no command except
through `go/test-execution.md`; never runs a golden `-update`; produces no task record of its own.

## State-awareness contract

Before writing a new test, look for an existing test that already specifies the behaviour, by
searching the package's `_test.go` files for the criterion identifier and for the behaviour's own
vocabulary. Add a row to an existing table rather than adding a second test that overlaps it. A bug
fix almost always belongs on the existing test for the behaviour that broke.

Do not read the production source to make that decision. The test files are readable; the code is
not.

## Verifier

- Each test carries its criterion identifier at the end of its function name, or of its table row
  name, recoverable by an end-anchored match and not as a substring of a longer identifier.
- Each test file sits beside the code it tests and declares `package <pkg>_test`, or records why the
  behaviour has no exported surface.
- No test function has a lowercase letter after `Test`, which vet rejects and which therefore breaks
  the package build.
- Each new test was seen to fail, and the recorded failure is an assertion that ran and did not hold
  rather than a package that never compiled or a selector that matched nothing.
- No test asserts on an error's message text. The repair is `errors.Is` or `errors.As` against an
  exported sentinel or type; assert on the program's own stderr only where that wording is the
  contract the CLI promises.
- No parallel test, and no test with a parallel ancestor, calls `t.Setenv` or `t.Chdir`. The standard
  library panics on it — verified on Go 1.27, where the message names `t.Setenv`, `t.Chdir` and
  `cryptotest.SetGlobalRandom` together. The repair is to pass configuration as a parameter, use
  `t.TempDir()` for filesystem work, or leave the test serial with a comment saying why.
- No test mutates a package-level variable. Under `t.Parallel()` that variable is shared with every
  test running at the same time, so the failure appears somewhere else and intermittently.
- No golden file was generated from the program's output. A golden this reader writes is authored
  from the contract and seen to fail.
- No production file was written or changed.

## References

### Stack-neutral discipline (referenced, not authored here)

| Guide | What it holds |
|---|---|
| `development/tdd-spec-driven` | What a failing test proves, when not to write a test at all, the anti-patterns, and when a double is legitimate. Written for one person doing red, green and refactor; this reader does red and stops |

### Sibling process recipes

| Recipe | What it holds |
|---|---|
| `go/test-execution.md` | The command at each scope, its cost, the conditions for running one, and how to read what came back |
| `go/standards-and-tests.md` | The green and refactor half, the formatting and vet floor, the ordering traps, and the `## Oracle files` declaration that names the test file pattern |

### External origins (referenced, not authored here)

| Origin | What it settled |
|---|---|
| Go 1.27 toolchain — `go test`, `go vet`, the `testing` package | That the external test package cannot reach an unexported name; that a malformed `Test` name fails the build through vet; that `-run` is unanchored and splits on `/`; that `t.Setenv` and `t.Chdir` panic under `t.Parallel()` |
