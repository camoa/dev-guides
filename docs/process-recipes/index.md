---
description: Process recipes — framework-specific drivers for one lifecycle phase, resolved by an orchestrator by (phase × framework), never matched during free task routing.
---

# Process Recipes

> A **separate class** from [agentic (task) recipes](../agentic-recipes/index.md) and from [guides](../drupal/index.md). A **process recipe** is a framework-specific *driver* for **one phase of the development lifecycle** — e2e setup, visual-regression setup, contrib research. The plugin owns the **generic, stack-neutral mechanism**; the recipe owns the **framework-specific how**.

Process recipes are **resolved by an orchestrator**, keyed by **`(phase × framework)`**, at a lifecycle moment — they are **never** matched by capability during free task work, where they would pollute context. That is why they publish to their **own** index, `process-recipes.txt` (separate from `llms.txt` and `agentic-recipes.txt`), and live under their **own** docs root, `docs/process-recipes/`.

## Routing table

| Phase | Framework | Recipe | When to use |
|---|---|---|---|
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

> **`claude-code-plugins` binds only four phases.** A Claude Code plugin has no rendered or behavioural runtime surface, so this framework declares **no `e2e-setup` or `visual-regression` recipe**. Do not run `/setup-e2e` or `/setup-visual-regression` on a plugin project — the loader correctly returns no recipe, but those commands' generic fallback would still try to scaffold a Playwright harness that does not apply.

> **`php-cli` binds only four phases.** A PHP CLI tool has no rendered or behavioural runtime surface, so this framework declares **no `e2e-setup` or `visual-regression` recipe**. Do not run `/setup-e2e` or `/setup-visual-regression` on a PHP CLI project — the loader correctly returns no recipe, but those commands' generic fallback would still try to scaffold a Playwright harness that does not apply. "No e2e" means no *browser* e2e: a CLI tool's end-to-end shape — run the built binary against a fixture tree and assert on output and exit code — lives in the `implement` and `review` recipes as a test tier, not as an `e2e-setup` binding.

> **`go` binds only four phases, and declares no change-impact globs.** A Go module has no rendered or browser surface, so this framework declares **no `e2e-setup` or `visual-regression` recipe** — and, because change-impact globs exist to route a changed file to exactly those two gates, the review recipe deliberately declares none. A Go CLI's end-to-end shape is a test tier, not a phase: it lives in the `implement` recipe as the entry-point tier (calling `run(ctx, args, stdin, stdout, stderr) error` with buffers) and the subprocess tier (for the exit status, signals, and a real stdin pipe), and is checked under the test gate at `review`. The `review` recipe **does** declare `## Code-quality extensions`, and that one is load-bearing rather than optional: no Go extension is in the framework-neutral change-scoping floor, so without it a pure-Go change filters to an empty file list and every change-scoped gate skips itself — a clean-looking run that examined nothing.

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
