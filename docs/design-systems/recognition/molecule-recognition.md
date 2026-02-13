---
description: Recognize composite components that combine 2-3 atoms for a single purpose
---

# Molecule Recognition

## When to Use

> Use when you've identified atoms and need to find grouped patterns. Use to determine if a component is a molecule vs organism.

## Decision

| Component Has... | Classification | Reasoning |
|------------------|----------------|-----------|
| 2-3 atoms, single purpose | **Molecule** | Simple functional group |
| 1 atom only | **Atom** | Not composite |
| Many atoms, multiple purposes | **Organism** | Too complex |
| Layout structure for organisms | **Template** | Page-level organization |

## Pattern

**Common Molecule Types:**

| Molecule | Atoms | Purpose | Example |
|----------|-------|---------|---------|
| **Form Field** | Label + Input + Error message | Single data entry | "Email" + text input + "Invalid email" |
| **Search Bar** | Input + Button + Icon | Search functionality | Search input + magnifying glass + "Search" |
| **Card Content** | Image + Heading + Text + Button | Content unit | Product photo + name + price + "Add to cart" |
| **Navigation Item** | Link + Icon | Single nav element | Home icon + "Home" link |
| **Media Object** | Image/Avatar + Text block | Content with media | User avatar + comment text |
| **Button Group** | 2-3 related buttons | Related actions | "Cancel" + "Save" |
| **Breadcrumb** | Links + Dividers | Navigation hierarchy | Home > Products > Category |
| **Stats Display** | Icon + Number + Label | Single metric | Heart icon + "1,234" + "Likes" |
| **Alert/Toast** | Icon + Message + Close | Notification | Warning icon + "Saved" + X |
| **Pagination** | Prev + Page numbers + Next | Page navigation | "< Prev" + "1 2 3" + "Next >" |

**Recognition Strategy:**

```
1. Identify functional grouping
   - Do atoms always appear together?
   - Single purpose?
   - Reusable as unit?

2. Count components
   - 2-3 atoms → Likely molecule
   - 4+ atoms or multiple molecules → Organism

3. Test single responsibility
   - Does ONE thing well → Molecule
   - Multiple purposes → Organism

4. Check independence
   - Exists outside context → Molecule
   - Context-dependent → Part of organism
```

## Common Mistakes

- **Wrong**: Adding 5+ atoms to a molecule → **Right**: Keep molecules simple (2-3 atoms); more complexity = organism
- **Wrong**: Form field as organism → **Right**: Single label + input + error is a molecule
- **Wrong**: Individual atoms used together without grouping → **Right**: Only intentionally grouped, reusable units are molecules
- **Wrong**: Every atom pairing is a molecule → **Right**: Only if reused as unit

## See Also

- [Atom Recognition](./atom-recognition.md)
- [Organism Recognition](./organism-recognition.md)
- [Component Classification](./component-classification.md)
- Reference: [Atomic Design Molecules](https://atomicdesign.bradfrost.com/chapter-2/#molecules)
