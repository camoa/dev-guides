---
# Routing block — an orchestrator reads to here and decides.
name: drupal_design_architecture
capability: design
description: Use when a Drupal project enters the design phase and must turn researched requirements into a service-based architecture — places business logic in injected services, defines a Drush entry point, selects the form / entity / plugin pattern for each component, and grounds every choice in a canonical Drupal core example before any code is written.
# Metadata — read only after a match.
label: Service-based architecture design (Drupal)
recipe_schema_version: 1.0.0
version: 0.1.0
# Machine-readable dependency declaration (recipe-loader resolves these without parsing prose).
requires_guides:
  - drupal/services
  - drupal/forms
  - drupal/entities
  - drupal/config-management
# Process-recipe routing keys, enforced by validate_recipes.py for any recipe
# under docs/process-recipes/. `capability` above doubles as the phase (the
# lifecycle moment the orchestrator resolves on); there is no separate
# applies_to_phase. `framework` is the second routing dimension.
recipe_class: process
framework: drupal
drupal_compatibility: "^10.3 || ^11"
assumes:
  - composer
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Turn researched requirements into a Drupal architecture decision before any code is written: business logic placed in services that are registered in a `*.services.yml` file with their dependencies injected, a Drush command entry point for every feature, the right pattern chosen for each form / storage / plugin component, and each choice grounded in a canonical Drupal core example.

The plugin owns the generic mechanism — when the design phase runs, the shape of the architecture artifact, the mandatory architecture checklist that gates Phase 3, and how the decision is recorded and reviewed. This recipe owns the part the stack-neutral mechanism cannot know: how a Drupal architecture is actually shaped — Library-First service design, the CLI-First Drush entry point, the Drupal pattern catalogue and its decision criteria, and where the canonical example for each pattern lives in Drupal core.

## Opinion

**A service is the default unit of architecture; forms and controllers are thin.** Every piece of business logic belongs in a service with an interface, registered in a `*.services.yml` file, receiving its collaborators by constructor injection. A form or controller exists to orchestrate — gather input, call a service, hand back a response — and holds no business logic. Business logic living in a `buildForm()` or a controller method is a design defect, not a stylistic preference, and the design is incomplete until it is moved into a service.

**No static `\Drupal::` calls inside a service.** A service names every collaborator it needs in its constructor and its `*.services.yml` entry. A `\Drupal::service(...)` or `\Drupal::entityTypeManager()` call buried inside a service is a hidden, untestable dependency — replace it with an injected argument. Static `\Drupal::` is acceptable only in procedural `.module` glue and in code Drupal does not let you inject into, never in the service layer this recipe designs.

**CLI-First: every feature has a Drush entry point.** Each feature is reachable from a Drush command that calls the *same* service the UI calls — so the feature is scriptable, testable headless, and never UI-only. The Drush command is an orchestration shell over the service, exactly like the form is; the two share the service, never the logic.

**The pattern is chosen against criteria, never defaulted from habit.** Which form base, which storage model, and which extension mechanism a component uses are explicit decisions with stated reasoning — not whatever was used last time. The catalogue and its decision criteria are in the Sequence below.

**Every pattern choice is anchored to a canonical core example.** A recommendation without a Drupal-core file path to study is incomplete. The design names, for each component, the core class that demonstrates the chosen pattern, so the implementer has a proven reference rather than an invented one.

**Mechanics are referenced, not re-authored.** *How* dependency injection, a form, an entity type, or a config schema is actually wired is the knowledge guides' domain. This recipe references `drupal/services`, `drupal/forms`, `drupal/entities`, and `drupal/config-management` for those mechanics and stays focused on the architectural decisions on top of them.

**Design decides; it does not build.** This phase produces an architecture decision for a human to approve — the component breakdown, the dependency map, the pattern choices, and the implementation order. It writes no module code, registers no service, and installs nothing. Recording the decision into the architecture artifact is the plugin's design phase; building from it is Phase 3.

## Preconditions

- A Drupal 10.3+ or 11.x project, Composer-managed, whose target core version is resolvable (so pattern availability can be judged against it).
- The research phase has produced requirements and any prior-art findings (see the `contrib-prior-art` recipe) — the design starts from a known problem and a known build/extend/reuse posture, not a blank brief.
- Read access to a Drupal core checkout (the project's core directory) so canonical example paths can be confirmed, or knowledge of the canonical paths the catalogue names.
- The plugin's generic design phase is present: the architecture artifact and the architecture checklist that gates Phase 3. This recipe supplies the Drupal-specific design method; it does not recreate the artifact or the gate.

## Input contract

Source-agnostic, supplied by the caller (the orchestrator at the design phase, or a human operator).

```yaml
code_path: string             # absolute path to the Drupal project root
requirements: string          # the researched feature/problem to architect
components:                   # optional; pre-identified units to design for
  - string                    #   e.g. "import service", "settings form"
prior_art:                   # optional; the research phase's use/extend/build call
  recommendation: string      #   so design extends contrib rather than re-building it
core_version: string          # optional; the target Drupal core constraint;
                              #   if absent, derived from the project's composer.json
```

## Sequence

If invoked in dry-run mode, perform all reads but emit an architecture-decision preview instead of recording anything. Dry-run is required.

1. **Frame the components.** From `requirements` (and `prior_art`, so an extend recommendation reuses the contrib module rather than re-implementing it), list the units the feature needs: the services that hold its logic, the Drush commands that drive them, the forms / controllers that surface them, and the entities or config that store its data. Services are listed first because everything else depends on them.

2. **Apply Library-First.** For each unit of business logic, define a service with an interface, a `*.services.yml` registration, and constructor-injected dependencies. Confirm no service reaches for a `\Drupal::` static. Demote every form and controller to a thin orchestrator over those services. The mechanics of DI and service registration are referenced to `drupal/services`, not restated here.

3. **Apply CLI-First.** Define at least one Drush command per feature whose attributed command method (`#[CLI\Command(...)]` on a `DrushCommands` subclass) calls the same service the UI calls. No feature is left UI-only. The command is an orchestration shell, carrying no logic of its own.

4. **Select the pattern for each component, against criteria.** Decide, with stated reasoning, which base class or storage model each component uses. Reference `drupal/forms` for the form mechanics, `drupal/entities` for the entity mechanics, and `drupal/config-management` for the config mechanics:

   **Forms** — what is being collected drives the base class:

   | Use case | Pattern | Canonical core example |
   |---|---|---|
   | Module / site settings (stored as config) | `ConfigFormBase` | `core/modules/system/src/Form/SiteInformationForm.php` |
   | Free-standing data entry (not an entity) | `FormBase` | `core/modules/system/src/Form/CronForm.php` |
   | Destructive confirmation | `ConfirmFormBase` | `core/modules/node/src/Form/RebuildPermissionsForm.php` |
   | Add / edit of an entity | `ContentEntityForm` | `core/modules/node/src/Form/NodeForm.php` |
   | Multi-step | `FormBase` + form-state step tracking | contrib `webform` |

   **Storage** — the data's lifecycle and exportability drive the model:

   | Use case | Pattern | Decision criterion |
   |---|---|---|
   | User-created content, often revisioned/translatable | Content entity | The site's editors create and own the data |
   | Exportable bundles / definitions (field types, view modes) | Config entity | The data is part of the site's configuration, deployed via config sync |
   | Simple module settings | Config (`*.settings.yml` + schema) | A small, flat, deployable settings set with no list of instances |
   | High-volume, non-content rows (logs, analytics) | Custom table (schema API) | Append-heavy data that does not need entity overhead |

   **Extensibility** — how the behaviour needs to vary drives the mechanism:

   | Use case | Pattern | Canonical core example |
   |---|---|---|
   | Swappable, discoverable implementations | A plugin type | `core/lib/Drupal/Core/Block/BlockManager.php` |
   | One shared, globally-available behaviour | A service | `core/lib/Drupal/Core/Entity/EntityTypeManager.php` |
   | Genuinely stateless one-off | Static helper (rare) | only when truly stateless and not a dependency |

5. **Anchor each choice to a canonical example.** For every selected pattern, confirm the core file the implementer should study. Check the catalogue paths above first; for anything not in the catalogue, locate the example in core — Grep core for `class <PatternName>`, `extends <BaseClass>`, or `implements <Interface>`, read no more than three candidate files, and record the path plus the key methods and the dependencies it injects. The output of this step is a path, not a paraphrase.

6. **Assemble the architecture decision.** Produce the component breakdown (services first), the dependency map (who injects whom), the per-component pattern choice with its reasoning and its core example path, and the implementation order — services → Drush commands → forms/controllers → integration. Hand the decision to the caller; the plugin's design phase records it into the architecture artifact and runs the checklist gate. The recipe method writes no file of its own.

## Data flow

```
input: code_path, requirements, components (optional), prior_art (optional),
       core_version (optional)

reads project state:
       composer.json (core constraint), existing architecture artifact
       existing custom modules: *.services.yml, src/, *.routing.yml
       Drupal core (canonical example paths for the chosen patterns)

applies opinion:
       service is the unit of architecture · forms/controllers thin ·
       no static \Drupal:: in services · CLI-First Drush entry point ·
       pattern chosen against criteria · every choice anchored to core ·
       design decides, never builds

references origin (never duplicated):
       drupal/services        — DI, service registration, interfaces
       drupal/forms           — form base classes and form mechanics
       drupal/entities        — content vs config entity mechanics
       drupal/config-management — config schema and settings mechanics
       Drupal core            — the canonical example for each pattern

emits (to the caller; the recipe method writes nothing):
       components:     services (first), Drush commands, forms, entities/config
       dependency map: constructor-injection graph
       patterns:       per-component choice + reasoning + core example path
       order:          services → Drush → forms/controllers → integration
```

## State-awareness contract

The recipe reads existing state before deciding. The project's `composer.json` core constraint, any existing architecture artifact, and the current custom-module layout (`*.services.yml`, `src/`, `*.routing.yml`) are read so the design extends what is present rather than colliding with it — and so an extend recommendation from prior art is honoured instead of re-architected from scratch. The method is read-only on the project: it registers no service, writes no module file, and installs nothing; the architecture decision is returned to the caller, which owns recording it.

Idempotent: running the recipe twice on identical input and identical project state produces the same architecture decision, with no side effect on either run. A decision that changes because the requirements or the project's existing components changed is the method reflecting current reality, not a non-deterministic recipe.

## Verifier

After the recipe runs, verify:

1. Every unit of business logic is a service with an interface, a `*.services.yml` registration, and constructor-injected dependencies — and no service in the design reaches for a `\Drupal::` static.
2. Every feature has a Drush command entry point that calls the same service its UI calls; no feature is UI-only.
3. Each component names a chosen pattern with explicit decision reasoning **and** a canonical Drupal-core file path to study.
4. Forms and controllers in the design hold orchestration only — no business logic has been left in a `buildForm()` or a controller method.
5. The design left the project code unchanged — no service registered, no module file written by the method itself, nothing installed; the architecture decision was returned for the plugin's design phase to record.

This recipe ships no executable verifier of its own — the checks above are the agent-driven protocol; the plugin's design phase owns the architecture artifact and the checklist gate that blocks Phase 3 on a failed item.

## References

### Drupal guides (referenced, not authored here)

| Source | Used for |
|---|---|
| `drupal/services` | Dependency injection, service registration, and interface design — the Library-First mechanics this recipe decides with |
| `drupal/forms` | Form base classes and form-building mechanics behind the form-pattern choice |
| `drupal/entities` | Content-entity vs config-entity mechanics behind the storage-pattern choice |
| `drupal/config-management` | Config schema and settings mechanics behind the config-storage choice |

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| Drupal core (the project's core directory) | The canonical example class for each chosen pattern — forms, entities, services, and plugin managers |
| Drush (drush.org) | The CLI-First command entry point that drives each feature's service |

### Plugin-side generic mechanism (ai-dev-assistant)

The stack-neutral design phase this recipe binds Drupal into — when design runs, the shape of the architecture artifact, the mandatory architecture checklist that gates Phase 3, and how the decision is recorded and reviewed — is documented in the plugin itself, not duplicated here. The recipe supplies only the Drupal-specific design method (Library-First service design, the CLI-First Drush entry point, the pattern catalogue and its criteria, and the core-example anchoring) on top of that mechanism.
