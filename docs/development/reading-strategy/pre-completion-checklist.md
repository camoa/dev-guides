---
description: Checklist to run before declaring a Type B task complete — documentation, audit, review, or architecture analysis
tldr: "Use before declaring a Type B task complete — documentation finished, audit signed off, review approved. If any item was skipped because of context-saving instincts, the work is incomplete."
---

# Pre-Completion Checklist

## When to Use

> Use before declaring a Type B task complete — documentation finished, audit signed off, review approved. If any item was skipped because of context-saving instincts, the work is incomplete.

## Decision

| Checklist item | Why |
|----------------|-----|
| All manifest/config files read in full | Wiring, dependencies, permissions live here |
| All entry-point files read in full | Bootstrap, hooks, lifecycle handlers can be anywhere in the file |
| Every source file in the unit read in full | Classes/modules are contracts; partial = missed methods |
| Parent classes, traits, mixins, interfaces read | Inherited behavior isn't visible in the child file |
| Annotation/decorator metadata reviewed | Docblocks carry framework-relevant info grep truncates |
| Cross-reference Grep ran AFTER full reads | "Who uses this?" only after you know what "this" is |

## Pattern

```
Type B task complete check:

1. Manifests & configs — did you read every one in full?
   - package.json / composer.json / *.info.yml
   - services.yml, routing.yml, permissions.yml
   - *.config.ts, tsconfig.json, etc.

2. Entry points — did you read every one in full?
   - *.module, main.py, index.js, lib.rs
   - install/uninstall hooks, lifecycle files

3. Source files — did you read every one in full?
   - All classes/components in src/ or lib/
   - All stores, reducers, handlers, plugins

4. Inheritance chain — did you follow it?
   - For each source file, which parents/traits/interfaces did you also read?

5. Annotations/decorators — did you check them?
   - Plugin attributes, ORM mappings, validation constraints

6. Cross-references — did you grep AFTER the above?
   - Not a substitute for reading, but a verification of relationships
```

## Common Mistakes

- **Wrong**: Declaring an audit complete because you read "the main files" → **Right**: Run the checklist; audits fail when inherited methods or wired services are missed
- **Wrong**: Skipping config files "because they're just YAML" → **Right**: YAML is where wiring lives; half of security findings come from permission and service configs
- **Wrong**: Treating the inheritance chain as "too deep, not worth it" → **Right**: Read at least one level of parents; abstract methods and trait behavior cascade
- **Wrong**: Running grep BEFORE full reads to "save time" → **Right**: Grep is a verification tool for Type B, not a discovery tool

## See Also

- [Type B — Comprehensive Understanding](task-type-b-comprehensive-understanding.md)
- [What Grep Misses](what-grep-misses.md)
