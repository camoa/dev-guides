---
description: The three Drupal contribution workflows — core, your own contrib, and someone else's contrib — and how they differ across authority, CI ownership, and merge gates
tldr: "Read this first: the three workflows (core / your own contrib / someone else's contrib) differ in authority, CI ownership, and who merges. Target `main` for all new core work; contrib follows each project's branch conventions."
drupal_version: "11.x"
---

# Three Contribution Workflows Compared

## When to Use

> Read this first. Every other section in this guide behaves differently depending on which of the three workflows you are in. This orientation section maps the decision space so every subsequent section makes sense.

## Decision

| Dimension | **A. Core** | **B. Your own contrib** | **C. Someone else's contrib** |
|---|---|---|---|
| Repository target | `drupal/drupal` `main` branch | Your project's branches | The project's branches (from a fork) |
| CI config owner | Core maintainers (read-only to you) | **You** — you set the `.gitlab-ci.yml` | The maintainer (read-only to you) |
| Blocking jobs | Stricter; linting effectively enforced | Your choice — `allow_failure` per job | Whatever the maintainer configured |
| Issue assignment | Discouraged — comment instead | Your policy | Follow project policy; ask first |
| Gates | All 6 core gates mandatory | None mandatory; you define them | The maintainer's documented expectations |
| RTBC discipline | Strict; no self-RTBC as sole author | Relaxed; self-RTBC OK as maintainer | Strict; no self-RTBC unless maintainer allows |
| Who merges | Core committers only | You / trusted committers | The maintainer only |
| Your authority | Propose only | Full | Propose only |
| Pace | Slow; release-phase limits apply | You control | Maintainer's pace — be patient |

## Branch Strategy (2025–2026)

Core's branching changed. For **core contributions:**

| Branch | Status | Use for |
|---|---|---|
| `main` | Primary development trunk | **All new work** — features, improvements |
| `11.x` | Deprecated interim branch | 11.x-specific bugs only; do not target for new features |
| `10.x` | Critical fixes only | EOL Dec 2026 after Drupal 12 (targeted Aug 2026) |

For **contrib modules:** follow each project's own branch conventions. Always make the MR against the most recent development branch first. Backports to older branches are a later maintainer decision, not a contributor decision.

## Core Gates (Workflow A only)

| Gate | Owned by |
|---|---|
| Accessibility | Accessibility team |
| Documentation | Docs team |
| Frontend | Frontend team |
| Performance | Performance team |
| Testing | Testing (test coverage required) |
| Usability | UX team |

Not every core change triggers a cross-team review — scope determines which gates apply.

## Common Mistakes

- **Wrong**: Targeting `11.x` for new core features → **Right**: Target `main` for all new work
- **Wrong**: Self-assigning a core issue without commenting → **Right**: Post a comment stating what part you are taking
- **Wrong**: Opening a backport MR without first merging into the development branch → **Right**: Target the development branch; maintainers backport
- **Wrong**: Treating contrib CI strictness as equal to core CI → **Right**: Contrib CI is configured per-maintainer; read the `.gitlab-ci.yml`

## See Also

- [The drupalci Pipeline & gitlab_templates](drupalci-pipeline-gitlab-templates.md)
- [Serving as a Drupal Module/Theme Maintainer](module-theme-maintainer.md)
- Reference: [drupal.org/about/core/policies/core-change-policies/core-gates](https://www.drupal.org/about/core/policies/core-change-policies/core-gates)
- AI overlay: [Contributing with AI](../contributing-with-ai/index.md)
