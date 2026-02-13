---
description: You're deciding between Layout Builder, Paragraphs, or page templates
drupal_version: "11.x"
---

## 6.4 Layout Builder Best Practices

### When to Use This Section
- You're deciding between Layout Builder, Paragraphs, or page templates
- You need guidance on when Layout Builder makes sense vs traditional theming
- You're implementing Layout Builder with SDC components
- You want to balance editorial flexibility with code quality

### Layout Builder vs Page Templates vs Paragraphs

#### Decision Framework: Which Approach?

| Use Case | Use Layout Builder | Use Page Templates | Use Paragraphs |
|----------|-------------------|-------------------|----------------|
| **Marketing landing pages** | ✅ Best choice | ❌ Too rigid | ⚠️ Complex UI |
| **Blog posts** | ⚠️ Overkill | ✅ Template sufficient | ✅ For content blocks |
| **Home page** | ✅ Good for flexibility | ✅ Good for consistency | ⚠️ May be complex |
| **News articles** | ❌ Unnecessary | ✅ Consistent structure | ✅ For rich content |
| **Product pages** | ⚠️ Maybe | ✅ Structured data | ✅ Variant sections |
| **Per-page customization** | ✅ Editor control | ❌ Requires code | ⚠️ Limited layouts |

**LAYOUT BUILDER — WHEN TO USE:**
- Content editors need drag-and-drop page building
- Different page instances need different layouts
- Marketing team wants landing page control without developer involvement
- You have reusable section/block components

**PAGE TEMPLATES — WHEN TO USE:**
- Consistent structure across all pages of a type
- Developer-controlled layout
- High performance requirement (Layout Builder adds overhead)
- Simple content display (blog posts, articles)

**PARAGRAPHS — WHEN TO USE:**
- Rich content within a specific field
- Consistent page structure but flexible content sections
- Need version control on content blocks
- Want structured data for each section type

---

### Layout Builder Section Strategy

#### Pattern: When Custom Sections Make Sense

**USE BOOTSTRAP GRID (Default):**

```yaml
# Let Layout Builder use Bootstrap sections
# No custom code needed
```

**ADVANTAGES:**
- Zero maintenance
- Editors understand "2-column" layout
- Responsive out of the box
- Compatible with all blocks

**WHEN SUFFICIENT:** 90% of use cases

---

**CREATE CUSTOM SECTION (Advanced):**

**File: `config/install/layout_builder.layout.custom_hero_section.yml`**

```yaml
id: custom_hero_section
label: Hero Section Layout
category: Custom
template: layout/hero-section-layout
icon_map:
  - ["hero_content"]
regions:
  hero_content:
    label: Hero Content
```

**WHEN TO CREATE CUSTOM SECTION:**
- Need specific markup structure not achievable with grid
- Design system has opinionated section patterns
- Need to enforce brand consistency

**WHEN NOT TO:** If Bootstrap grid can achieve same result with less code.

---

### Block Types vs Paragraphs vs Layout Builder

#### Decision Matrix

| Requirement | Block Plugin + Layout Builder | Paragraph Type | Field + Formatter |
|-------------|------------------------------|----------------|-------------------|
| **Per-page placement** | ✅ Drag and drop | ❌ Needs Paragraphs + LB | ❌ Fixed field |
| **Reusable across pages** | ✅ Block library | ❌ Copy/paste | ❌ No |
| **Content editor friendly** | ✅ Visual placement | ⚠️ Complex UI | ✅ Simple form |
| **Version controlled** | ❌ Blocks not versioned | ✅ With node | ✅ With node |
| **Translation support** | ⚠️ Complex | ✅ Good | ✅ Good |
| **Performance** | ⚠️ More queries | ✅ Good | ✅ Best |

**RECOMMENDATION FOR SDC ORGANISMS:**

**Hero Sections, Features, CTAs → Block Plugins with Layout Builder**

```php
// Custom block renders SDC organism
public function build() {
  return [
    '#type' => 'component',
    '#component' => 'THEME_NAME:hero-section',
    '#props' => [
      'heading' => $this->configuration['heading'],
      'background_image' => $this->configuration['bg_image'],
    ],
  ];
}
```

**WHY:** Reusable, drag-and-drop placement, integrates with design system.

**Rich Content Sections → Paragraphs**

```yaml
# Paragraph type: "content_section"
# Fields: heading, body, image, CTA button
```

**WHY:** Version controlled with node, better for content that changes frequently.

**Structured Data → Field + Field Formatter**

```php
// Custom field formatter renders SDC
public function viewElements(FieldItemListInterface $items, $langcode) {
  foreach ($items as $item) {
    $elements[] = [
      '#type' => 'component',
      '#component' => 'THEME_NAME:data-card',
      '#props' => ['title' => $item->title, 'value' => $item->value],
    ];
  }
  return $elements;
}
```

**WHY:** Tightly coupled to content structure, best performance.

---

### Performance Considerations

#### Pattern: Caching Layout Builder Content

**PROBLEM:** Layout Builder generates many render arrays and database queries.

**SOLUTION:** Proper cache metadata on blocks

```php
/**
 * Custom block plugin
 */
public function build() {
  $build = [
    '#type' => 'component',
    '#component' => 'THEME_NAME:hero-section',
    '#props' => ['heading' => $this->configuration['heading']],
  ];

  // CRITICAL: Add cache metadata
  $build['#cache'] = [
    'contexts' => ['url.path'],  // Vary by page
    'tags' => ['config:block.block.hero'],  // Invalidate when block config changes
    'max-age' => Cache::PERMANENT,  // Cache permanently until invalidated
  ];

  return $build;
}
```

**WHY:**
- **Cache contexts** — Different cache per URL, user role, etc.
- **Cache tags** — Invalidate when specific data changes
- **Max-age** — How long to cache

**PERFORMANCE IMPACT:**
- Without caching: ~500-1000ms per Layout Builder page
- With proper caching: ~50-100ms (10x improvement)

#### Pattern: BigPipe Integration

**Drupal automatically uses BigPipe for Layout Builder**, but you can optimize:

```php
// Make slow blocks use BigPipe
public function build() {
  $build = [
    '#lazy_builder' => [
      'THEME_NAME.lazy_builder:buildHeroSection',
      [$this->configuration],
    ],
    '#create_placeholder' => TRUE,  // Forces BigPipe placeholder
  ];
  return $build;
}
```

**WHEN TO USE:**
- Block has slow external API call
- Block has expensive database query
- Block has user-specific content

**WHY:** Page shell loads immediately, slow block loads separately.

---

### Content Editor Experience

#### CRITICAL PRINCIPLE: Don't Sacrifice Editorial UX for Code Cleanliness

**GOOD PRACTICE:**

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

**WHY:**
- **Clear labels** — Editors know what to enter
- **Help text** — Guidance prevents mistakes
- **Validation** — Prevents broken images
- **Smart defaults** — Reduces configuration burden

**BAD PRACTICE:**

```php
// Minimal labels, no help, no validation
$form['heading'] = [
  '#type' => 'textfield',
  '#title' => 'Heading',
];

$form['bg'] = [
  '#type' => 'textfield',
  '#title' => 'BG',
];
```

**WHY BAD:** Editors don't know what to enter, make mistakes, require training.

---

### Common Mistakes Senior Themers Catch

**1. Using Layout Builder when templates would work**

```yaml
# BAD: Enabling Layout Builder for News articles
# News articles all have same structure, editors don't need layout control
```

**WHY BAD:**
- Performance overhead for no benefit
- Editors overwhelmed by unnecessary options
- Content structure inconsistency risk

**WHEN CAUGHT:** "This content type has consistent structure. Why add Layout Builder complexity?"

---

**2. Not providing default layouts**

```php
// BAD: Enabling Layout Builder with no default
# Editors see blank page, have to build from scratch every time
```

**CORRECT:**

```yaml
# Provide sensible default layout
# Editors can customize if needed but have starting point
```

**WHY:** Default layouts save editor time and ensure consistency.

---

**3. No caching on custom blocks**

```php
// BAD: Block builds expensive query every page load
public function build() {
  $nodes = \Drupal::entityQuery('node')
    ->condition('type', 'article')
    ->range(0, 10)
    ->execute();

  // No cache metadata!
  return ['#markup' => $this->renderNodes($nodes)];
}
```

**CORRECT:**

```php
public function build() {
  $build = ['#markup' => $this->renderNodes($nodes)];

  $build['#cache'] = [
    'tags' => ['node_list:article'],
    'contexts' => ['url.path'],
    'max-age' => 3600,  // Cache 1 hour
  ];

  return $build;
}
```

**WHEN CAUGHT:** "Why is Layout Builder so slow?" — Missing cache metadata.

---

**4. Over-using Layout Builder permissions**

```yaml
# BAD: Giving all editors full Layout Builder access
# Editors accidentally break layouts, need constant support
```

**CORRECT:**

```yaml
# Use Layout Builder Restrictions module
# Limit which blocks editors can place
# Provide curated set of safe blocks
```

**WHY:** Too much power = too many support tickets.

---

**5. Not integrating SDC organisms properly**

```php
// BAD: Rendering component HTML in block
public function build() {
  return [
    '#markup' => '<div class="hero">...</div>',  // Hardcoded HTML
  ];
}
```

**CORRECT:**

```php
// GOOD: Use SDC rendering
public function build() {
  return [
    '#type' => 'component',
    '#component' => 'THEME_NAME:hero-section',
    '#props' => $this->configuration,
  ];
}
```

**WHY:** SDC integration maintains design system consistency.

#### See Also
- [5.3 Layout Builder Integration](#53-layout-builder-integration)
- Drupal Layout Builder: https://www.drupal.org/docs/8/core/modules/layout-builder
- Layout Builder Restrictions: https://www.drupal.org/project/layout_builder_restrictions