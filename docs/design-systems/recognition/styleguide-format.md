---
description: Canonical 9-section structure for a regenerable styleguide artifact that bridges DS authoring and Stage 2 implementation tools
tldr: Use this when producing or evaluating a styleguide artifact — a regenerable markdown snapshot consolidating tokens, atoms, molecules, organisms, image use cases, and classifications into a single document that serves as the API contract for theme converters and SDC generators. Regenerate on every committed DS change; never edit the generated output manually.
---

# Styleguide Format

## When to Use

> Use this when you need to produce or evaluate a styleguide artifact — a regenerable markdown snapshot that consolidates all design-system layers into a single reviewable document. This is the contract between Stage 1 design authoring and Stage 2 implementation tools (theme converters, SDC generators, code generators).

## Decision

| Situation | Choose | Why |
|-----------|--------|-----|
| Stage 2 tool needs DS input | Styleguide artifact | Single document; format is the API contract |
| DS has changed and converters need to rerun | Regenerate styleguide | Converters must read current state, not stale snapshot |
| Designer wants to prototype a new component idea | Do NOT regenerate yet | Styleguide reflects committed state, not design intent |
| Manual edits were made to generated output | Revert and fix source | Manual edits are overwritten on next regen |

## Pattern

A conforming styleguide contains these 9 sections in order (1–7 required, 8 conditional, 9 required):

| # | Section | Required | Content |
|---|---------|----------|---------|
| 1 | Brand Foundation | Yes | Prose: voice, visual personality, design intent |
| 2 | Tokens | Yes | Colors, typography, spacing, breakpoints, effects — each as `name \| value \| semantic alias` table |
| 3 | Atoms | Yes | Props table + variants table per atom |
| 4 | Molecules | Yes | Atom-dependency list + behaviors table per molecule |
| 5 | Organisms | Yes | Composition list + `classification` field (native / composite / custom) |
| 6 | Image Use Cases | Yes | Typed YAML/JSON block: `name`, `aspectRatio`, `maxWidth`, `purpose`, `formatPriority` |
| 7 | Component Classifications | Yes | 3-column table: `component \| classification \| rationale` |
| 8 | Theme Variables | Conditional | Token-to-CSS-variable mappings; omit if utility-classes-only |
| 9 | Regeneration Model | Yes | Source of truth per section + canonical regeneration triggers table |

**Canonical regeneration triggers:**

| Trigger | When |
|---------|------|
| Initial scaffold | DS authoring begins; brand + tokens only |
| DS authoring complete | All atoms/molecules/organisms documented |
| DS extension during composition | New component discovered; update before Stage 2 runs |
| On-demand | Before any theme conversion sprint |

## Common Mistakes

- **One-time generation** — The value is regenerability. Each regen gives converters a fresh, accurate contract.
- **Folding image use cases into Atoms** — Image use cases must appear in their own section (6) so converters scan a single location.
- **Omitting classification rationale** — Listing `custom` without rationale leaves converter authors guessing; rationale makes it reviewable.
- **Manually editing generated output** — Any manual edit is lost on the next regen. Fix the source metadata or generator template instead.
- **Skipping the Regeneration Model section** — Without it, consumers treat the styleguide as static and stop regenerating after first use.

## See Also

- [6. Templates vs Pages](templates-vs-pages.md)
- [3. Atom Recognition](atom-recognition.md) — image atom classification
- [5. Organism Recognition](organism-recognition.md) — organism composition patterns
- [8. Design System Analysis Best Practices](design-system-analysis-best-practices.md)
- Cross-topic: `../daisyui/customization-patterns.md` — component classification decision tree
