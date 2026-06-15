---
# Routing block — an orchestrator reads to here and decides.
name: cc_plugins_design_architecture
capability: design
description: Use when a Claude Code plugin project enters the design phase and must turn a researched need into a component architecture — applies the decision framework to choose skill / command / agent / hook / MCP per capability, enforces progressive disclosure and the description budget, fixes the plugin boundary and manifest layout, and records a component map the implement and review phases conform to, before any component is scaffolded.
# Metadata — read only after a match.
label: Plugin component architecture (Claude Code)
recipe_schema_version: 1.0.0
version: 0.1.0
# Process-recipe routing keys, enforced by validate_recipes.py for any recipe
# under docs/process-recipes/. `capability` above doubles as the phase (the
# lifecycle moment the orchestrator resolves on); there is no separate
# applies_to_phase. `framework` is the second routing dimension.
recipe_class: process
framework: claude-code-plugins
assumes:
  - claude-code
authors:
  - name: camoa
license: GPL-2.0-or-later
---

## Goal

Turn the researched need into a component architecture before any component is scaffolded. The design decides, for each capability the plugin must deliver, **which component type carries it** (skill, command, agent, hook, MCP server, theme), **how the components decompose** (one responsibility each), **how progressive disclosure is honoured** (lean bodies, detail in references, descriptions inside the budget), and **where the plugin boundary sits** (a new plugin, or components added to an existing one). It records a component map — the architecture artifact the implement and review phases conform to.

The plugin owns the generic design phase — when it runs and the artifact slot it fills. This recipe owns the Claude-Code-specific judgement the stack-neutral mechanism cannot make: the component-type decision, the progressive-disclosure and description-budget constraints, and the manifest-and-boundary layout.

## Opinion

**Component type is chosen, not defaulted.** Each capability runs through the decision framework before it gets a type: a skill for a model-invoked workflow that benefits from progressive disclosure; a command for an action the user types deliberately; an agent for work that needs fresh-context isolation or a narrowed tool set; an MCP server for an external system or data source; a hook for a reaction to a lifecycle event; a theme for a visual identity. Picking the type by habit is how a plugin ends up with a command that should have been a skill.

**Skills over commands for new work.** Commands are the legacy surface — supported, but a new capability that the model should reach for on its own belongs in a skill, where the `description` trigger and progressive disclosure do their work. The design reaches for a command only when the action is genuinely user-initiated and should not auto-fire.

**Progressive disclosure is an architectural constraint, not a finishing polish.** The design fixes, per skill, what lives in the `SKILL.md` body (the lean instruction set — under ~250 lines) and what is pushed into `references/` (the depth loaded on demand). A skill designed as one long body is a design defect, not a formatting one, because the whole body is paid for in context on every load.

**The description budget is part of the design.** A skill's `description` plus its when-to-use is capped (≈1,536 characters) and silently truncated past it, so the design front-loads the primary trigger to survive truncation and writes the description in the third person with literal trigger phrasing. A capability whose trigger surface cannot be expressed inside the budget is a signal the component is doing too much and should be split.

**One responsibility per agent.** An agent is designed around a single job and the minimum tool set that job needs. An agent that reviews *and* fixes *and* reports is three agents wearing one name; the design separates them so each can be reasoned about, permissioned, and modelled independently.

**Hooks are designed to the event and the handler, exec-form first.** A hook is bound to one of the recognised lifecycle events and one handler type, chosen deliberately; a one-time setup belongs on a setup event, not bolted onto session start. The design prefers the exec form (explicit `args`) over a shell-form command string, and never routes a hook to `/dev/tty`.

**The manifest and the boundary are decided here.** `.claude-plugin/plugin.json` is the only manifest home; the design records it and the directory layout, and notes the path semantics that bite later — `skills/` *adds* to the default while `commands`, `agents`, and `experimental.themes` *replace* their default folder when a custom path is set. The plugin boundary follows the research recommendation: extend an existing plugin with the new components, or stand up a new one only when no existing plugin owns the domain.

**Design grounds every choice and records it; it scaffolds nothing.** Each component-type decision is grounded in the decision framework and the canonical templates rather than taste, and the result is written as a component map for the downstream phases to build and check against. The design creates no files and runs no scaffolder — that is the implement phase's work.

## Preconditions

- A Claude Code environment with plugin support, Composer-free (plugins are file-based) — the design needs only the research output and the documented component contracts.
- The research recommendation is available (see the prior-art recipe under this framework): reuse / extend / build-new, with the plugin and domain it concerns. The design conforms the boundary to that recommendation rather than re-deriving it.
- The plugin's generic design phase is present: the phase that invokes this method and slots the artifact. This recipe supplies the Claude-Code-specific architecture; it does not recreate the phase.

## Input contract

Source-agnostic, supplied by the caller (the orchestrator at the design phase, or a human operator).

```yaml
need: string                  # the capability set the plugin must deliver
research: string              # the prior-art recommendation (reuse | extend | build-new)
                              #   and the plugin / domain it named
target_plugin: string         # optional; the existing plugin to extend, when research
                              #   recommended extend
constraints: [string]         # optional; tool-permission, model, or distribution constraints
```

## Sequence

If invoked in dry-run mode, perform all reads and emit a component-map preview instead of recording the artifact. Dry-run is required.

1. **Read the research recommendation.** Resolve whether the work extends an existing plugin (and which) or stands up a new one, so the boundary is fixed before components are placed. Read the documented component contracts through `plugin-creation-tools:plugin-creation` rather than recalling them.

2. **Apply the decision framework per capability.** For each capability in the need, choose the component type — skill, command, agent, hook, MCP, or theme — against the framework, and record *why* that type and not its neighbours. Default new model-invoked workflows to skills; reserve commands for deliberately user-typed actions.

3. **Decompose into components.** For each component, fix: its name (kebab-case), its single responsibility, its trigger surface (the skill/agent `description`, or the command name), the minimum tool permissions it needs, and its model (leaving skills to inherit, pinning an agent only with a reason — and never pinning a skill to a sub-1M-context model).

4. **Apply progressive disclosure and the description budget.** For each skill, split the lean `SKILL.md` body from the on-demand `references/` depth, and draft the `description` inside the budget with the primary trigger front-loaded. A component that cannot be expressed within these constraints is flagged for splitting before it reaches implement.

5. **Lay out the manifest and the boundary.** Record the `.claude-plugin/plugin.json` shape and the directory layout, noting the add-vs-replace path semantics. Confirm the plugin boundary matches the research recommendation (extend the named plugin, or a new plugin only when no existing one owns the domain).

6. **Record the component map.** Write the architecture artifact — every component with its type, responsibility, trigger, permissions, model, and body/references split, plus the manifest and boundary decision. This is what the implement phase builds and the review phase conforms against.

## Data flow

```
input: need, research recommendation, target_plugin (optional), constraints (optional)

reads project / environment state:
       the research recommendation (reuse | extend | build-new + named plugin/domain)
       the documented component contracts (skill / command / agent / hook / MCP / theme)
       the existing plugin's layout, when the recommendation was extend

applies opinion:
       component type is chosen via the decision framework · skills over commands for
       new work · progressive disclosure is a constraint · the description budget is
       part of the design · one responsibility per agent · hooks designed to event +
       handler, exec-form first · manifest + boundary decided here · design records,
       never scaffolds

references origin (never duplicated):
       plugin-creation-tools:plugin-creation — the decision framework, the component
              contracts, progressive disclosure, the manifest + path semantics
       superpowers-developing-for-claude-code:developing-claude-code-plugins —
              the lifecycle workflow the design sits inside (Plan → Create → Add …)

emits (to the caller; the recipe writes nothing):
       component_map:  per component — type, responsibility, trigger, tool permissions,
                       model, body/references split
       manifest:       the plugin.json shape + directory layout
       boundary:       extend <named plugin> | new plugin, conformant with research
```

## State-awareness contract

The recipe reads the research recommendation and, when the work extends a plugin, that plugin's existing layout before placing anything — it conforms the boundary to a recorded decision and designs around what is already there, not around a blank slate. The method is read-only on the project: it scaffolds no component, writes no manifest, installs nothing; the component map is returned to the caller, which owns recording it as the architecture artifact the downstream phases consume.

Idempotent for fixed inputs: running the design twice over the same need, the same research recommendation, and the same existing-plugin state produces the same component map. A map that changes because the need or the research changed is the design reflecting current reality, not a non-deterministic recipe.

## Verifier

After the recipe runs, verify:

1. Every capability in the need maps to exactly one component type, each chosen against the decision framework with the reason recorded — and no new model-invoked workflow was placed in a command where a skill was the right home.
2. Each component carries a single responsibility, a kebab-case name, a trigger surface, a minimum tool-permission set, and a model decision (skills left to inherit unless justified; no skill pinned to a sub-1M-context model).
3. Each skill records its body/`references/` split and a `description` drafted inside the budget with the primary trigger front-loaded; any component that could not fit the constraints is flagged for splitting.
4. The manifest shape and directory layout are recorded, with the add-vs-replace path semantics noted, and the plugin boundary matches the research recommendation.
5. The design left the project unchanged — no component scaffolded, no manifest written, nothing installed; the component map was returned for the plugin's design phase to record as the artifact the implement and review phases conform to.

This recipe ships no executable verifier of its own — the decision-and-decomposition steps are the agent-driven protocol; the plugin's design phase owns the artifact slot and how the component map feeds the implement phase.

## References

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| `plugin-creation-tools:plugin-creation` | The decision framework (skill / command / MCP / agent / agent-team / hook), the component contracts, progressive disclosure, the description budget, and the `.claude-plugin/plugin.json` manifest with its add-vs-replace path semantics — the mechanics the component-type and layout decisions rest on |
| `superpowers-developing-for-claude-code:developing-claude-code-plugins` | The end-to-end plugin lifecycle (Plan → Create Structure → Add Components → Test → Release) the design phase sits inside |

### Plugin-side generic mechanism (ai-dev-assistant)

The stack-neutral design phase this recipe binds Claude Code into — when the phase runs, the artifact slot it fills, and how the component map feeds the implement and review phases — is documented in the plugin itself, not duplicated here. The recipe supplies only the Claude-Code-specific architecture: the component-type decision, the progressive-disclosure and description-budget constraints, and the manifest-and-boundary layout.
