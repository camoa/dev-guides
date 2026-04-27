---
description: A custom module is the last resort, not the first tool. Apply reuse, extend, create in order — CSS and config only (reuse), then contrib modules, template overrides, preprocess hooks, and hook implementations (extend), then custom module (create).
tldr: Reuse = CSS + Drupal config (zero new code). Extend = contrib modules, Twig template overrides, preprocess hooks, hook implementations (use the framework's extension points). Create = custom module only when both fail. Contrib is shared infrastructure; your template is yours to patch forever.
drupal_version: "11.x"
---

# Avoid Unnecessary Custom Modules

**What:** A custom module is the last resort, not the first tool. Apply the **reuse, extend, create** principle:

- **REUSE** what's already there: (1) CSS in the theme, (2) Drupal config (Manage Display, view modes, permissions, blocks)
- **EXTEND** through the framework's supported extension points: (3) existing core or contrib module, (4) Twig template override, (5) theme preprocess hook (only when templates alone can't do it — you need to compute or transform data), (6) hook implementations into existing modules
- **CREATE** new code paths: (7) custom module (last resort). When a custom module is genuinely necessary, minimize its security surface.

**Rationale:** Every custom module is a permanent maintenance liability — security patching, upgrade testing, code review on every change, and a new attack surface (controllers, forms, services, AJAX endpoints, permissions). The **reuse, extend, create** principle ranks options by maintenance cost and ownership:

- **Reuse first** (zero new code): CSS and config aren't "creating" — they're using systems Drupal already provides. CSS reuses the cascade. Manage Display reuses the field/view-mode system. Permissions reuse the role/access system. None of this carries code-ownership burden.
- **Extend second** (use the framework's extension points): contrib modules, template overrides, preprocess hooks, and hook implementations are all ways to extend Drupal through the supported APIs the framework documents. A contrib module is shared infrastructure — its maintainers respond to security advisories, ship Drupal-version compatibility, and absorb edge cases hundreds of sites have hit. A template override or preprocess hook lives in your theme's supported extension surface, isolated and theme-scoped. Within "extend": prefer contrib over template (shared maintenance), template over preprocess (no PHP runtime cost).
- **Create last** (new code paths you own forever): custom modules are what you'll be maintaining at 2 AM in three years. Every controller, route, form, and service is yours to patch, upgrade-test, and security-audit. Write custom code only when reuse and extension both fail.

**Why contrib before template override (within Extend)**: if a contrib does 80% of what you need with config, that's almost always a better trade than 100% in a template you own. The contrib is patched by maintainers; the template is patched by you on every Drupal upgrade.

**Why templates before preprocess (within Extend)**: a `.html.twig` override is pure presentation. It has no PHP runtime cost, no side effects, can't break caching, and a designer can review it. A preprocess hook is PHP that runs on every render of every entity of that type — it adds a maintenance surface, can introduce caching bugs (forgetting cache tags on data it pulls in), and requires PHP review even for trivial markup tweaks.

**When it applies:** Every "we need to customize X" decision. Especially when the request is presentation-only (use CSS), display-tweaking (theme template/preprocess), or behavior available via existing contrib (search drupal.org first). Also during refactoring — audit existing custom modules for ones that could be retired in favor of config + theme.

**Example:**

```
Need: Change button color on a specific block
  Wrong: Custom module to inject a CSS class via render-array alter
  Right: CSS in the theme — `.block--my-block .btn { background: ... }`

Need: Hide a field on card view, show on full
  Wrong: Custom field formatter module
  Right: Manage Display config — hide field per view mode

Need: Move a field above the title
  Wrong: hook_node_view_alter() in a custom module
  Right: Manage Display config (drag field above title) — first choice
         If display config can't do it: Twig template override
         (node--article--full.html.twig) reorders {{ content.field_x }}
         and {{ label }}
         Last theme-layer resort: preprocess hook to reorder
         $variables['content']

Need: Add a "share by email" button to articles
  Wrong: Custom module with controller, form, mailer service
  Right: Existing contrib (service_links, social_share) — already tested,
         security-patched, documented

Need: Add a custom validation rule on a specific webform
  Wrong: Custom module with FormStateInterface validator service
  Right: Webform's built-in custom validation handler (admin UI)

Need: Process an incoming external API webhook
  No theme or config-only solution exists — custom module IS justified.
  Then minimize surface:
    - Single dedicated route, predictable path, no_cache: TRUE
    - HMAC signature verification on every request (reject unauth)
    - JsonResponse only — no HTML output
    - No user-facing forms or admin UI unless required
    - No unsanitized DB writes — use entity API or parameterized queries
    - Permissions: skip "administer X" unless an admin truly manages it
    - Limit hook implementations to what the module actually needs
    - No PHP filter use; no eval(); no shell_exec()
    - Audit dependencies — every required contrib module added to your
      module is now your transitive surface
```

**Decision flowchart:**

```
Need a customization?
│
├─ REUSE — use what Drupal already provides (zero new code)
│   ├─ Is it visual only (color, spacing, layout)?
│   │   └─ YES → CSS in theme. Done.
│   └─ Is it config (Manage Display, view modes, permissions, blocks)?
│       └─ YES → Config UI + drush cex. Done.
│
├─ EXTEND — use Drupal's supported extension points
│   ├─ Does an existing core or contrib module solve it?
│   │   └─ YES → Install/configure it. Done.
│   ├─ Is it markup arrangement, conditional display, or output
│   │  structure that no contrib provides?
│   │   ├─ Can a Twig template override do it (no computed values)?
│   │   │   └─ YES → Template override (node--TYPE--VIEW.html.twig).
│   │   │            Done.
│   │   └─ Need to compute or transform variables before render?
│   │       └─ YES → Theme preprocess hook. Done.
│   └─ Does it hook into an existing module's behavior?
│       └─ YES → hook_X_alter() or hook_entity_X() in a small
│                custom module (still extend, not create — minimal
│                surface). Done.
│
└─ CREATE — none of the above? Custom module justified.
            Minimize attack surface (see security checklist above).
```
