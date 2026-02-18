---
topic: drupal/twig
guide: template-suggestions
---

## Template Suggestions

### When to Use
When you need Drupal to use a more specific template for certain conditions (specific node type, view mode, user role, etc.) without overriding the base template for all cases.

### Decision
| Approach | When | How |
|---|---|---|
| Named template file | Override for specific bundle/view mode | Create `node--article.html.twig` |
| `hook_theme_suggestions_HOOK()` | Add programmatic suggestions | Return array of suggestion strings |
| `hook_theme_suggestions_HOOK_alter()` | Add/remove suggestions from any source | Modify `$suggestions` array |
| `\|add_suggestion` Twig filter | Add suggestion from within a template | `{{ content\|add_suggestion('special') }}` |

### Pattern

**Adding suggestions via hook (module or theme):**
```php
// Adds node--article--full.html.twig as highest priority
function mymodule_theme_suggestions_node_alter(array &$suggestions, array $variables): void {
  $node = $variables['elements']['#node'];
  $view_mode = $variables['elements']['#view_mode'];
  // Add a suggestion based on node type + view mode
  $suggestions[] = 'node__' . $node->bundle() . '__' . $view_mode;
  // Add suggestion for logged-in users
  if (\Drupal::currentUser()->isAuthenticated()) {
    $suggestions[] = 'node__authenticated';
  }
}
```

**OOP version (Drupal 11.2+ modules, 11.3+ themes):**
```php
#[Hook('theme_suggestions_node_alter')]
public function themeSuggestionsNodeAlter(array &$suggestions, array $variables): void {
  // Higher index = higher priority
  $suggestions[] = 'node__' . $variables['elements']['#node']->bundle();
}
```

**Built-in node suggestions** (from `NodeThemeHooks::themeSuggestionsNode()`):
```
node__full                     (view mode)
node__article                  (bundle)
node__article__full            (bundle + view mode)
node__123                      (specific node ID)
node__123__full                (specific ID + view mode)
```

**Built-in field suggestions** (from `field.html.twig` docblock):
```
field--node--field-foo--article.html.twig
field--node--field-foo.html.twig
field--node--article.html.twig
field--field-foo.html.twig
field--text-with-summary.html.twig
field.html.twig
```

**`|add_suggestion` filter (Twig-level, Drupal 10.1+):**
```twig
{# In a template — adds block__my_special suggestion #}
{{ content|add_suggestion('my_special') }}
```

### Suggestion Priority Rules
- Suggestions are evaluated **last-to-first** — the last item in the array is highest priority
- Theme templates override module templates at the same suggestion level
- More specific (longer) suggestions take precedence over less specific ones
- Debug mode shows which suggestions were considered and which was used

### Common Mistakes
- Appending suggestion at wrong index — `$suggestions[] = ...` appends (highest priority); `array_unshift($suggestions, ...)` prepends (lowest)
- Using hyphens instead of underscores in suggestion strings: `'node__my-type'` → should be `'node__my_type'`
- Not clearing theme registry after changing suggestion hooks → `drush cr`
- Applying suggestions in `hook_theme_suggestions_HOOK()` (not `_alter`) from a theme → only `_alter` is called for themes
- The `|add_suggestion` filter replaces dashes with underscores automatically, but the template file still uses hyphens

### See Also
- Template naming → [Template Discovery & Naming](template-discovery-naming.md)
- Debug mode to see suggestions → [Template Debugging](template-debugging.md)
- Drupal API: `https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Render!theme.api.php/function/hook_theme_suggestions_HOOK_alter/11.x`
