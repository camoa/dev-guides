---
description: Plus Suite vs Canvas (Experience Builder) — architecture comparison, decision matrix, and coexistence guidance
drupal_version: "11.x"
---

# Plus Suite vs Canvas (Experience Builder)

## When to Use

> Use Plus Suite when you have existing Layout Builder investment or a PHP-only team. Use Canvas for new Drupal CMS projects prioritizing long-term core alignment.

## Decision

| Factor | Choose Plus Suite | Choose Canvas |
|--------|------------------|---------------|
| Existing LB investment | Yes — drop-in upgrade | No — requires migration |
| Need LB contrib modules | Yes — compatible | No — different system |
| PHP-only team | Yes — no React required | No — requires React knowledge |
| Greenfield Drupal CMS project | Consider | Yes — official direction |
| Maximum future-proofing | Less certain | Yes — core initiative |
| Workspace integration | Yes — Tempstore+ | Under development |
| Custom tooling needs | Yes — pluggable modes/tools | Component-level customization |
| Time to production | Faster for LB users | Learning curve for new paradigm |

## Pattern

**Fundamental differences:**

| Aspect | Plus Suite | Canvas |
|--------|-----------|--------|
| Architecture | PHP/Twig native, enhances Layout Builder | React frontend, ground-up rebuild |
| Foundation | Layout Builder (enhanced) | New rendering engine |
| Data model | Layout Builder sections, blocks, entities | Components, slots, props |
| Frontend | Server-rendered Twig | React client-side rendering |
| Maturity | Early (March 2025) | 1.0 (late 2025), Drupal CMS 2.0 default |
| Backing | Tag1 Consulting (contrib) | Drupal core initiative |
| Compatibility | Drop-in LB replacement | New system, migration needed |

**Coexistence:** Both can coexist on different content types. No migration path between them.

## Common Mistakes

- **Wrong**: Choosing Plus Suite just because it's familiar → **Right**: Evaluate Canvas for new greenfield projects
- **Wrong**: Choosing Canvas just because it's "official" → **Right**: If you have heavy LB investment, Plus Suite may be more practical

## See Also

- [Overview](overview.md)
- [Architecture & Module Map](architecture-module-map.md)
- Reference: [Canvas/Experience Builder](https://www.drupal.org/project/experience_builder)
