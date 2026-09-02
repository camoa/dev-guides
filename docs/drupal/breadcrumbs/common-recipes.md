---
description: Ready-to-apply breadcrumb patterns — entity-type builders, menu-based breadcrumbs, per-node title overrides, multilingual, and hiding breadcrumbs
tldr: "Ready-to-apply patterns for the most frequent breadcrumb requirements. Each recipe is self-contained."
drupal_version: "11.x"
---

# Common Recipes

## When to Use

> Ready-to-apply patterns for the most frequent breadcrumb requirements. Each recipe is self-contained.

## Items

#### Entity-Type-Specific Breadcrumbs

For a content type `product` that should always show: Home → Products → [Product Title]:

```php
// In applies():
$cacheable_metadata?->addCacheContexts(['route']);
$node = $route_match->getParameter('node');
return $route_match->getRouteName() === 'entity.node.canonical'
  && $node instanceof NodeInterface
  && $node->bundle() === 'product';

// In build():
$breadcrumb->addCacheContexts(['route']);
$breadcrumb->addCacheableDependency($node);
$breadcrumb->addLink(Link::createFromRoute($this->t('Home'), '<front>'));
$breadcrumb->addLink(Link::createFromRoute($this->t('Products'), 'view.products.page_1'));
// Do NOT add current page link — it's convention not to self-link the current page
return $breadcrumb;
```

Priority recommendation: 100 (runs before core, yields to Easy Breadcrumb at 1003 if also installed — so either disable Easy Breadcrumb for this route or use priority 1004).

#### Menu-Based Breadcrumbs

For sites where breadcrumb should follow the menu trail, not the URL structure, use the `menu_breadcrumb` contrib module instead of a custom builder. It provides menu-trail resolution with config to specify which menus to check in priority order.

If you need custom menu-based breadcrumbs:
```php
// Use MenuLinkManager to find the menu trail
$links = $this->menuLinkManager->loadLinksByRoute($route_match->getRouteName(), $route_match->getRawParameters()->all());
if ($links) {
  $link = reset($links);
  $parents = $this->menuLinkTree->load($link->getPluginId(), new MenuTreeParameters());
  // Walk parents to build trail
}
```

#### Per-Node Breadcrumb Title Override

Use Easy Breadcrumb's `alternative_title_field`:
1. Create a text field `field_breadcrumb_title` on the content type
2. Set `alternative_title_field: field_breadcrumb_title` in Easy Breadcrumb settings
3. When a node has a value in `field_breadcrumb_title`, that is used as the breadcrumb label instead of the node title
4. Supports translation: `TitleResolver::getTitle()` loads the translation for the current language

This is the preferred approach for content editors who need to customize breadcrumb labels without changing the page title.

#### Multilingual Breadcrumbs

In a multilingual builder, add the `languages` cache context and translate entity links:

```php
// In build():
$breadcrumb->addCacheContexts(['route', 'languages:language_content']);

// For entity links, use the repository to get the translated entity
$translated_term = $this->entityRepository->getTranslationFromContext($term);
$breadcrumb->addCacheableDependency($translated_term);
$breadcrumb->addLink(Link::createFromRoute($translated_term->getName(), 'entity.taxonomy_term.canonical', ['taxonomy_term' => $term->id()]));
```

Easy Breadcrumb handles this automatically — it reads the current content language and applies it to `TitleResolver::getTitle()`.

#### Hiding Breadcrumbs on Specific Pages

Via config (Easy Breadcrumb `excluded_paths`):
```
# In easy_breadcrumb settings
excluded_paths: |
  search
  user\/login
  user\/register
```

Via block visibility (block config YAML):
```yaml
visibility:
  request_path:
    id: request_path
    pages: "/checkout\n/cart\n<front>"
    negate: true
```

Via `hook_system_breadcrumb_alter()` (when you need programmatic logic):
```php
function my_module_system_breadcrumb_alter(Breadcrumb &$breadcrumb, RouteMatchInterface $route_match, array $context): void {
  $breadcrumb->addCacheContexts(['route']);
  if ($route_match->getRouteName() === 'commerce_checkout.form') {
    $breadcrumb->setLinks([]); // Clears the breadcrumb entirely
  }
}
```

Wait — `setLinks()` throws if links are already set. To truly clear a breadcrumb in the alter hook, replace the breadcrumb object:
```php
function my_module_system_breadcrumb_alter(Breadcrumb &$breadcrumb, RouteMatchInterface $route_match, array $context): void {
  $breadcrumb->addCacheContexts(['route']);
  if ($route_match->getRouteName() === 'commerce_checkout.form') {
    $breadcrumb = new Breadcrumb();
    $breadcrumb->addCacheContexts(['route']);
    // Returns empty breadcrumb — block hides when no links
  }
}
```

## Common Mistakes

- Not invalidating the old breadcrumb cache when a node referenced in the trail changes — always `addCacheableDependency($node)` for every entity in the trail, not just the current one
- Building a product breadcrumb at priority 100 with Easy Breadcrumb also installed at 1003 — Easy Breadcrumb wins; either uninstall Easy Breadcrumb for those routes using `applies_admin_routes` or set your priority to 1004
- Using the `menu_breadcrumb` module at the same time as Easy Breadcrumb without understanding priority — check which module registers at what priority via `drush yml-preview --type=service` or inspection of `*.services.yml`

## See Also

- Custom builder full pattern → [Custom Breadcrumb Builder](custom-breadcrumb-builder.md)
- Easy Breadcrumb `alternative_title_field` → [Easy Breadcrumb Configuration](easy-breadcrumb-configuration.md)
- Caching entities in breadcrumbs → [Caching](caching.md)
