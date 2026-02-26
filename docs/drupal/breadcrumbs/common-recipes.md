---
description: Ready-to-apply breadcrumb patterns — entity-type builders, menu-based breadcrumbs, per-node title overrides, multilingual, and hiding breadcrumbs
drupal_version: "11.x"
---

# Common Recipes

## When to Use

> Ready-to-apply patterns for the most frequent breadcrumb requirements. Each recipe is self-contained.

## Decision

| Scenario | Recipe |
|---|---|
| Content type always shows specific trail | Entity-type-specific builder |
| Breadcrumb follows menu structure, not URL | `menu_breadcrumb` module or custom menu-trail builder |
| Editors need per-node breadcrumb label | Easy Breadcrumb `alternative_title_field` |
| Multilingual site needs translated trail | `languages` cache context + `getTranslationFromContext()` |
| Hide breadcrumb on specific pages | `excluded_paths` config, block visibility, or alter hook |

## Pattern

**Entity-type-specific builder** (product content type):
```php
// applies():
$cacheable_metadata?->addCacheContexts(['route']);
$node = $route_match->getParameter('node');
return $route_match->getRouteName() === 'entity.node.canonical'
  && $node instanceof NodeInterface
  && $node->bundle() === 'product';

// build():
$breadcrumb->addCacheContexts(['route']);
$breadcrumb->addCacheableDependency($node);
$breadcrumb->addLink(Link::createFromRoute($this->t('Home'), '<front>'));
$breadcrumb->addLink(Link::createFromRoute($this->t('Products'), 'view.products.page_1'));
return $breadcrumb;
```
Priority: use 1004 if Easy Breadcrumb is also installed (otherwise Easy Breadcrumb wins at 1003).

**Per-node breadcrumb title override:**
1. Create text field `field_breadcrumb_title` on the content type
2. Set `alternative_title_field: field_breadcrumb_title` in Easy Breadcrumb settings
3. Supports translation — `TitleResolver::getTitle()` loads the translation for the current language

**Multilingual breadcrumbs:**
```php
// In build():
$breadcrumb->addCacheContexts(['route', 'languages:language_content']);
$translated_term = $this->entityRepository->getTranslationFromContext($term);
$breadcrumb->addCacheableDependency($translated_term);
$breadcrumb->addLink(Link::createFromRoute(
  $translated_term->getName(),
  'entity.taxonomy_term.canonical',
  ['taxonomy_term' => $term->id()]
));
```

**Hiding breadcrumbs on specific pages:**

Via Easy Breadcrumb `excluded_paths` (escape `/` as `\/`):
```
user\/login
user\/register
search
```

Via block visibility config YAML:
```yaml
visibility:
  request_path:
    id: request_path
    pages: "/checkout\n/cart\n<front>"
    negate: true
```

Via alter hook (replace `$breadcrumb` — `setLinks()` throws if links exist):
```php
function my_module_system_breadcrumb_alter(Breadcrumb &$breadcrumb, RouteMatchInterface $route_match, array $context): void {
  $breadcrumb->addCacheContexts(['route']);
  if ($route_match->getRouteName() === 'commerce_checkout.form') {
    $breadcrumb = new Breadcrumb();
    $breadcrumb->addCacheContexts(['route']);
  }
}
```

## Common Mistakes

- **Wrong**: Building a product breadcrumb at priority 100 with Easy Breadcrumb installed at 1003 → **Right**: Easy Breadcrumb wins; set your priority to 1004 or conditionally disable Easy Breadcrumb for those routes
- **Wrong**: Not invalidating the cache when an entity referenced in the trail changes → **Right**: Call `addCacheableDependency($entity)` for every entity in the trail, not just the current node
- **Wrong**: Using `menu_breadcrumb` and Easy Breadcrumb together without checking priority → **Right**: Inspect each module's `*.services.yml` to understand which wins

## See Also

- [Custom Breadcrumb Builder](custom-breadcrumb-builder.md)
- [Easy Breadcrumb Configuration](easy-breadcrumb-configuration.md)
- [Caching](caching.md)
