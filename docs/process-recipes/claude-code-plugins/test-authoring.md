---
# Routing block — an orchestrator reads to here and decides.
name: claude_code_plugins_test_authoring
capability: test-authoring
description: Use when a context is about to write the tests for executable code a Claude Code plugin ships — a hook script, a validator, a helper — before that code exists, and needs to know which level the behaviour belongs at, where the spec file goes, what it is called, how the criterion it specifies is traced to it, and what such a spec may not do. Not for a plugin component whose whole substance is instructions; that is paper-traced instead, and this recipe says where.
# Metadata — read only after a match.
label: Test authoring (Claude Code plugins)
recipe_schema_version: 1.0.0
version: 0.2.0
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
requires_guides:
  - development/tdd-spec-driven
# Process-recipe routing keys, enforced by validate_recipes.py for any recipe
# under docs/process-recipes/. `capability` above doubles as the phase; there is
# no separate applies_to_phase. `framework` is the second routing dimension.
recipe_class: process
framework: claude-code-plugins
assumes:
  - claude-code-plugin
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Answer four questions for whoever is about to write a test for the executable code a plugin ships:
which level the behaviour belongs at, where the file goes and what it is called, how the criterion it
specifies is recoverable from it, and what such a spec may not do.

**This recipe stops at red.** Its reader writes the spec, watches it fail, and stops. It does not
write the script that turns the spec green, and nothing here tells it to. The authoring half of the
cycle belongs to `claude-code-plugins/authoring-standards.md`, read by a different context. Running
the spec belongs to `claude-code-plugins/test-execution.md`.

## Opinion

**Most of a plugin is not tested by this recipe, and that is the framework's real shape.** A skill,
a command, an agent and the instruction half of a hook are prose. What stands in for a failing test
there is tracing the component's instructions against what the design said it must do, before
anything relies on it — that trace is `claude-code-plugins/authoring-standards.md`'s business and it
leaves no file behind. This recipe is for the other half of that sentence: **a plugin that ships
executable code — a hook script, a validator, a helper — is ordinary code, and it gets ordinary
test-first treatment.** Nothing below applies to a component that is only instructions.

**The level follows what the behaviour reaches, decided from the contract and not from the script.**

| Level | Where the file goes | Choose it when the behaviour needs | Cost |
|---|---|---|---|
| unit, in the script's own language | `<plugin>/tests/test_<module>.py` for a Python script, `<plugin>/tests/<topic>-spec.mjs` for a Node one | a function over its arguments: a rule's decision, a parser's output | milliseconds |
| script contract | `<plugin>/tests/<topic>-spec.sh` | what a caller reading only the exit code and the printed output is told: run the real script against a fixture tree and assert on both | tenths of a second |
| event contract | `<plugin>/tests/<hook-name>-spec.sh` | what a hook does with an event: pipe a sample payload to the handler on stdin and assert on the exit code the event assigns it | tenths of a second |
| runner | `<plugin>/tests/<runner>-spec.sh` | the aggregate answer several scripts produce together, including the case where a check could not look at all | seconds |

The runner level is the one most easily skipped and the one worth keeping. A run where a check could
not look must not come back zero however many other checks passed, and the only way to specify that
is to drive the runner in an environment where the check genuinely cannot look.

**A spec is a plain script that counts, not a framework.** It runs under `bash`, builds every fixture
it needs under `mktemp -d` with a `trap` that removes it, counts passes and failures, prints one line
per failure, and ends by exiting on the counters. It never touches the developer's real tree.

**The delete guard watches the shell specs, and does not watch the rest.**
`claude-code-plugins/authoring-standards.md` declares `**/tests/**/*-spec.sh` and
`**/tests/**/*-spec.bats` as the files whose deletion halts a builder. A unit test written in the
script's own language sits in the same `tests/` directory and outside those two patterns, so
deleting it is not guarded. Write it anyway — the guard's coverage is a question for that
declaration, not a reason to leave a script's rules unspecified — but know which of your tests is
protected and which is not.

**One spec case per behaviour the criterion names, and no more.** The full set of excess cases
belongs to `development/tdd-spec-driven` and is cited, not restated.

## Preconditions

This phase writes files and runs nothing itself, so it declares no machine-checkable environment
condition of its own. What this framework has instead of a test harness, and what answers in its
place, is declared by `claude-code-plugins/test-execution.md`.

```yaml
preconditions: []
```

## Input contract

```yaml
code_path: string             # absolute path to the plugin root
script: string                # the script the behaviour belongs to, relative to the plugin root
criterion_id: string          # the identifier of the criterion this spec case specifies
behavior: string              # what the spec must observe, in a sentence
interface: string             # what the script declares: its exit codes, the fields it prints, or the event it binds
test_level: string            # optional; unit | script-contract | event-contract | runner
```

The field names match the other four frameworks so one caller can fill a uniform set: `script` is
this framework's unit field, where Drupal has `module` and Go has `package`. `interface` is the only
thing this reader gets about code that already exists, and it is a declaration rather than source.
Where it is empty, the behaviour must be observable from the script's documented exit codes and
output alone.

## Sequence

If invoked in dry-run mode, emit the level choice, the file path, the case labels and the assertions
planned, and write nothing. Dry-run is required.

1. **Confirm the component ships executable code.** If it does not — if the component is a skill, a
   command, an agent, or a hook's instruction half — stop and hand it to the paper trace in
   `claude-code-plugins/authoring-standards.md`. A paper trace is not a test and this recipe cannot
   make one.

2. **Select the level.** From `behavior` and what it reaches, using the table in Opinion. Use
   `test_level` if supplied.

3. **Place and name the file.** Under `<plugin>/tests/`, named for the topic it specifies and ending
   in `-spec.sh` for a shell spec. The `tests/` segment is load-bearing rather than tidy: the delete
   guard's globs are `**/tests/**`-prefixed, so a spec outside a `tests/` directory is not watched.

4. **Name the criterion in the case label.** Every assertion in a spec carries a label that is
   printed when it fails; the criterion identifier goes at the end of that label and nothing follows
   it — `bad decodes-header-c3 "..."`. The label is the whole mechanism here, because a shell spec
   has no runner-level selector: the file is the unit of execution, and a criterion is found by
   grepping the tests directory for its identifier. Put it in the section comment above the case as
   well, so the file reads as a specification and not only as a script.

5. **Write the spec.** Build fixtures under `mktemp -d`, with a `trap` that removes them on exit.
   Invoke the real script — not a copy of its logic — and assert on the exit code and on a parsed
   field of its output, never on prose. Count each case into a pass or fail counter. Finish by
   exiting non-zero when any case failed **and** when no case ran at all: a spec whose cases were all
   skipped exits 0 on the failure counter alone, which is the same defect the runner level exists to
   catch, in the spec itself.

6. **Watch it fail.** Run the spec and confirm the case fails on its assertion, and that the failure
   line names the criterion. A case that passes with no script behind it is rewritten once; if it
   still passes, stop and report it as proving nothing.

7. **Stop.** Return the level, the path, the case labels, the criterion each carries, and the failure
   output for each. Write no script under test.

## Data flow

Input: one criterion, the behaviour it names, the script's declared interface.
Output: one spec file under `<plugin>/tests/`, and for each case the criterion it carries and the
output of the run that failed.
Boundaries: reads no production script source; writes only under the plugin's tests directory; builds
every fixture under a temporary directory it removes; produces no task record of its own.

## State-awareness contract

Before writing a new spec, look for an existing spec that already covers the script, by searching the
plugin's tests directory for the criterion identifier and for the script's own name. Add a case to
the existing spec rather than starting a second file for the same script. A bug fix almost always
belongs on the existing case for the behaviour that broke.

Do not read the script's source to make that decision. The tests directory is readable; the script is
not.

## Verifier

- Each case carries its criterion identifier at the end of its printed label, so a failure line names
  the criterion.
- Each spec sits under a `tests/` directory inside the plugin and ends in `-spec.sh`, so the delete
  guard watches it.
- Each spec builds its fixtures under a temporary directory and removes them, and touches nothing
  outside it.
- Each spec exits non-zero when a case failed and when no case ran. A spec that can only report
  failures cannot report having done nothing.
- No spec uses `set -e`. A spec counts its failures and prints a summary, and `-e` aborts it at the
  first failing case, so the counters never print and the summary never appears. `set -uo pipefail`
  is the shape that survives a failing case.
- No spec asserts on a script's prose output. The exit code and any parsed field are contracts; the
  wording around them is not.
- No spec re-implements the script's logic to compare against itself. It invokes the real script.
- No script under test was written or changed.

## References

### Stack-neutral discipline (referenced, not authored here)

| Guide | What it holds |
|---|---|
| `development/tdd-spec-driven` | What a failing test proves, when not to write a test at all, the anti-patterns, and when a double is legitimate. Written for one person doing red, green and refactor; this reader does red and stops |

### Sibling process recipes

| Recipe | What it holds |
|---|---|
| `claude-code-plugins/test-execution.md` | That this framework ships no test harness, what the paper trace and the structural validator answer instead, and which framework answers for a component that ships executable code |
| `claude-code-plugins/authoring-standards.md` | The component contracts, the paper trace that stands in for a failing test where a component is only instructions, and the `## Oracle files` declaration that names the spec file patterns |

### External origins (referenced, not authored here)

| Origin | What it settled |
|---|---|
| The `camoa-skills` plugin marketplace on this machine | The observed spec shape — `set -uo pipefail`, fixtures under `mktemp -d` with a `trap`, pass and fail counters, one printed line per failure, the exit taken from the counters — and the four levels above, including a runner spec that starves a check's environment to prove a run that could not look does not report zero |
