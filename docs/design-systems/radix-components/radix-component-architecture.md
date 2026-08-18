---
description: "Understanding Radix's SDC architecture for component selection and customization decisions"
tldr: "Understanding Radix's SDC architecture for component selection and customization decisions."
---

# Radix Component Architecture

## When to Use

> Understanding Radix's SDC architecture for component selection and customization decisions.

## Architecture Overview

This guide documents Radix 6.0.8 (tagged 2026-06-19), the current stable release on the 6.x branch.

| Aspect | Implementation | Why |
|--------|----------------|-----|
| Single Directory Components | `.component.yml` + Twig + CSS + JS in one directory | Drupal core feature (10.1+); automatic asset loading |
| Bootstrap 5.3 foundation | All components map to Bootstrap patterns | Consistent styling, accessibility, responsive behavior |
| Radix as base theme | Never activate Radix directly; always use sub-theme | Updates won't break customizations |
| Component discovery | Drupal scans `themes/*/components/` automatically | Sub-theme components override Radix base |

## The Twig Is The Contract, Not The YAML

Every prop table in this guide is read from the component's `.twig`, because that is the only
file that decides what actually happens. The `.component.yml` `props` block is a validation
schema and a piece of documentation. It is not a filter, and outside a development environment
it is not even checked. (Mechanism verified against Drupal core 11.3.)

**The YAML does not gate what reaches the template.** Core's only prop check is
`ComponentsTwigExtension::validateProps()`, whose entire body is
`assert($this->doValidateProps($context, $component_id));` — under a production
`zend.assertions=-1` that line is compiled out and never runs at all. When it *does* run,
`ComponentValidator::validateProps()` takes the Twig context **by value**, builds a local
`array_intersect_key($context, array_flip($prop_names))` to scope the JSON-Schema check to the
declared names, and returns a bool. It validates; it never writes the context back. Nothing else
in the pipeline filters either: the `component` render element passes `#props` straight through
as the inline-template context, and core's only additions to that context are `componentMetadata`
and `attributes`.

So a variable the YAML never declares still arrives in the template, and if the Twig reads it, it
works. That is why this guide documents props with no YAML entry at all — `radix:nav`'s `items`,
`radix:table`'s `rows` / `striped` / `empty`, `radix:carousel`'s `crossfade`. They are undeclared
and fully functional.

**Core never applies a YAML `default:` either.** There is no default-injection step anywhere in
the SDC pipeline — `ComponentMetadata` parses the schema and stores it, and the JSON-Schema
validator is invoked with `CHECK_MODE_TYPE_CAST` only, never a mode that writes defaults back
(and it runs against that local copy regardless). The value documents intent and feeds the UI.
The effective default is whatever the Twig sets with `|default(...)` or `?? ...`, and the two
disagree often. `radix:heading` is declared `h1` and renders `h2`. `radix:alert` declares
`dismissible` with no default and renders a dismissible alert. `radix:card` declares
`card_text_tag: p` and emits a `div`. Where the YAML and the Twig disagree, the Twig wins and
the YAML entry is inert.

Nothing errors to tell you, in either direction. A misspelled or renamed prop is silent in every
environment: production skips validation entirely, and even with assertions on, the intersect
scopes the check to declared names, so an unknown key is never reported. What validation catches,
in development only, is a *declared* prop given a value of the wrong type.

Three consequences worth carrying into your own components:

- **Read the Twig before you pass a prop.** If the template does not name the variable, passing
  it does nothing, whatever the YAML says. If the template *does* name it, it works, whatever the
  YAML says.
- **Set your defaults in the Twig.** A `default:` in your own `.component.yml` is documentation
  only; if a value must exist, `{% set x = x|default(...) %}` at the top of the template is the
  only thing that guarantees it.
- **Declare your props anyway.** The schema is what gives you type checking in development and
  what the next developer reads first. Undeclared-but-working is a fact about core, not a licence.

Two Twig-specific traps show up in Radix's own defaults. `|default()` replaces *falsy* values,
not just missing ones, so `{% set backdrop = backdrop|default('true') %}` in `offcanvas.twig`
makes `backdrop: false` unreachable; `??` only replaces null and is the safer choice for
booleans. And `{% set x = create_attribute() %}` with no `?:` fallback silently discards
whatever the caller passed.

## Pattern

```twig
{%
  include 'radix:card' with {
    card_title: 'My Card',
    card_body: content.body,
    card_utility_classes: ['shadow-sm', 'mb-4']
  }
%}
```

## Common Mistakes

- **Using Radix as active theme** → Always create sub-theme
- **Ignoring `*_utility_classes` props** → Use for Bootstrap utilities without template overrides
- **Duplicating unchanged templates** → Only override what you modify

## See Also

- [Component Selection Strategy](component-selection-strategy.md)
- Reference: https://docs.trydrupal.com/radix
