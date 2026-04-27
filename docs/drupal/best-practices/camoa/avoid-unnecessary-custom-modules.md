---
description: A custom module is the last resort, not the first tool. Apply reuse, extend, create in order — CSS, config, existing contrib, Twig template, preprocess, then custom module. When a module is necessary, minimize its security surface.
tldr: Apply reuse, extend, create in order — CSS/config/existing-contrib first (reuse), then Twig template override and preprocess hooks (extend), then custom module (create). Contrib is shared infrastructure; your template is yours to patch forever.
drupal_version: "11.x"
---

# Avoid Unnecessary Custom Modules

**What:** A custom module is the last resort, not the first tool. Apply the **reuse, extend, create** principle in order: (1) CSS in the theme, (2) Drupal config (Manage Display, view modes, permissions, blocks), (3) reuse — existing core or contrib module that solves the problem (often via its own config UI), (4) extend through the theme layer — Twig template override, (5) extend through preprocess — theme preprocess hook (only when templates alone can't do it; you need to compute or transform data), (6) create — custom module (last resort). When a custom module is genuinely necessary, minimize its security surface.

**Rationale:** Every custom module is a permanent maintenance liability — security patching, upgrade testing, code review on every change, and a new attack surface (controllers, forms, services, AJAX endpoints, permissions). The **reuse, extend, create** principle ranks options by maintenance cost:

- **Reuse first**: a contrib module already used by thousands of sites has been audited, fuzz-tested, security-patched, and documented in ways your custom code never will be. Adding a well-maintained contrib dependency carries less long-term cost than writing the equivalent yourself — even if "writing the equivalent" is just a Twig template.
- **Extend second**: when no module fits, extend the system through its supported extension points — config, templates, preprocess hooks. These layers are isolated, theme-scoped, and don't introduce new module surface.
- **Create last**: write custom modules only when reuse and extension both fail. Custom code is what you'll be maintaining at 2 AM in three years.

**Templates before preprocess**: Twig template overrides are pure presentation with no PHP runtime cost or side effects; preprocess hooks run on every render of every entity of that type and add a PHP maintenance surface. Reach for preprocess only when the template alone genuinely can't do it (you need to compute, transform, or fetch additional data).

**Config and CSS are "reuse" not "create"**: setting `display_label: hidden` in Manage Display is reusing Drupal's display system; writing `.field--name { display: none }` is reusing the CSS cascade. Neither creates new code paths.

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
├─ REUSE — Is it visual only (color, spacing, layout)?
│   └─ YES → CSS in theme. Done.
│
├─ REUSE — Is it config (fields, view displays, permissions, blocks)?
│   └─ YES → Config UI + drush cex. Done.
│
├─ REUSE — Does an existing core or contrib module solve it?
│   └─ YES → Install/configure it (its config UI is reuse, not creation).
│            Done.
│
├─ EXTEND — Is it markup arrangement, conditional display, or output
│           structure that no contrib provides?
│   ├─ Can a Twig template override do it (no computed values needed)?
│   │   └─ YES → Template override (node--TYPE--VIEW.html.twig). Done.
│   └─ Need to compute or transform variables before render?
│       └─ YES → Theme preprocess hook (last theme-layer option). Done.
│
└─ CREATE — None of the above? Custom module justified.
            Minimize attack surface (see security checklist above).
```

**Why reuse before extend**: a contrib module is shared infrastructure.
Maintainers respond to security advisories, ship Drupal-version
compatibility, and absorb edge cases hundreds of sites have hit. Your
template override is yours alone — you ship it, you patch it, you
re-test it on every Drupal upgrade. If a contrib does 80% of what you
need with config, that's almost always a better trade than 100% in a
template you own.

**Why templates before preprocess**: a `.html.twig` override is pure
presentation. It has no PHP runtime cost, no side effects, can't break
caching, and a designer can review and edit it. A preprocess hook is
PHP that runs on every render of every entity of that type — it adds a
maintenance surface, can introduce caching bugs (forgetting cache tags
on data it pulls in), and requires PHP review even for trivial markup
tweaks. Preprocess is correct when you genuinely need to compute,
transform, or fetch additional data; if you're only moving HTML around,
it's the wrong tool.
