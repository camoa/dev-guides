---
description: Process recipes — framework-specific drivers for one lifecycle phase, resolved by an orchestrator by (phase × framework), never matched during free task routing.
---

# Process Recipes

> A **separate class** from [agentic (task) recipes](../agentic-recipes/index.md) and from [guides](../drupal/index.md). A **process recipe** is a framework-specific *driver* for **one phase of the development lifecycle** — e2e setup, visual-regression setup, contrib research. The plugin owns the **generic, stack-neutral mechanism**; the recipe owns the **framework-specific how**.

Process recipes are **resolved by an orchestrator**, keyed by **`(phase × framework)`**, at a lifecycle moment — they are **never** matched by capability during free task work, where they would pollute context. That is why they publish to their **own** index, `process-recipes.txt` (separate from `llms.txt` and `agentic-recipes.txt`), and live under their **own** docs root, `docs/process-recipes/`.

## Routing table

| Phase | Framework | Recipe | When to use |
|---|---|---|---|
| `research` | `drupal` | [Contrib prior-art research](drupal/contrib-prior-art.md) | A Drupal project must establish prior art on drupal.org and in contrib — usage, maintenance, security coverage and core-version fit — before any custom build. |
| `design` | `drupal` | [Service-based architecture design](drupal/architecture.md) | Turning researched requirements into a service-based architecture — business logic in injected services, a Drush entry point, and the form / entity / plugin pattern per component. |
| `implement` | `drupal` | [Coding standards and test discipline](drupal/standards-and-tests.md) | Holding Drupal code to coding standards and the implementation-time security rules, with the PHPUnit tier selected per unit of logic and each test shaped Red-Green-Refactor. |
| `review` | `drupal` | [Implementation review checks](drupal/checks.md) | Validating a Drupal implementation against its architecture and Drupal security — static `\Drupal::` in new code, logic in forms/controllers, Form API CSRF — before acceptance. |
| `e2e-setup` | `drupal` | [ATK end-to-end test setup](drupal/e2e-setup-atk.md) | A Drupal project (DDEV + Playwright) needs a behavioural E2E harness. |
| `visual-regression` | `drupal` | [Visual-regression setup](drupal/visual-regression-setup.md) | A Drupal project needs visual-regression coverage with deterministic baselines. |
| `research` | `claude-code-plugins` | [Plugin prior-art research](claude-code-plugins/prior-art.md) | A Claude Code plugin project must establish prior art (reuse / extend / build-new) before scaffolding a component. |
| `design` | `claude-code-plugins` | [Plugin component architecture](claude-code-plugins/architecture.md) | Turning a researched need into a component map — type choice, progressive disclosure, manifest + boundary. |
| `implement` | `claude-code-plugins` | [Component authoring standards](claude-code-plugins/authoring-standards.md) | Authoring skills / commands / agents / hooks to contract, with paper-test as the test-first gate. |
| `review` | `claude-code-plugins` | [Plugin review checks](claude-code-plugins/checks.md) | Validating a plugin (structural + semantic) before acceptance, routing each check to its owning tool. |
| `research` | `php-cli` | [PHP CLI prior-art research](php-cli/prior-art.md) | A PHP CLI project (a Composer library/app whose interface is one or more binaries) must establish prior art (reuse / extend / build-new) before building — Packagist is dense. |
| `design` | `php-cli` | [PHP CLI architecture](php-cli/architecture.md) | Turning a researched need into a library-first architecture — the library/CLI boundary, the entrypoint contract (exit codes, stream split, machine-readable output), and the dependency posture. |
| `implement` | `php-cli` | [PHP CLI standards and tests](php-cli/standards-and-tests.md) | Holding PHP code to PSR-12 / `strict_types` and test-first discipline, with fixture-driven CLI end-to-end coverage and the extensionless-binary syntax check. |
| `review` | `php-cli` | [PHP CLI review checks](php-cli/checks.md) | Validating a PHP CLI implementation (boundary, exit-code contract, dependency policy, security sinks, every binary linted) before acceptance. |
| `research` | `go` | [Go prior-art research](go/prior-art.md) | A Go project must decide whether a capability needs a dependency at all — standard library first, then transitive depth, deprecation and reachable-vulnerability evidence per candidate. |
| `design` | `go` | [Go architecture](go/architecture.md) | Turning researched requirements into a package layout whose boundary the compiler enforces — `internal/` by default, `cmd/` as a shim, the module path and its compatibility promise, consumer-side interfaces, context and the exported error surface. |
| `implement` | `go` | [Go standards and tests](go/standards-and-tests.md) | Holding Go code to `gofmt` and test-first discipline, with table-driven subtests, `testdata/` goldens, `t.Parallel()` constraints, `-race` in the ordinary test command, and the map-iteration and unstable-sort ordering traps. |
| `review` | `go` | [Go review checks](go/checks.md) | Validating a Go change against its architecture and the toolchain gates — including the three gates commonly written in a form that can never fail — before acceptance. |
| `research` | `python-cli` | [Python prior-art research](python-cli/prior-art.md) | A Python project must establish what already exists before anything is written — the standard library first, then PyPI, with each candidate judged on maintenance, typing, dependency weight, licence, yanked status and a pre-adoption vulnerability audit rather than on stars. |
| `design` | `python-cli` | [Python CLI architecture](python-cli/architecture.md) | Turning researched requirements into a library-first architecture with a thin console script — the package boundary, a named programmatic entry point per capability, the entrypoint contract (exit codes, stream split, machine-readable output), protocol seams, and the dependency and typing postures. |
| `implement` | `python-cli` | [Python implementation standards and tests](python-cli/standards-and-tests.md) | Holding Python code to the project's formatting, linting and typing standards with test-first discipline — tests that import the package rather than shelling out, one exception type per failure class, and the import-time, mutable-default and shell-injection traps. |
| `review` | `python-cli` | [Python review checks](python-cli/checks.md) | Validating a Python change against its architecture and the toolchain gates in a blocking order, plus the conformance reads a linter structurally cannot make, before acceptance. |

> **`claude-code-plugins` binds only four phases.** A Claude Code plugin has no rendered or behavioural runtime surface, so this framework declares **no `e2e-setup` or `visual-regression` recipe**. Do not run `/setup-e2e` or `/setup-visual-regression` on a plugin project — the loader correctly returns no recipe, but those commands' generic fallback would still try to scaffold a Playwright harness that does not apply.

> **`php-cli` binds only four phases.** A PHP CLI tool has no rendered or behavioural runtime surface, so this framework declares **no `e2e-setup` or `visual-regression` recipe**. Do not run `/setup-e2e` or `/setup-visual-regression` on a PHP CLI project — the loader correctly returns no recipe, but those commands' generic fallback would still try to scaffold a Playwright harness that does not apply. "No e2e" means no *browser* e2e: a CLI tool's end-to-end shape — run the built binary against a fixture tree and assert on output and exit code — lives in the `implement` and `review` recipes as a test tier, not as an `e2e-setup` binding.

> **`go` binds only four phases, and declares no change-impact globs.** A Go module has no rendered or browser surface, so this framework declares **no `e2e-setup` or `visual-regression` recipe** — and, because change-impact globs exist to route a changed file to exactly those two gates, the review recipe deliberately declares none. A Go CLI's end-to-end shape is a test tier, not a phase: it lives in the `implement` recipe as the entry-point tier (calling `run(ctx, args, stdin, stdout, stderr) error` with buffers) and the subprocess tier (for the exit status, signals, and a real stdin pipe), and is checked under the test gate at `review`. The `review` recipe **does** declare `## Code-quality extensions`, and that one is load-bearing rather than optional: no Go extension is in the framework-neutral change-scoping floor, so without it a pure-Go change filters to an empty file list and every change-scoped gate skips itself — a clean-looking run that examined nothing.

> **`python-cli` binds only four phases, and declares no change-impact globs.** A Python library or console-script tool has no rendered or browser surface, so this framework declares **no `e2e-setup` or `visual-regression` recipe** — and, because change-impact globs exist to route a changed file to exactly those two gates, the review recipe deliberately declares none. A CLI's end-to-end shape is a test tier, not a phase: it lives in the `implement` recipe as the entry-point tier the tests import, and is checked under the test gate at `review`. The `review` recipe **does** declare `## Code-quality extensions`, and that one is load-bearing rather than optional: no Python extension is in the framework-neutral change-scoping floor, so without it a pure-Python change filters to an empty file list and every change-scoped gate skips itself. It declares `.py`, `.pyi` (a stub is the declared public typing surface, not dead text) and `.toml` — the last one deliberately, because a change that touches only `pyproject.toml` carries the dependency and version decisions this framework blocks on. The `implement` recipe declares machine-checkable `## Preconditions`, which is the one declaration that fails closed.

## What each phase type is for

The authoring rules below specify a recipe's **form**. This section specifies its **job** — what a
recipe of each type must decide, and what belongs to a different type. Read it before authoring a set
for a new framework, because the form is identical across all six and the form alone will not stop you
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
| `research` | Establish what already exists, in the ecosystem and in the project, and return **named** candidates with a reuse / extend / build-new verdict and the evidence behind it. | Choosing the architecture. Judging code that does not exist yet. |
| `design` | Turn researched requirements into structure — where business logic lives, the programmatic entry point, which of the stack's patterns each component takes, and the boundary the language or framework enforces. | Coding standards. Test tiers. Anything about how the code will be written. |
| `implement` | The rules applied **while** code is written: coding standards, the implementation-time security guarantees, test-tier selection, and the test-first cycle. This is where a stack's best practices live. | Running linters — the recipe judges what a standard means, the tooling runs it. Post-hoc validation. |
| `review` | The **blocking** validations run before work is accepted, in the stack's own terms, in a deliberate order. | Restating the generic review. Re-authoring checks `implement` already applied inline. |
| `e2e-setup` | One-time wiring of a behavioural harness into the gate the plugin already owns — install, scaffold, bind authenticated journeys. | Running the suite. Deciding what to test. |
| `visual-regression` | One-time wiring of surface discovery, the viewport matrix and baseline capture into the plugin's baseline-and-gate mechanism. | Capturing or approving baselines on an ongoing basis. |

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

Only four of the six types carry machine-readable declarations at all. `research` and `design` carry
none — they are prose method, consumed by an agent, not parsed by a script.

| Type | Declaration (exact heading) | Posture |
|---|---|---|
| `implement` | `## Oracle files`, `## Routing hints`, `## Preconditions` | fail-open (`## Preconditions` fails closed) |
| `review` | `## Change-impact globs`, `## Code-quality extensions` | fail-open |
| `visual-regression` | `## Change-impact globs`, `## Screenshot capture` | fail-open |
| `e2e-setup` | `e2e.preflight_command` (a YAML key in the registry seed) | **fail-closed** |

Spelling is load-bearing. A fail-open declaration with a misspelled heading does not error — it silently
degrades to the neutral floor, and the run looks clean while checking less than you think.

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

**5. Reference origin; do not ship code assets.** A process recipe carries the framework-specific *binding* as prose and **references** canonical sources (module docs, Playwright, etc.) — it does not bake in `.ts`/`.sh` files. The plugin owns the generic machinery; the recipe binds the framework into it.

### What the build produces

On deploy, `scripts/generate_process_recipes.py` emits one routing line per recipe into `process-recipes.txt`, plus `process-recipes.hash`:

```
- <name> [phase=<phase> framework=<framework>] (sha:XXXXXXXX): <when-to-use> — <site-url>
```

The orchestrator matches on `(phase, framework)` without fetching the body; the per-recipe `(sha:XXXXXXXX)` gates the body cache; the body is fetched as raw markdown from the site-url.
