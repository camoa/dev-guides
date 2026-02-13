---
description: Layout Builder best practices — Layout Builder vs templates vs Paragraphs, performance, editorial UX, block integration
drupal_version: "11.x"
---

# Layout Builder Best Practices

## When to Use

> Use this when deciding between Layout Builder, Paragraphs, or page templates, or when balancing editorial flexibility with code quality and performance.

## Decision

| Use Case | Use Layout Builder | Use Page Templates | Use Paragraphs |
|----------|-------------------|-------------------|----------------|
| Marketing landing pages | ✅ Best choice | ❌ Too rigid | ⚠️ Complex UI |
| Blog posts | ⚠️ Overkill | ✅ Template sufficient | ✅ For content blocks |
| Home page | ✅ Good for flexibility | ✅ Good for consistency | ⚠️ May be complex |
| News articles | ❌ Unnecessary | ✅ Consistent structure | ✅ For rich content |
| Product pages | ⚠️ Maybe | ✅ Structured data | ✅ Variant sections |
| Per-page customization | ✅ Editor control | ❌ Requires code | ⚠️ Limited layouts |

**Block Types vs Paragraphs vs Layout Builder:**

| Requirement | Block Plugin + Layout Builder | Paragraph Type | Field + Formatter |
|-------------|------------------------------|----------------|-------------------|
| Per-page placement | ✅ Drag and drop | ❌ Needs Paragraphs + LB | ❌ Fixed field |
| Reusable across pages | ✅ Block library | ❌ Copy/paste | ❌ No |
| Content editor friendly | ✅ Visual placement | ⚠️ Complex UI | ✅ Simple form |
| Version controlled | ❌ Blocks not versioned | ✅ With node | ✅ With node |
| Translation support | ⚠️ Complex | ✅ Good | ✅ Good |
| Performance | ⚠️ More queries | ✅ Good | ✅ Best |

## Pattern

**Layout Builder Section Strategy:**

**USE BOOTSTRAP GRID (Default) — 90% of use cases:**

- Zero maintenance
- Editors understand "2-column" layout
- Responsive out of the box
- Compatible with all blocks

**CREATE CUSTOM SECTION (Advanced) — Only when:**

- Need specific markup structure not achievable with grid
- Design system has opinionated section patterns
- Need to enforce brand consistency

**SDC Organism Integration:**

**Hero Sections, Features, CTAs → Block Plugins with Layout Builder:**

```php
// Custom block renders SDC organism
public function build() {
  $build = [
    '#type' => 'component',
    '#component' => 'THEME_NAME:hero-section',
    '#props' => [
      'heading' => $this->configuration['heading'],
      'background_image' => $this->configuration['bg_image'],
    ],
  ];

  // CRITICAL: Add cache metadata
  $build['#cache'] = [
    'contexts' => ['url.path'],
    'tags' => ['config:block.block.hero'],
    'max-age' => Cache::PERMANENT,
  ];

  return $build;
}
```

**Performance: Caching Impact:**

- Without caching: ~500-1000ms per Layout Builder page
- With proper caching: ~50-100ms (10x improvement)

**BigPipe for Slow Blocks:**

```php
// Make slow blocks use BigPipe
public function build() {
  $build = [
    '#lazy_builder' => [
      'THEME_NAME.lazy_builder:buildHeroSection',
      [$this->configuration],
    ],
    '#create_placeholder' => TRUE,
  ];
  return $build;
}
```

**Content Editor Experience:**

```php
// Block form with clear labels and help text
public function blockForm($form, FormStateInterface $form_state) {
  $form['heading'] = [
    '#type' => 'textfield',
    '#title' => $this->t('Heading'),
    '#description' => $this->t('Large heading text displayed prominently.'),
    '#default_value' => $this->configuration['heading'] ?? '',
    '#required' => TRUE,
  ];

  $form['background_image'] = [
    '#type' => 'managed_file',
    '#title' => $this->t('Background Image'),
    '#description' => $this->t('Recommended size: 1920x1080px. Formats: JPG, PNG, WebP.'),
    '#upload_location' => 'public://hero-images/',
    '#upload_validators' => [
      'file_validate_extensions' => ['jpg jpeg png webp'],
      'file_validate_size' => [10 * 1024 * 1024], // 10MB
    ],
  ];

  return $form;
}
```

## Common Mistakes

- **Wrong**: Using Layout Builder when templates would work → **Right**: Use templates for consistent structure
- **Wrong**: No default layouts → **Right**: Provide sensible default layout
- **Wrong**: No caching on custom blocks → **Right**: Add `#cache` metadata
- **Wrong**: Giving all editors full Layout Builder access → **Right**: Use Layout Builder Restrictions module
- **Wrong**: Over-using Layout Builder permissions → **Right**: Limit which blocks editors can place
- **Wrong**: No help text in block forms → **Right**: Clear labels, descriptions, validation
- **Wrong**: Using minimal labels without guidance → **Right**: Help editors with descriptions and examples
- **Wrong**: Not validating uploads → **Right**: File validators prevent broken images

## See Also

- [Organisms SDC Layout Builder](organisms-sdc-layout-builder.md)
- [Templates Drupal Theme Layer](templates-drupal-theme-layer.md)
- [Performance Best Practices](performance-best-practices.md)
- Drupal Layout Builder: https://www.drupal.org/docs/8/core/modules/layout-builder
