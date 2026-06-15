---
# Routing block — an orchestrator reads to here and decides.
name: cc_plugins_research_prior_art
capability: research
description: Use when a Claude Code plugin project enters the research phase and must establish prior art before building — searches the installed skill / command / agent / hook / MCP surface and the reachable marketplaces, evaluates candidates by availability, maintenance, trust and trigger-surface fit, and reports reuse / extend / build-new before any component is scaffolded.
# Metadata — read only after a match.
label: Plugin prior-art research (Claude Code)
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

Establish prior art before a single Claude Code component is scaffolded. The research asks one question from several angles: **does the capability already exist** — as an installed skill, command, agent, hook, or MCP server, or as a plugin reachable in a marketplace — and if it half-exists, is the right move to reuse it, extend the plugin that owns it, or build new. It returns a reuse / extend / build-new recommendation backed by the candidates it found and why each was kept or rejected.

The plugin owns the generic research phase — when it runs and the envelope it emits. This recipe owns the part the stack-neutral mechanism cannot know: *where* Claude Code capabilities live (the installed registry and the marketplaces), *how* to read a candidate's trigger surface, and *what* disqualifies a candidate from reuse.

## Opinion

**The default is not to build.** A new component earns its place only when nothing installed and nothing reachable covers the need. The cheapest plugin is the one already loaded; the second cheapest is one more component added to a plugin that already exists. A brand-new plugin is the most expensive option and the last one considered.

**Apply the 5-and-10 threshold before recommending a build.** A component is worth authoring when the task it automates has been done five or more times and will plausibly recur ten or more. Research that recommends building a component for a one-off is recommending waste — the recommendation records the recurrence evidence, or it recommends reuse.

**Search the model-invoked surface, not just the slash menu.** Skills are auto-triggered on their `description`; a capability can already be covered by a skill the user never types. Reading only the `/command` list misses exactly the components designed to fire without being named. The search reads the installed skill, command, agent, hook, and MCP surface together.

**Prefer extend over create.** When a candidate plugin owns the right domain but lacks the one component needed, the recommendation is to add that component to it (`/plugin-creation-tools:add-component`), not to stand up a parallel plugin that fragments the surface. A new plugin is justified only when no existing plugin owns the domain.

**The registry and the APIs are read live, never from memory.** Which plugins are installed, what a marketplace currently offers, and what the plugin / skill / hook contracts are this version — all move. The research reads the authoritative documentation through `superpowers-developing-for-claude-code:working-with-claude-code` and the live registry rather than recalling how it worked.

**Trust is a selection criterion.** A candidate from an unknown marketplace owner, or one that traverses paths it should not, is a finding, not a dependency. The research weighs the source the same way it weighs fit.

**Research reports; it does not scaffold.** The phase returns prior art and a recommendation. It creates no plugin, writes no component, installs nothing. Acting on the recommendation is the design and implement phases' work.

## Preconditions

- A Claude Code environment with plugin support, with the installed plugin / skill / command / agent / MCP registry readable and at least one marketplace reachable.
- A described need — the capability to be built, framed (or framable) as the trigger or use-case that would invoke it.
- The plugin's generic research phase is present: the phase that invokes this method and emits the research envelope. This recipe supplies the Claude-Code-specific search and evaluation; it does not recreate the phase.

## Input contract

Source-agnostic, supplied by the caller (the orchestrator at the research phase, or a human operator).

```yaml
need: string                  # the capability to research, described as the trigger /
                              #   use-case that would invoke it
component_hint: string        # optional; suspected component type
                              #   (skill | command | agent | hook | mcp | theme)
marketplaces: [string]        # optional; marketplaces to search beyond the installed set
recurrence: string            # optional; evidence of how often the task has occurred /
                              #   will recur, for the 5-and-10 threshold
```

## Sequence

If invoked in dry-run mode, perform all reads and emit a prior-art preview instead of recording a recommendation. Dry-run is required.

1. **Frame the need as a trigger surface.** Restate the need as the user phrasing or task that would invoke it, and as a candidate component type (skill for an auto-triggered workflow, command for a user-typed action, agent for isolated specialized work, hook for an event reaction, MCP for an external integration). This frame is what every candidate is matched against.

2. **Search the installed surface.** Read the installed plugins and, within them, the skill `description` triggers, the `/command` set, the agent descriptions, the declared hooks, and the MCP servers. A skill whose description already fires on the framed trigger is prior art even if no command names it. Defer to `superpowers-developing-for-claude-code:working-with-claude-code` for how the registry and loading actually work this version.

3. **Search the reachable marketplaces.** For needs the installed set does not cover, search the configured marketplaces (and any named in `marketplaces`) for candidate plugins, reading each candidate's described capability against the frame.

4. **Evaluate each candidate.** Score on availability (installed, or installable from a trusted marketplace), maintenance (version, recency, changelog), trust (marketplace owner, no path traversal or over-broad permissions), trigger-surface fit (does its description fire on the need), and component-type fit (does it deliver the need as the right component type).

5. **Decide reuse / extend / build-new.** Reuse a candidate that already covers the need. Extend the plugin that owns the right domain with one added component (`/plugin-creation-tools:add-component`) when the domain exists but the component does not. Recommend a new plugin (`/plugin-creation-tools:create`) only when no existing plugin owns the domain **and** the 5-and-10 threshold is met; otherwise recommend deferring the build.

6. **Report.** Return the candidates found, each kept-or-rejected with the reason, and the single reuse / extend / build-new recommendation with its evidence.

## Data flow

```
input: need, component_hint (optional), marketplaces (optional), recurrence (optional)

reads environment state:
       installed plugins + their skills / commands / agents / hooks / MCP servers
       skill and agent `description` triggers (the model-invoked surface)
       reachable marketplace catalogs (installed + caller-named)
       authoritative Claude Code docs (registry, loading, component contracts)

applies opinion:
       default is not to build · 5-and-10 threshold before any build · search the
       model-invoked surface, not just /commands · prefer extend over create · read
       the registry and APIs live, never from memory · trust is a selection criterion
       · research reports, never scaffolds

references origin (never duplicated):
       superpowers-developing-for-claude-code:working-with-claude-code — registry,
              loading, component contracts (read live)
       plugin-creation-tools (plugin) — /plugin-creation-tools:add-component and
              /plugin-creation-tools:create, the handoff targets the recommendation names

emits (to the caller; the recipe writes nothing):
       candidates:      each with availability / maintenance / trust / fit + kept|rejected
       recommendation:  reuse | extend | build-new (with the plugin/component named) |
                        defer, with the evidence (including 5-and-10) behind it
```

## State-awareness contract

The recipe reads the live environment — what is installed, what the reachable marketplaces offer, and the current component contracts — before judging. It matches candidates against the framed need, not against an idealized catalog, so a capability already present is found rather than rebuilt. The method is read-only on the environment: it installs nothing, scaffolds nothing, edits no plugin; the candidates and the recommendation are returned to the caller, which owns recording them and acting on the build decision.

Idempotent for a fixed environment: running the research twice over the same installed set, the same reachable marketplaces, and the same need produces the same candidates and the same recommendation. A recommendation that changes because a marketplace gained a plugin, or a plugin was installed, is the research reflecting current reality, not a non-deterministic recipe.

## Verifier

After the recipe runs, verify:

1. The installed surface was searched across all component types — skills (by `description` trigger), commands, agents, hooks, and MCP servers — not only the `/command` list.
2. The reachable marketplaces were searched for needs the installed set did not cover, and each candidate was read against the framed trigger surface.
3. Every candidate carries an evaluation (availability, maintenance, trust, trigger-surface fit, component-type fit) and a kept-or-rejected reason.
4. The recommendation is exactly one of reuse / extend / build-new / defer, names the plugin and component it concerns, and — for build-new — records the 5-and-10 recurrence evidence rather than asserting a build on a one-off.
5. The research left the environment unchanged — nothing installed, scaffolded, or edited; the candidates and recommendation were returned for the plugin's research phase to record.

This recipe ships no executable verifier of its own — the search-and-evaluate steps are the agent-driven protocol; the plugin's research phase owns the envelope and what the recommendation feeds into design.

## References

### External origins (referenced, not authored here)

| Source | Used for |
|---|---|
| `superpowers-developing-for-claude-code:working-with-claude-code` | The authoritative, live Claude Code documentation — how the plugin / skill / command / agent / hook / MCP registry and loading work this version; read rather than recalled |
| `superpowers-developing-for-claude-code:developing-claude-code-plugins` | The plugin lifecycle overview, for situating a candidate's maturity and where an extend-vs-build decision lands |
| plugin-creation-tools (plugin) | The scaffolding the recommendation hands off to — `/plugin-creation-tools:add-component` for extend, `/plugin-creation-tools:create` for build-new; this recipe names them, it does not invoke them |

### Plugin-side generic mechanism (ai-dev-assistant)

The stack-neutral research phase this recipe binds Claude Code into — when the phase runs, the envelope it emits, and how its recommendation feeds the design phase — is documented in the plugin itself, not duplicated here. The recipe supplies only the Claude-Code-specific method: where capabilities live (the installed registry and the marketplaces), how to read a candidate's trigger surface, and the reuse / extend / build-new line.
