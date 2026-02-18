---
topic: drupal/twig
guide: template-debugging
---

## Template Debugging

### When to Use
When you need to identify which template is rendering, what variables are available, or why output looks wrong.

### Decision
| Problem | Tool | How |
|---|---|---|
| Which template is rendering | Twig debug mode | HTML comments show template path and suggestions |
| What variables are available | `{{ dump() }}` with Devel | Shows full variable dump |
| Deep entity inspection | Kint (Devel) | `{{ kint(node) }}` — expandable tree |
| Check a specific variable | `{{ dump(variable) }}` | Prints var_dump output |
| Find template path | Debug mode HTML comments | Look for `FILE NAME SUGGESTIONS` |
| Cache not refreshing | `drush cr` | Rebuild all caches |

### Pattern

**Enable Twig debug mode (`sites/default/services.yml`):**
```yaml
parameters:
  twig.config:
    debug: true
    auto_reload: true
    cache: false
```
Never enable in production. Performance drops significantly.

**Debug output in browser source:**
```html
<!-- THEME DEBUG -->
<!-- THEME HOOK: 'node' -->
<!-- FILE NAME SUGGESTIONS:
   * node--123--full.html.twig
   * node--123.html.twig
   x node--article--full.html.twig   <- USED (x marks the winner)
   * node--article.html.twig
   * node--full.html.twig
   * node.html.twig
-->
<!-- BEGIN OUTPUT from 'themes/custom/mytheme/templates/content/node--article--full.html.twig' -->
```

**Dump in templates:**
```twig
{# Dump all available variables (requires Devel) #}
{{ dump() }}

{# Dump specific variable #}
{{ dump(node) }}
{{ dump(content.field_tags) }}

{# Kint for deep inspection (requires Devel + Kint) #}
{{ kint(node) }}
{{ kint(content) }}
```

**twig_tweak drupal_dump (doesn't require Devel kint):**
```twig
{{ drupal_dump(node) }}
{{ dd(content.field_body) }}
```

**Debugging template path (`{{ _self }}`):**
```twig
{# Output current template file path #}
{{ _self }}
```

**Inspecting render arrays in preprocess:**
```php
// In preprocess, use dsm() from Devel
dsm($variables, 'All template variables');
dsm($variables['content'], 'Content render array');
```

### Debugging Workflow
1. Enable Twig debug in `services.yml`, clear cache
2. View page source — find HTML comments showing which template is used
3. Copy the template from core/module to your theme and make changes
4. Use `{{ dump() }}` to verify available variables
5. Check the `THEME HOOK` comment to verify correct hook name for preprocess

### Common Mistakes
- Enabling debug mode in production → significant performance impact and information disclosure
- `{{ dump() }}` without Devel module → outputs nothing (function not registered)
- Looking in wrong template — debug comments show exact path; always trust the comment over assumptions
- Editing core template files instead of copying to theme → core updates overwrite your changes
- Forgetting to clear cache after adding new template files → `drush cr` required

### See Also
- Template naming → [Template Discovery & Naming](template-discovery-naming.md)
- Template suggestions → [Template Suggestions](template-suggestions.md)
