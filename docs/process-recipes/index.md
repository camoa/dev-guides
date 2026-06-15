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

> **`claude-code-plugins` binds only four phases.** A Claude Code plugin has no rendered or behavioural runtime surface, so this framework declares **no `e2e-setup` or `visual-regression` recipe**. Do not run `/setup-e2e` or `/setup-visual-regression` on a plugin project — the loader correctly returns no recipe, but those commands' generic fallback would still try to scaffold a Playwright harness that does not apply.

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
