---
description: ATK's ~36 shipped tests organized by area — authentication, content, page errors, forms, navigation, search, media, email, and FedRAMP.
tldr: ATK ships ~36 tests organized by area (auth, content, page errors, forms, navigation, search, media, email, FedRAMP) with parallel Cypress and Playwright variants. Run only the auth + page-error suites for a first-day smoke check; never modify ATK's shipped test files in-place.
drupal_version: "11.x"
---

# ATK Test Catalog

## When to Use

> Use this guide when picking which ATK tests to run against your site or when scoping a smoke vs full suite.

## Decision

| If you're starting | Run |
|---|---|
| First-day smoke check | Auth + page-error suites only |
| Full pre-deploy run | All ATK + your custom tests |
| Per-PR | Smoke + tests covering the changed area |
| Nightly | Full suite + FedRAMP (if 2.1) |

## Pattern

### How tests are organized

Each test exists in both runner variants with parallel IDs:

| Cypress | Playwright |
|---|---|
| `auth-login.cy.js` (`-CY-LOGIN-001`) | `auth-login.spec.js` (`-PW-LOGIN-001`) |
| `content-create.cy.js` (`-CY-CONTENT-001`) | `content-create.spec.js` (`-PW-CONTENT-001`) |

### Catalog by area

| Area | Examples |
|---|---|
| **Authentication** | Login, logout, login-with-redirect, password reset, login limits (2.1+) |
| **User management** | Create user, edit user, delete user, role assignment, role-based access checks |
| **Content** | Create node, edit node, delete node, view modes, revisions, scheduled publishing |
| **Page errors** | 403 unauthorized, 404 not found, custom error pages |
| **Administrative** | Toolbar interactions, admin pages reachable by role, configuration form submissions |
| **Forms** | Standard form submission, validation errors, AJAX interactions, multi-step forms |
| **Navigation** | Menus, breadcrumbs, primary/secondary navigation, search blocks |
| **Search (1.3+)** | Default search, search with filters, no-results handling |
| **Menu (1.3+)** | Menu link CRUD, hierarchy, position |
| **Media (1.3+)** | Image upload, `.webp` rendering, media library |
| **Email (2.0+)** | Mailtrap verification, Testmail.app integration, reroute_email assertions |
| **Feeds (2.1-beta+)** | Feeds module import workflows |
| **FedRAMP (2.1-beta+)** | Login attempt limits, CORS, session timeout, unauthorized resource access |

### Running a subset

```bash
# Playwright — by tag
npx playwright test --grep "@smoke"
npx playwright test --grep "@atk-auth"

# Playwright — by file pattern
npx playwright test e2e/atk/auth/

# Cypress
npx cypress run --spec "e2e/atk/auth/**"
```

## Common Mistakes

- **Wrong**: Running the entire catalog on every PR → **Right**: slow, reduces signal; use smoke subset per-PR
- **Wrong**: Adding ATK tests without the demo recipe → **Right**: tests reference content/users that don't exist; everything fails
- **Wrong**: Modifying ATK's shipped tests in-place → **Right**: your changes get lost on upgrade; copy and rename instead

## See Also

- [Custom Tests](atk-custom-tests.md)
- [Helper Functions](atk-helper-functions.md)
- [Installation](atk-installation.md)
- Reference: `tests/playwright/` and `tests/cypress/` in the 2.0.x branch
