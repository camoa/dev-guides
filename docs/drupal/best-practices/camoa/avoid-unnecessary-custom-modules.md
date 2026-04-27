---
description: A custom module is the last resort, not the first tool. Try CSS, Twig template overrides, theme preprocess, or contrib before creating custom code. When a module is necessary, minimize its security surface.
tldr: A custom module is the last resort — try CSS, Twig template overrides (before preprocess hooks), config-only solutions, and existing contrib before creating custom code. Templates beat preprocess because they have no PHP runtime cost, no caching risk, and no maintenance surface.
drupal_version: "11.x"
---

# Avoid Unnecessary Custom Modules

**What:** A custom module is the last resort, not the first tool. Try in order: (1) CSS in the theme, (2) Twig template overrides, (3) theme preprocess hooks (only when templates alone can't do it), (4) extend/reuse existing core or contrib via config, (5) only then a custom module. When a custom module is genuinely necessary, minimize its security surface.

**Rationale:** Every custom module is a permanent maintenance liability — security patching, upgrade testing, code review on every change, and a new attack surface (controllers, forms, services, AJAX endpoints, permissions). CSS and theme changes are isolated, easy to roll back, and don't require module-level concerns. **Templates before preprocess**: Twig template overrides are pure presentation with no PHP runtime cost or side effects; preprocess hooks run on every render of every entity of that type and add a maintenance surface. Reach for preprocess only when the template alone genuinely can't do it. Config-only solutions are exportable, reviewable, and survive module changes. The "extend, reuse, create" principle: extend what exists (templates, preprocess, config) before reusing (contrib modules), and create (custom code) only when both fail. A contrib module already used by hundreds of sites has been audited, fuzz-tested, and security-patched in ways your custom code never will be.

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
├─ Is it visual only (color, spacing, layout)?
│   └─ YES → CSS in theme. Done.
├─ Is it config (fields, view displays, permissions, blocks)?
│   └─ YES → Config UI + drush cex. Done.
├─ Is it markup arrangement, conditional display, or output structure?
│   ├─ Can a Twig template override do it (no computed values needed)?
│   │   └─ YES → Template override (node--TYPE--VIEW.html.twig). Done.
│   └─ Need to compute or transform variables before render?
│       └─ YES → Theme preprocess hook (last theme-layer option). Done.
├─ Does an existing core or contrib module solve it?
│   └─ YES → Use it. Possibly extend via hooks. Done.
└─ NO to all → Custom module justified. Minimize attack surface.
```

**Why templates before preprocess**: a `.html.twig` override is pure
presentation. It has no PHP runtime cost, no side effects, can't break
caching, and a designer can review and edit it. A preprocess hook is
PHP that runs on every render of every entity of that type — it adds a
maintenance surface, can introduce caching bugs (forgetting cache tags
on data it pulls in), and requires PHP review even for trivial markup
tweaks. Preprocess is correct when you genuinely need to compute,
transform, or fetch additional data; if you're only moving HTML around,
it's the wrong tool.
