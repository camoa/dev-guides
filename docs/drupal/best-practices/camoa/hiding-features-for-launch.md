---
description: When temporarily removing a feature for launch, preserve all code — use view templates or #access = FALSE to hide it, and document the re-enable path in comments.
drupal_version: "11.x"
tldr: When temporarily removing a feature for launch (or a specific milestone), preserve all code. Use display-specific view templates that skip the feature, hide form elements with `#access = FALSE` in form alter hooks, keep the original template/CSS/JS intact, and document how to re-enable in code comments.
---

# Hiding Features for Launch

**What:** When temporarily removing a feature for launch (or a specific milestone), preserve all code. Use display-specific view templates that skip the feature, hide form elements with `#access = FALSE` in form alter hooks, keep the original template/CSS/JS intact, and document how to re-enable in code comments.

**Rationale:** "Temporary" features that get deleted always need to come back, and the engineering cost of rebuilding from scratch dwarfs the cost of leaving dormant code. Preserving code with a clear hide-mechanism keeps the original intent visible, lets QA test the feature in non-production environments, and turns "re-enable for v2" into a config flip rather than a re-implementation.

**When it applies:** Pre-launch decisions to ship a reduced scope, A/B testing where the off-variant returns later, seasonal features, region-specific content variants. NOT a substitute for genuinely deleting unused code — features that will never return should be removed.

**Example:**

```php
// theme.theme — hide a field via display-specific template
function mytheme_theme_suggestions_node_alter(array &$suggestions, array $variables) {
  if ($variables['elements']['#view_mode'] === 'full' &&
      $variables['elements']['#node']->bundle() === 'article') {
    $suggestions[] = 'node__article__full__launch';   // uses node--article--full--launch.html.twig
  }
}

// node--article--full--launch.html.twig — copy of node--article--full but with the launched-only fields
// {{ content|without('field_recommendations') }}
// (To re-enable for v2: delete this template; the original node--article--full kicks back in.)
```

```php
// Hide a form element until v2
function mymodule_form_node_article_form_alter(&$form, $form_state) {
  // LAUNCH-HIDDEN: This field is intentionally suppressed for v1 launch.
  // To re-enable: delete this block; the field becomes editable again.
  // Tracked in PROJECT-1234.
  if (isset($form['field_recommendations'])) {
    $form['field_recommendations']['#access'] = FALSE;
  }
}
```
