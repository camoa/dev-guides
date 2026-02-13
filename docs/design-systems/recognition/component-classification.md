---
description: Classify UI components into atoms, molecules, organisms, templates, and pages
---

# Component Classification Framework

## When to Use

> Use when categorizing UI components into atomic hierarchy. Use after identifying design tokens, when mapping component relationships.

## Decision

| Component Characteristic | Classification | Reasoning |
|-------------------------|----------------|-----------|
| Cannot be broken down further | **Atom** | Foundational element |
| Combines 2-3 atoms, single purpose | **Molecule** | Simple functional group |
| Combines molecules + atoms, complex | **Organism** | Distinct interface section |
| Layout structure, no real content | **Template** | Content-agnostic scaffold |
| Template + actual content | **Page** | Real-world implementation |

## Pattern

**Classification Process:**

```
Step 1: Can it be decomposed?
  NO → Atom
  YES → Continue

Step 2: How many parts?
  2-3 atoms, single function → Molecule
  Multiple molecules/atoms → Continue

Step 3: Discrete interface section?
  YES → Organism
  NO (layout structure) → Continue

Step 4: Contains real content?
  NO (placeholder) → Template
  YES (real) → Page
```

**Example Classifications:**

| Component | Type | Reason |
|-----------|------|--------|
| Button | Atom | Cannot decompose further |
| Search bar (input + button) | Molecule | 2 atoms, single purpose |
| Header (logo + nav + search) | Organism | Multiple molecules, complex |
| Homepage layout | Template | Structure, placeholder content |
| Homepage (logged in) | Page | Real content instance |

## Common Mistakes

- **Wrong**: 5-level taxonomy (atoms/molecules/organisms/cells/tissues) → **Right**: Use 5-stage hierarchy as communication aid, not dogma
- **Wrong**: SearchBar as separate molecule and organism → **Right**: Classify by purpose, not category enforcement
- **Wrong**: Templates with real content → **Right**: Templates use placeholders; pages use real data
- **Wrong**: ProductCard built from scratch → **Right**: Compose from existing atoms/molecules for reusability

## See Also

- [Atom Recognition](./atom-recognition.md)
- [Molecule Recognition](./molecule-recognition.md)
- [Organism Recognition](./organism-recognition.md)
- [Templates vs Pages](./templates-vs-pages.md)
- Reference: [Atomic Design (Brad Frost)](https://atomicdesign.bradfrost.com/chapter-2/)
- Reference: [Atomic Design in 2025: Flexible Practice](https://medium.com/design-bootcamp/atomic-design-in-2025-from-rigid-theory-to-flexible-practice-91f7113b9274)
