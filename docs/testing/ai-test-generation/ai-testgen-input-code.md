---
description: Seeding plan generation from codebase analysis — which source files yield the most useful test plan vocabulary for Drupal, React/Next.js, and generic projects.
tldr: "Point the Planner at routing + form + permissions + one existing spec — not the whole codebase. For Drupal, *.routing.yml and buildForm() yield routes, field labels, and required-field negatives automatically. Always combine code analysis with live exploration — the rendered DOM (with hooks, Ajax fields, #states) is authoritative over the PHP source."
---

# Input: Code Analysis

## When to Use

> Generating plans from the codebase — the Planner reads source files to extract routes, forms, content types, permissions.

## Decision

| Approach | When |
|---|---|
| Single file (routing + form for one feature) | Targeted plan generation |
| Module directory | Plan for one bounded feature |
| Whole repo | Almost never — token waste, shallow output |

Be selective. Routing + form + permissions + one existing spec is usually enough for a focused plan.

## Pattern: useful extractions per codebase

**Drupal:**

| Source | Yields |
|---|---|
| `*.routing.yml` | URLs, controllers, access requirements |
| `src/Form/*.php` `buildForm()` | Field names, labels, `#required`, `#type` |
| `node.type.*.yml`, `field.field.node.*.yml` | Content types and their fields |
| `*.permissions.yml` | Roles for boundary-case enumeration |
| `composer.json` | ATK detection, Drush version, Drupal core version |
| Existing tests in `tests/` | Style reference — Planner mirrors structure |

**React / Next.js:**

| Source | Yields |
|---|---|
| `app/**/page.tsx` (App Router) | Routes |
| Form components with `<form>` | Fields, validation rules |
| `package.json` | Framework version, testing stack |
| `playwright.config.ts` | Existing test conventions |

**Generic:**

| Source | Yields |
|---|---|
| OpenAPI / sitemap.xml | Routes |
| README.md "Getting Started" | Critical user flows |
| `tests/` siblings | Test style |

## Pattern: telling the Planner what to extract

```
Generate a test plan for the contact form. Read these files only:
- web/modules/custom/site_contact/site_contact.routing.yml
- web/modules/custom/site_contact/src/Form/ContactForm.php
- specs/example-form.md (use as style reference)
```

This focuses the Planner. Without scope, it crawls broadly and produces flat plans.

## Pattern: deriving negative cases from code

`#required => TRUE` in a Drupal form is a free negative test:

```markdown
**Negative checks:**
- Submitting with empty "Your name" shows an error referencing that field
- Submitting with empty "Subject" shows an error referencing that field
```

The Planner can produce this list automatically if pointed at the form class.

## Anti-Patterns

- **"Read every PHP file"** — token budget; shallow understanding
- **Generate plan from form class alone, without exploring live** — misses JS-only fields (Ajax-added), conditional fields (`#states`), client-side validation
- **Trusting the code over the live site** — if the form has been overridden by a hook or alter, the rendered DOM is authoritative

## Common Mistakes

- **Pointing at the whole codebase** instead of the feature-specific subset
- **Skipping the live exploration step** — Playwright Test Agents Planner *both* reads code and opens the browser; honor both
- **Using stale routes** — Drupal route changes don't always rebuild caches in dev; verify against actual `drush route:list`

## See Also

- [Input: User Stories](ai-testgen-input-user-stories.md)
- [Hybrid Inputs](ai-testgen-hybrid-inputs.md)
- [Drupal & ATK Notes](ai-testgen-drupal-atk-notes.md)
