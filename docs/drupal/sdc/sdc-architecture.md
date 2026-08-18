---
description: "How Drupal discovers and loads SDC components, and how replacement precedence works between themes and modules"
tldr: "Discovery recursively scans components/ directories in the active theme, base themes, and modules with no precedence between them — the component ID is provider:{basename of the .component.yml}. Precedence applies only to replacement: ComponentNegotiator picks a winner among candidates that declare replaces, active theme before base themes before module fallback."
drupal_version: "11.x"
---

# SDC Architecture

## When to Use

> Use this when you need to understand how Drupal discovers and loads components, when you're debugging component registration issues, or when you're planning component organization across modules/themes.

## Decision

**Plugin-Based Architecture:**
- Component Plugin Manager discovers components at cache rebuild.
- Recursively scans `components/` directories in modules and themes for any file matching `*.component.yml`.
- Generates the component ID as `provider:{basename of the .component.yml}` — the enclosing directory name plays no part.
- Caches component definitions for performance.

**Discovery Locations (all scanned, no precedence between them):**

| Location | Path |
|---|---|
| Active theme | `themes/{theme_name}/components/` |
| Base themes | `themes/{base_theme}/components/` |
| Modules | `modules/{module_name}/components/` |

Components are namespaced by provider, so `my_theme:card` and `my_module:card` are two distinct plugins that coexist. **Dropping a same-named component into your theme does not take over a module's component** — see the replacement rules in [Replacing Templates with SDCs](replacing-templates-with-sdcs.md).

**Precedence applies only to replacement.** `ComponentNegotiator::doNegotiate()` first filters all definitions down to those whose `replaces` key equals the requested ID, then picks a winner among *those* candidates: a theme in the active theme hierarchy wins (active theme before base themes), and a module-provided candidate is the fallback when no theme claims it. With no `replaces` declared anywhere, there are no candidates and the requested plugin ID is instantiated directly.

**Integration Points:**
- Render System: `#type => 'component'` render element.
- Asset System: Automatic library generation per component.
- Theme System: Component replacement via the `replaces` directive (themes **and** modules).
- Template System: `include()` and `embed` functions.

## Pattern

**Component ID Format:**

```
provider:component-name

Examples:
- olivero:teaser
- radix:button
- my_theme:hero-banner
- my_module:user-card
```

## Common Mistakes

- **Wrong**: Expecting nested directories to create namespaces → **Right**: The scan *is* recursive, so `components/atoms/button/button.component.yml` is found — but the ID is still `provider:button`, not `provider:atoms:button`. Subdirectories are for your own organization only, and two `.component.yml` files with the same basename under one provider collide no matter how deeply they are nested.

## See Also

- Reference: `/core/lib/Drupal/Core/Plugin/Discovery/DirectoryWithMetadataDiscovery.php:79-88` — `getIdentifier()` builds the ID from `basename($file, '.component.yml')`
- Reference: `/core/lib/Drupal/Core/Theme/ComponentNegotiator.php:72-140` — `doNegotiate()`, `maybeNegotiateByTheme()`, `maybeNegotiateByModule()`
- Reference: `/core/lib/Drupal/Core/Theme/ComponentPluginManager.php` — Discovery implementation
- [Component File Structure](component-file-structure.md)
- [Replacing Templates with SDCs](replacing-templates-with-sdcs.md)
