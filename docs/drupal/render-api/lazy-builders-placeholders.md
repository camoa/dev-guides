---
description: Deferring expensive or personalized rendering with lazy builders, auto-placeholdering, and Big Pipe integration.
---

# Lazy Builders & Placeholders

## When to Use

When part of your render array is **expensive to generate** or **highly dynamic** (personalized, uncacheable, time-sensitive) but the rest of the page can be cached. Lazy builders defer that part's rendering until after the page is retrieved from cache.

## How It Works

1. **Page is cached with a placeholder** instead of dynamic content
2. **Placeholder is replaced** just before sending response
3. **Dynamic part is rendered** only when needed, not on every cache hit
4. **Big Pipe** (if enabled) can stream placeholders separately, improving perceived performance

## Pattern: Basic Lazy Builder

**Define the lazy builder callback:**

```php
namespace Drupal\mymodule\Service;

class DynamicContentBuilder {

  /**
   * Lazy builder callback for current time.
   *
   * @param string $format
   *   Date format string.
   *
   * @return array
   *   Render array.
   */
  public static function buildCurrentTime($format) {
    return [
      '#markup' => '<time>' . date($format) . '</time>',
      '#cache' => ['max-age' => 0],  // Never cache
    ];
  }

}
```

**Use the lazy builder:**

```php
$build['timestamp'] = [
  '#lazy_builder' => [
    '\Drupal\mymodule\Service\DynamicContentBuilder::buildCurrentTime',
    ['Y-m-d H:i:s'],  // Arguments passed to callback
  ],
  '#create_placeholder' => TRUE,  // Generate placeholder
];
```

**Requirements for lazy builder elements:**

- Must contain ONLY: `#lazy_builder`, `#cache`, `#weight`, `#create_placeholder`
- No children allowed
- No other properties
- Arguments must be scalars (strings, ints, bools) -- no objects

**Reference:** [Use Lazy Builders and Placeholders](https://drupalize.me/tutorial/use-lazy-builders-and-placeholders)

## Pattern: Auto-Placeholdering

Drupal can automatically create placeholders for slow render array parts without explicit `#create_placeholder`.

**Conditions for auto-placeholdering:**

1. Element has `#cache['max-age'] < page max-age` (uncacheable or shorter cache)
2. Element is "expensive enough" (configurable threshold)
3. `#lazy_builder` is defined

```php
$build['personalized_greeting'] = [
  '#lazy_builder' => [
    '\Drupal\mymodule\Service\PersonalizedContent::buildGreeting',
    [$user->id()],
  ],
  '#cache' => [
    'contexts' => ['user'],  // Vary by user
    'max-age' => 0,  // Uncacheable
  ],
  // No #create_placeholder needed -- auto-placeholdered
];
```

**Reference:** [Auto-placeholdering](https://www.drupal.org/docs/drupal-apis/render-api/auto-placeholdering)

## Pattern: Lazy Builder for Personalized Content

```php
// In a block's build() method
public function build() {
  return [
    'static_part' => [
      '#markup' => '<h2>Welcome to our site</h2>',
      '#cache' => [
        'keys' => ['mymodule', 'welcome_block', 'static'],
        'max-age' => Cache::PERMANENT,
      ],
    ],
    'personalized_part' => [
      '#lazy_builder' => [
        '\Drupal\mymodule\PersonalizedBuilder::buildUserWidget',
        [],
      ],
      '#create_placeholder' => TRUE,
      '#cache' => [
        'contexts' => ['user'],
        'max-age' => 0,  // Never cache
      ],
    ],
  ];
}

// The lazy builder
public static function buildUserWidget() {
  $user = \Drupal::currentUser();

  return [
    '#theme' => 'mymodule_user_widget',
    '#username' => $user->getAccountName(),
    '#last_login' => $user->getLastLoginTime(),
    '#cache' => [
      'contexts' => ['user'],
      'max-age' => 0,
    ],
  ];
}
```

**Benefit:** The static "Welcome to our site" part is served from cache for all users; only the personalized widget is regenerated per user.

## Pattern: Big Pipe Integration

When **Big Pipe module** is enabled, placeholders stream to the browser separately, improving perceived performance.

```php
// This element will stream via Big Pipe
$build['slow_content'] = [
  '#lazy_builder' => [
    '\Drupal\mymodule\SlowBuilder::buildExpensiveContent',
    [$entity_id],
  ],
  '#create_placeholder' => TRUE,
];
```

**User experience:**

1. Page HTML loads immediately with placeholder
2. Browser renders visible content
3. Placeholder gets replaced when lazy builder finishes
4. No blocking on slow operations

**Reference:** [Drupal BigPipe - using lazy builders](https://www.droptica.com/blog/drupal-bigpipe-using-lazy-builders-2023/)

## Common Mistakes

- **Adding children or extra properties to lazy builder elements** -- Violates lazy builder requirements; element ignored or error
- **Passing objects as lazy builder arguments** -- Only scalars allowed; pass IDs and load objects in callback
- **Not setting `max-age => 0` on truly dynamic content** -- Content gets cached when it shouldn't
- **Overusing lazy builders** -- Each placeholder has overhead; only use for expensive/uncacheable parts
- **Forgetting to add cache metadata in lazy builder callback** -- Return value must have proper `#cache` metadata
- **Not understanding auto-placeholdering conditions** -- Expecting auto-placeholdering without meeting the criteria

## See Also

- [Cache Metadata in Render Arrays](cache-metadata-render-arrays.md) for cache strategy
- [Security & Performance](security-performance.md) for performance optimization
- Reference: [Using Lazy Builders and Auto Placeholders in Drupal 8](https://agileadam.com/2020/03/using-lazy-builders-and-auto-placeholders-in-drupal-8/)
