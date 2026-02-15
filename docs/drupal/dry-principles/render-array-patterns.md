---
description: Create reusable render patterns with structured render arrays, theme hooks, and render element plugins instead of duplicating markup.
---

# Render Array Patterns

## When to Use

When you need consistent rendering patterns across multiple controllers, blocks, or preprocess functions. Render arrays are Drupal's structured way to describe renderable content.

## Reusable Render Patterns

| Pattern | Use When | Example |
|---------|----------|---------|
| **Theme hooks** | Consistent markup for entity type | `node.html.twig`, `user.html.twig` |
| **Render element plugins** | Reusable form/page elements | `Textfield`, `Details`, `Container` |
| **#type shortcuts** | Common render patterns | `#type => 'link'`, `#type => 'dropbutton'` |
| **Template suggestions** | Variations of same pattern | `node--article--teaser.html.twig` |

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Render link consistently | `['#type' => 'link']` | Structured, cacheable, themeable |
| Render image consistently | `['#theme' => 'image']` | Standard image render array |
| Custom render element type | Create render element plugin | Reusable across project |
| Complex repeated markup | Theme hook + template | Centralized markup pattern |
| Entity rendering | `view_builder->view($entity)` | Consistent entity rendering |

## Pattern

```php
// WRONG: Duplicating markup in controllers/blocks
public function build() {
  return [
    '#markup' => '<a href="/node/1" class="custom-link">Link</a>',
  ];
}

// RIGHT: Structured render array
public function build() {
  return [
    '#type' => 'link',
    '#title' => $this->t('Link'),
    '#url' => Url::fromRoute('entity.node.canonical', ['node' => 1]),
    '#attributes' => ['class' => ['custom-link']],
  ];
}
```

```php
// Reusable render array factory method (service)
class RenderHelper {

  public function buildCard(string $title, array $content): array {
    return [
      '#theme' => 'mymodule_card',
      '#title' => $title,
      '#content' => $content,
      '#cache' => [
        'contexts' => ['user.permissions'],
      ],
    ];
  }
}

// Use in multiple controllers/blocks
$build[] = $this->renderHelper->buildCard('Title', $content);
```

Reference: `core/lib/Drupal/Core/Render/Element/`, `core/modules/node/node.module` (theme hooks), `core/lib/Drupal/Core/Render/theme.api.php`

## Common Mistakes

- **Hardcoded HTML in #markup** — Use structured render arrays (`#type`, `#theme`) for themability and cacheability
- **Duplicating render array structures** — Create helper methods or services for repeated patterns
- **Not setting cache metadata** — Always set `#cache` contexts, tags, max-age for proper caching
- **Rendering entities manually** — Use `entity_type.view_builder` service to render entities
- **Ignoring existing #type options** — Check core render elements before creating custom ones

## See Also

- [SDC Component Reuse](sdc-component-reuse.md)
- [Hook and Event Reuse](hook-event-reuse.md)
- Reference: [Render API overview | Drupal.org](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Render!theme.api.php/group/theme_render/11.x)
- Reference: [Render arrays | Drupal at your Fingertips](https://www.drupalatyourfingertips.com/render)
