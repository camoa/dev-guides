---
description: Process recipes — framework-specific drivers for one lifecycle phase, resolved by an orchestrator by (phase × framework), never matched during free task routing.
---

# Process Recipes

> A **separate class** from [agentic (task) recipes](../agentic-recipes/index.md) and from [guides](../drupal/index.md). A **process recipe** is a framework-specific *driver* for **one phase of the development lifecycle** — e2e setup, visual-regression setup, contrib research. The plugin owns the **generic, stack-neutral mechanism**; the recipe owns the **framework-specific how**.

Process recipes are **resolved by an orchestrator**, keyed by **`(phase × framework)`**, at a lifecycle moment — they are **never** matched by capability during free task work, where they would pollute context. That is why they publish to their **own** index, `process-recipes.txt` (separate from `llms.txt` and `agentic-recipes.txt`), and live under their **own** docs root, `docs/process-recipes/`.

## Routing table

| Phase | Framework | Recipe | When to use |
|---|---|---|---|
| `research` | `drupal` | [Prior-art research](drupal/contrib-prior-art.md) | A Drupal project must establish prior art — first in its own custom code and exported configuration, then on drupal.org and in contrib by usage, maintenance, security coverage and core-version fit — before any custom build. |
| `design` | `drupal` | [Design](drupal/architecture.md) | Turning researched requirements into a service-based architecture — business logic in injected services, a Drush entry point, and the form / entity / plugin pattern per component. |
| `implement` | `drupal` | [Coding standards and test discipline](drupal/standards-and-tests.md) | Holding Drupal code to coding standards and the implementation-time security rules, with the PHPUnit tier selected per unit of logic and each test shaped Red-Green-Refactor. |
| `test-execution` | `drupal` | [Test execution](drupal/test-execution.md) | Running a Drupal test at any scope — the suite, one file, one case, the tests covering a change, or the cheapest thing that proves the runner works — with the tier's cost and how to read what came back. |
| `review` | `drupal` | [Implementation review checks](drupal/checks.md) | Validating a Drupal implementation against its architecture and Drupal security — static `\Drupal::` in new code, logic in forms/controllers, Form API CSRF — before acceptance. |
| `e2e-setup` | `drupal` | [ATK end-to-end test setup](drupal/e2e-setup-atk.md) | A Drupal project (DDEV + Playwright) needs a behavioural E2E harness. |
| `visual-regression` | `drupal` | [Visual-regression setup](drupal/visual-regression-setup.md) | A Drupal project needs visual-regression coverage with deterministic baselines. |
| `research` | `claude-code-plugins` | [Plugin prior-art research](claude-code-plugins/prior-art.md) | A Claude Code plugin project must establish prior art (reuse / extend / build-new) before scaffolding a component. |
| `design` | `claude-code-plugins` | [Design](claude-code-plugins/architecture.md) | Turning a researched need into a component map — type choice, progressive disclosure, manifest + boundary. |
| `implement` | `claude-code-plugins` | [Component authoring standards](claude-code-plugins/authoring-standards.md) | Authoring skills / commands / agents / hooks to contract, with paper-test as the test-first gate. |
| `test-execution` | `claude-code-plugins` | [Test execution](claude-code-plugins/test-execution.md) | Establishing that this framework has no test harness, what the paper-test and the structural validator answer instead, and which framework answers for a component that ships executable code. |
| `review` | `claude-code-plugins` | [Plugin review checks](claude-code-plugins/checks.md) | Validating a plugin (structural + semantic) before acceptance, routing each check to its owning tool. |
| `research` | `php-cli` | [PHP CLI prior-art research](php-cli/prior-art.md) | A PHP CLI project (a Composer library/app whose interface is one or more binaries) must establish prior art (reuse / extend / build-new) before building — Packagist is dense. |
| `design` | `php-cli` | [Design](php-cli/architecture.md) | Turning a researched need into a library-first architecture — the library/CLI boundary, the entrypoint contract (exit codes, stream split, machine-readable output), and the dependency posture. |
| `implement` | `php-cli` | [PHP CLI standards and tests](php-cli/standards-and-tests.md) | Holding PHP code to PSR-12 / `strict_types` and test-first discipline, with fixture-driven CLI end-to-end coverage and the extensionless-binary syntax check. |
| `test-execution` | `php-cli` | [Test execution](php-cli/test-execution.md) | Running a PHP CLI project's tests at any scope, with the PHPUnit filter and exit-code traps that make a run mean something other than what it reads as. |
| `review` | `php-cli` | [PHP CLI review checks](php-cli/checks.md) | Validating a PHP CLI implementation (boundary, exit-code contract, dependency policy, security sinks, every binary linted) before acceptance. |
| `research` | `go` | [Go prior-art research](go/prior-art.md) | A Go project must decide whether a capability needs a dependency at all — standard library first, then transitive depth, deprecation and reachable-vulnerability evidence per candidate. |
| `design` | `go` | [Design](go/architecture.md) | Turning researched requirements into a package layout whose boundary the compiler enforces — `internal/` by default, `cmd/` as a shim, the module path and its compatibility promise, consumer-side interfaces, context and the exported error surface. |
| `implement` | `go` | [Go standards and tests](go/standards-and-tests.md) | Holding Go code to `gofmt` and test-first discipline, with table-driven subtests, `testdata/` goldens, `t.Parallel()` constraints, `-race` in the ordinary test command, and the map-iteration and unstable-sort ordering traps. |
| `test-execution` | `go` | [Test execution](go/test-execution.md) | Running a Go module's tests at any scope, with the `-run` over-selection trap, the silent zero-exit cases, and the marker that separates a failed assertion from a package that never compiled. |
| `review` | `go` | [Go review checks](go/checks.md) | Validating a Go change against its architecture and the toolchain gates — including the three gates commonly written in a form that can never fail — before acceptance. |
| `research` | `python-cli` | [Python prior-art research](python-cli/prior-art.md) | A Python project must establish what already exists before anything is written — the standard library first, then PyPI, with each candidate judged on maintenance, typing, dependency weight, licence, yanked status and a pre-adoption vulnerability audit rather than on stars. |
| `design` | `python-cli` | [Design](python-cli/architecture.md) | Turning researched requirements into a library-first architecture with a thin console script — the package boundary, a named programmatic entry point per capability, the entrypoint contract (exit codes, stream split, machine-readable output), protocol seams, and the dependency and typing postures. |
| `implement` | `python-cli` | [Python implementation standards and tests](python-cli/standards-and-tests.md) | Holding Python code to the project's formatting, linting and typing standards with test-first discipline — tests that import the package rather than shelling out, one exception type per failure class, and the import-time, mutable-default and shell-injection traps. |
| `test-execution` | `python-cli` | [Test execution](python-cli/test-execution.md) | Running a Python project's tests at any scope through the runner the project declares, with the node-identifier form and the exit codes that separate a failed assertion from a collection that never happened. |
| `review` | `python-cli` | [Python review checks](python-cli/checks.md) | Validating a Python change against its architecture and the toolchain gates in a blocking order, plus the conformance reads a linter structurally cannot make, before acceptance. |

> **`claude-code-plugins` binds five phases.** A Claude Code plugin has no rendered or behavioural runtime surface, so this framework declares **no `e2e-setup` or `visual-regression` recipe**. Do not run `/setup-e2e` or `/setup-visual-regression` on a plugin project — the loader correctly returns no recipe, but those commands' generic fallback would still try to scaffold a Playwright harness that does not apply.

> **`php-cli` binds five phases.** A PHP CLI tool has no rendered or behavioural runtime surface, so this framework declares **no `e2e-setup` or `visual-regression` recipe**. Do not run `/setup-e2e` or `/setup-visual-regression` on a PHP CLI project — the loader correctly returns no recipe, but those commands' generic fallback would still try to scaffold a Playwright harness that does not apply. "No e2e" means no *browser* e2e: a CLI tool's end-to-end shape — run the built binary against a fixture tree and assert on output and exit code — lives in the `implement` and `review` recipes as a test tier, not as an `e2e-setup` binding.

> **`go` binds five phases, and declares no change-impact globs.** A Go module has no rendered or browser surface, so this framework declares **no `e2e-setup` or `visual-regression` recipe** — and, because change-impact globs exist to route a changed file to exactly those two gates, the review recipe deliberately declares none. A Go CLI's end-to-end shape is a test tier, not a phase: it lives in the `implement` recipe as the entry-point tier (calling `run(ctx, args, stdin, stdout, stderr) error` with buffers) and the subprocess tier (for the exit status, signals, and a real stdin pipe), and is checked under the test gate at `review`. The `review` recipe **does** declare `## Code-quality extensions`, and that one is load-bearing rather than optional: no Go extension is in the framework-neutral change-scoping floor, so without it a pure-Go change filters to an empty file list and every change-scoped gate skips itself — a clean-looking run that examined nothing.

> **`python-cli` binds five phases, and declares no change-impact globs.** A Python library or console-script tool has no rendered or browser surface, so this framework declares **no `e2e-setup` or `visual-regression` recipe** — and, because change-impact globs exist to route a changed file to exactly those two gates, the review recipe deliberately declares none. A CLI's end-to-end shape is a test tier, not a phase: it lives in the `implement` recipe as the entry-point tier the tests import, and is checked under the test gate at `review`. The `review` recipe **does** declare `## Code-quality extensions`, and that one is load-bearing rather than optional: no Python extension is in the framework-neutral change-scoping floor, so without it a pure-Python change filters to an empty file list and every change-scoped gate skips itself. It declares `.py`, `.pyi` (a stub is the declared public typing surface, not dead text) and `.toml` — the last one deliberately, because a change that touches only `pyproject.toml` carries the dependency and version decisions this framework blocks on. The machine-checkable `## Preconditions` for running a test — the manifest, the interpreter and the runner in the project's own environment — are declared by the `test-execution` recipe, alongside the commands they are conditions of.

## What each phase type is for

The authoring rules below specify a recipe's **form**. This section specifies its **job** — what a
recipe of each type must decide, and what belongs to a different type. Read it before authoring a set
for a new framework, because the form is identical across every one of them and the form alone will not stop you
putting review's content in implement, or putting something in a recipe that should not be in one.

**The invariant that governs every type.** The plugin owns the mechanism and the gate; the recipe owns
only what is genuinely specific to its stack, and **references** canonical sources rather than restating
them. A recipe ships no code assets. Two tests before anything goes in a recipe:

- *Would this sentence be identical for another stack?* Then it is not framework knowledge, and it
  belongs in a guide the recipe cites — not copied into each framework's recipe. A rule restated once per
  stack has no single place to correct it, and nothing detects the copies diverging.
- *Does this run something, or record a result?* Then it is the plugin's. The recipe supplies the method
  the gate evaluates; it does not own the gate.

| Type | Its job | Not its job |
|---|---|---|
| `research` | Establish what already exists, in the project's own code and configuration first and then in the ecosystem, and return **named** candidates with the evidence behind each, ordered by closeness. | Returning a verdict. The reuse-or-build call belongs to the stage that decides the architecture, and a recipe that returns one is one edit away from a recipe that decides. Judging code that does not exist yet. |
| `design` | Turn researched requirements into structure — where business logic lives, the programmatic entry point, which of the stack's patterns each component takes, and the boundary the language or framework enforces. Return the units to build and the order to build them in; the caller records them, and there is no architecture document. | Coding standards. Test tiers. Anything about how the code will be written. |
| `implement` | The rules applied **while** code is written: coding standards, the implementation-time security guarantees, test-tier selection, and the test-first cycle. This is where a stack's best practices live. | Running linters — the recipe judges what a standard means, the tooling runs it. Post-hoc validation. |
| `test-authoring` | Where a test goes, what shape it takes, and how it is traced to the criterion it specifies. Read by the context that writes tests and cannot read production source. | Running the test. Writing the code that passes it. |
| `test-execution` | The command that runs a test at each scope a caller asks for, its cost, and how to read what came back. Its several readers are the reason it is its own file: the failing-test step, the baseline, each build check, and the fixer all ask the same question at different moments. | Deciding what to test, or judging the result. It returns a command and the means to read the output; it runs nothing. |
| `protected-tests` | Which files are tests, and what may change them. Read by a rule rather than by a model. | Judging a test's content. Deciding whether a change is warranted. |
| `build-checks` | The checks a script runs after code is written and before anything judges it, in the stack's own terms. | The blocking acceptance validations — those are `review`'s, and the difference is when they run, not what they run. |
| `review` | The **blocking** validations run before work is accepted, in the stack's own terms, in a deliberate order. | Restating the generic review. Re-authoring checks `implement` already applied inline. |
| `e2e-setup` | One-time wiring of a behavioural harness into the gate the plugin already owns — install, scaffold, bind authenticated journeys. | Running the suite. Deciding what to test. |
| `visual-regression` | One-time wiring of surface discovery, the viewport matrix and baseline capture into the plugin's baseline-and-gate mechanism. | Capturing or approving baselines on an ongoing basis. |

**Three of these phases are named and not yet written.** `test-authoring`, `protected-tests` and
`build-checks` have their names and their jobs above, and no recipe files. They are named together
and ahead of their content deliberately: a name becomes a contract the moment anything resolves
against it, and picking them one at a time from inside a single step produces a set that does not
fit together. Until each one's content lands, the material stays where it is — the test-first cycle
and the tier selection under `implement`, the test-file list under `## Oracle files`.

**`## Oracle files` will need one producer, not two.** It answers "which files here are tests", which
the context that writes a test and the rule that stops a builder writing one both need. A phase
resolves one recipe per framework, so whichever file holds it, the other reader cannot resolve it.
The brief that moves it has to answer that; recorded here because the split is what creates it.

**Not every framework binds every type.** A stack with no rendered or browser surface declares no
`e2e-setup` and no `visual-regression` recipe, and that is a complete set, not a gap — see the
per-framework notes above the authoring rules. A CLI's end-to-end shape is a **test tier** inside
`implement`, checked under `review`, never a phase of its own.

**`implement` owns the TDD loop; `e2e-setup` and `visual-regression` do not.** The tests an
`implement` recipe selects a tier for are written before the code and run red then green, where the
red comes from a behaviour that does not exist yet rather than from code broken to force it — they
constrain a design that does not exist yet. The suites the other two phases wire up run against
something already built, cannot drive a design decision, and are therefore outer verification. The
line is not whether a browser or a subprocess is involved: Drupal's `FunctionalJavascript` tier
drives a real browser and belongs to `implement`, and a CLI's fixture-driven end-to-end tier spawns a
process and belongs there too. What follows for an `implement` recipe is that e2e or visual-regression
coverage never substitutes for a tier it must choose, and is reported separately rather than counted
toward its test-first requirement. The stack-neutral statement of this, and of what makes an added
test excess rather than coverage, lives in
[development/tdd-spec-driven](https://camoa.github.io/dev-guides/development/tdd-spec-driven/) and is
cited by each `implement` recipe rather than restated in it.

### What each type may declare

Five types carry machine-readable declarations. `research` and `design` carry none — they are prose
method, consumed by an agent, not parsed by a script. What the three unwritten phases declare is
decided with their content, not here.

| Type | Declaration (exact heading) | Posture |
|---|---|---|
| `implement` | `## Oracle files`, `## Routing hints`, `## Preconditions` | fail-open (`## Preconditions` fails closed) |
| `test-execution` | `## Test commands`, `## Preconditions` | **fail-closed** (both) |
| `review` | `## Change-impact globs`, `## Code-quality extensions` | fail-open |
| `visual-regression` | `## Change-impact globs`, `## Screenshot capture` | fail-open |
| `e2e-setup` | `e2e.preflight_command` (a YAML key in the registry seed) | **fail-closed** |

Spelling is load-bearing. A fail-open declaration with a misspelled heading does not error — it silently
degrades to the neutral floor, and the run looks clean while checking less than you think.

**`## Test commands` is parsed, and it fails closed.** A `test-execution` recipe declares five rows —
`suite`, `file`, `test`, `changed`, `smoke` — and each is either a command or a named statement that
this framework has none. Absent is an answer; a row nobody wrote is not, which is why the set is
fixed and `scripts/validate_recipes.py` rejects a recipe missing one. A command is a list of argv
tokens, never a shell string, and a token that is exactly a `{placeholder}` is substituted whole —
the same rule `check:` lives under, for the same reason. Each command carries a `cost:` of
`every-attempt` or `end-of-task`, because a caller without one either runs the cheapest thing and
under-checks or runs everything on every attempt. Alongside the rows, `failure_signal:` says how to
tell a failed assertion from a harness that never reached the behaviour, in that harness's own
output — the frameworks differ sharply here, and two of them report a selector that matched nothing
as a success.

Both blocks are plain YAML in the body, introduced by a line that is exactly the key. A fenced
```yaml block reads the same to the parser and renders as a code block rather than as one collapsed
paragraph, so fence anything longer than a few lines.

**The `preconditions:` entries are parsed too, as of this change.** The block has looked structured
since it was written and, until now, nothing read it, so a misspelled `check:`, `owner:` or `id:`
degraded in silence. The validator checks the entry keys and rejects an unknown one. Where nothing
owns an entry, say so — `owner: operator` for a toolchain the machine's owner installs — so that an
entry nobody owns and an entry whose owner was forgotten stop looking the same.

**A check may assert on what it printed, with `expect:`.** A `check:` is decided by its exit status,
and some commands answer in their output instead: `ddev describe -j` reports whether a project is
running and exits 0 either way. Where that is the case, the entry adds an optional `expect:` beside
its `check:`.

```yaml
preconditions:
  - id: test-runner
    what: a running DDEV environment, so the runner the project documents can be reached at all
    check: ddev describe -j
    expect: '"status_desc":"running"'
    owner: code-quality-tools:setup
```

The exit status is still read first and keeps every meaning it has: a command that is not found says
nothing about the condition, and any other non-zero exit is a condition that answered no. Only on a
zero exit does `expect:` decide, and it decides one way — the literal string appears in what the
command wrote to standard output, or the condition answered no. It is a substring test and nothing
more: no regular expression, no glob, no path into a document, no shell, for the same reason the
command itself never reaches one. Choose the string so that its **presence** is the answer, because
a JSON document reporting several things at once usually contains the string you meant to rule out —
and test it against every state the command can report, not just the two obvious ones. The example
above uses `status_desc` rather than `status` for exactly that reason: `status` appears once per
service, so a paused project still prints `"status":"running"` for whatever stayed up. An entry with
no `expect:` is decided exactly as before, so nothing that already works changes.

**`## Oracle files` is parsed, not just read.** As of 2026-09-01 a consumer takes the `globs` off the
row whose `type` is `test_delete` to answer "which files in this repository are tests", instead of
trusting a list the caller supplied. Three things are therefore load-bearing inside that section and
are enforced by `scripts/validate_recipes.py`: the first ```json fence under the H2 must parse as a
top-level array of flat objects; every row must carry exactly `type`, `globs`, `changes`,
`oracle_class`, `severity`; and `test_delete` must appear at most once, because it is the selector.
The markdown table above the fence and the fence itself state the same rules, and the validator now
checks that they agree — before it did not, so the table a person reads could drift away from the
rules a machine applies. When restructuring this section, keep a `test_delete` row resolvable from
the recipe's own body: a row present only by inheritance is invisible to anything reading the
published page. Where a stack
has no extension in the framework-neutral change-scoping floor, `## Code-quality extensions` stops being
optional: without it every change-scoped gate filters to an empty file list and skips itself.

## Authoring a process recipe

A process recipe is authored to the **same `recipe_schema_version 1.0.0` standard** as a task recipe — same validator, same required sections. It differs only in **where it lives** and **three routing keys**. `scripts/validate_recipes.py` enforces all of this (it scans both recipe roots).

**1. Location is the class.** Put the file at `docs/process-recipes/<domain>/<name>.md` (e.g. `docs/process-recipes/drupal/e2e-setup-atk.md`). The first path segment is the domain. Anything under this root is a process recipe; nothing else is. This is what keeps process recipes out of the task index — the task generator never scans here.

**2. Routing-first frontmatter** (first three keys, in order):

```yaml
name: drupal_e2e_setup_atk        # globally unique, snake_case
capability: e2e-setup             # the PHASE — capability IS the lifecycle phase
description: Use when …           # single-line when-to-use trigger
```

**3. Required metadata** + the process routing keys:

```yaml
label: ATK end-to-end test setup (Drupal)
recipe_schema_version: 1.0.0
version: 0.1.0
recipe_class: process             # required; self-declares the class
framework: drupal                 # required; the 2nd half of the resolution key
```

- **`capability` doubles as the phase.** There is no separate `applies_to_phase`. (If you add one, it must equal `capability`, or validation fails.)
- Any other keys (`drupal_compatibility`, `requires_modules`, `assumes`, `authors`, `license`, …) are free-form — the validator ignores them.

**4. Required body sections** (same nine as every recipe): `Goal`, `Opinion`, `Preconditions`, `Input contract`, `Sequence`, `Data flow`, `State-awareness contract`, `Verifier`, `References`.

**5. Declare the tooling your method needs.** A process recipe knows which tools its method requires; the caller does not. It knows it wants a standards check, not that a Drupal standards check means `phpcs`. Declare them by tool name, and the caller resolves each one against the tooling index rather than guessing what a framework's method runs:

```yaml
requires_tooling:                 # optional; tool names, resolved for THIS recipe's framework
  - phpcs
  - phpstan
```

The name is the whole contract — a tooling recipe is named for its tool, and whatever needs the tool refers to it by that name. `scripts/validate_recipes.py` checks that each declared name resolves to a real tooling recipe for the recipe's own framework, so a name that resolves to nothing fails when the recipe is published rather than when somebody runs it. The key is optional and checked only when present, so a recipe whose framework has no tooling recipes yet stays valid.

**6. Reference origin; do not ship code assets.** A process recipe carries the framework-specific *binding* as prose and **references** canonical sources (module docs, Playwright, etc.) — it does not bake in `.ts`/`.sh` files. The plugin owns the generic machinery; the recipe binds the framework into it.

### What the build produces

On deploy, `scripts/generate_process_recipes.py` emits one routing line per recipe into `process-recipes.txt`, plus `process-recipes.hash`:

```
- <name> [phase=<phase> framework=<framework>] (sha:XXXXXXXX): <when-to-use> — <site-url>
```

The orchestrator matches on `(phase, framework)` without fetching the body; the per-recipe `(sha:XXXXXXXX)` gates the body cache; the body is fetched as raw markdown from the site-url.
