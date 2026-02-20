## 18. Security & Performance

### When to Use

When hardening Layout Builder against security issues, optimizing performance, or auditing for vulnerabilities.

### Items

#### Access Control

**Security Concern:** Blocks placed in layouts bypass normal block access if not configured correctly

**Best Practices:**
- Block plugins implement `blockAccess()` method checking user permissions
- Field blocks check entity access AND field access
- Inline blocks check block content entity access
- System blocks check module permissions

**Example:**
```php
// Field blocks automatically check access
protected function blockAccess(AccountInterface $account) {
  $entity = $this->getEntity();
  $access = $entity->access('view', $account, TRUE);

  if (!$access->isAllowed()) {
    return $access;
  }

  // Check field access
  $field = $entity->get($this->fieldName);
  return $access->andIf($field->access('view', $account, TRUE));
}
```

**Gotchas:**
- Layout Builder Restrictions is UI convenience, NOT security. Don't rely on it to hide sensitive blocks
- Custom blocks must implement access checks. Default is "allow access"
- Check both entity access and field access for field blocks

#### XSS Prevention

**Security Concern:** User-provided layout configuration could inject malicious markup

**Best Practices:**
- Never use user input directly in templates without escaping
- Block configuration goes through form API with sanitization
- Inline block content uses filtered text formats
- Layout Builder Styles classes should be validated/restricted

**Example:**
```php
// DON'T: Trusting user input
$section->setThirdPartySetting('custom', 'class', $_POST['class']);

// DO: Validate and sanitize
use Drupal\Component\Utility\Html;

$class = Html::getClass($_POST['class']);
$section->setThirdPartySetting('custom', 'class', $class);
```

**Gotchas:**
- Layout Builder Styles doesn't validate classes by default — can inject `onclick="..."` etc.
- Twig auto-escapes but concatenated variables in attributes need care
- Third-party settings bypass validation unless you implement it

#### Performance: Orphaned Inline Blocks

**Performance Concern:** Removed inline blocks remain in database, bloating storage and queries

**Impact:**
- Each orphaned block = row in `block_content` and `block_content_field_data` tables
- Usage tracking table (`inline_block_usage`) grows
- Orphans counted in views, reports, searches

**Mitigation:**
```bash
# Core cleanup via cron
drush cron

# Manual cleanup with contrib module
composer require drupal/delete_orphaned_non_reusable_blocks
drush en delete_orphaned_non_reusable_blocks
drush delete-orphaned-blocks
```

**Programmatic cleanup:**
```php
// Get orphaned block IDs
$usage_service = \Drupal::service('inline_block.usage');
$orphaned_ids = $usage_service->getUnused(100);

// Delete them
if (!empty($orphaned_ids)) {
  $storage = \Drupal::entityTypeManager()->getStorage('block_content');
  $blocks = $storage->loadMultiple($orphaned_ids);
  $storage->delete($blocks);

  // Clean up usage tracking
  $usage_service->deleteUsage($orphaned_ids);
}
```

**Gotchas:**
- Cron cleanup conservative (only truly orphaned blocks)
- Translation deletion doesn't auto-cleanup inline blocks — must handle manually
- Orphans accumulate fastest when editors experiment with layouts then revert

#### Performance: Render Caching

**Performance Concern:** Layout Builder renders many blocks per page, each potentially uncached

**Best Practices:**
- Enable render cache (core)
- Configure block-level cache max-age
- Use cache tags for invalidation
- Lazy-load images in blocks
- Avoid N+1 queries in custom blocks

**Example:**
```php
// In custom block plugin
public function build() {
  $build = [
    '#theme' => 'my_block',
    '#data' => $this->getData(),
    '#cache' => [
      'tags' => ['my_block:list'],
      'contexts' => ['url.path'],
      'max-age' => 3600,
    ],
  ];

  return $build;
}
```

**Cache Configuration:**
```yaml
# In block plugin annotation
* @Block(
*   id = "my_block",
*   admin_label = @Translation("My Block"),
*   cache = {
*     "max-age" = 3600,
*     "contexts" = {"url.path"},
*     "tags" = {"my_block:list"}
*   }
* )
```

**Gotchas:**
- Field blocks inherit field caching — configure on field formatter
- Inline blocks cache per revision
- Section rendering caches entire section — nested block cache can be redundant
- Context-based caching (user, url) creates cache variations — use sparingly

#### Performance: Query Optimization

**Performance Concern:** Loading sections, blocks, entities for every layout render

**Best Practices:**
- Use entity query access checks
- Preload referenced entities
- Avoid loading entities in loops
- Use Views for lists instead of custom queries

**Example:**
```php
// DON'T: N+1 query in block
public function build() {
  $items = [];
  $nids = [1, 2, 3, 4, 5];  // From config
  foreach ($nids as $nid) {
    $node = Node::load($nid);  // 5 queries
    $items[] = $node->label();
  }
}

// DO: Batch load
public function build() {
  $items = [];
  $nids = [1, 2, 3, 4, 5];
  $nodes = Node::loadMultiple($nids);  // 1 query
  foreach ($nodes as $node) {
    $items[] = $node->label();
  }
}
```

**Gotchas:**
- Section storage loads all sections at once (good)
- Each block plugin instantiated separately (potential overhead)
- Entity reference fields need `->referencedEntities()` preloading

#### Security: Permission Granularity

**Permission Concerns:**
- "Configure any layout" is powerful — grants full LB admin
- Override permissions per entity type/bundle
- No per-section or per-region permissions

**Permissions:**
- `configure any layout` — Administer all default layouts
- `configure editable {entity_type} {bundle} layout overrides` — Per-entity overrides
- `administer blocks` — See all blocks in LB (often needed for editors)

**Best Practices:**
- Don't grant "Configure any layout" to editors — too powerful
- Use override permissions for editorial flexibility
- Pair with Layout Builder Restrictions to limit blocks
- Consider workflow modules if layouts need approval

**Gotchas:**
- Override permission doesn't imply view permission — editors need both
- "Administer blocks" shows debug blocks in production if present
- No built-in approval workflow — overrides go live immediately

#### Performance: Layout Complexity

**Performance Concern:** Deep nesting, many sections, dozens of blocks per page

**Guidelines:**
- 2-3 sections per entity typical
- 10-15 blocks per page reasonable
- Avoid sections inside sections (not possible in core LB)
- Lazy load below-fold content

**Monitoring:**
```php
// Check section count in preprocess
function mytheme_preprocess_node(&$variables) {
  if (isset($variables['content']['_layout_builder'])) {
    $section_count = count($variables['content']['_layout_builder']);

    if ($section_count > 5) {
      \Drupal::logger('performance')->warning('Node @nid has @count sections', [
        '@nid' => $variables['node']->id(),
        '@count' => $section_count,
      ]);
    }
  }
}
```

**Gotchas:**
- Each section renders independently — caching helps
- Block count more impactful than section count
- Complex layouts with many entity references = many queries

### Common Mistakes

- **Trusting Layout Builder Restrictions for security** → It's UI convenience. Use permissions and access control
- **Not validating third-party settings** → User input in third-party settings (like LB Styles) needs validation
- **Ignoring orphaned blocks** → They accumulate silently. Monitor and cleanup regularly
- **Not configuring block cache** → Blocks default to low/no caching. Set appropriate max-age and tags
- **Granting "administer blocks" to editors** → Shows all blocks including debug/admin blocks. Use Layout Builder Restrictions instead
- **Using user context for all blocks** → Creates per-user cache, kills cache hit rate. Use sparingly
- **Not testing with slow queries log** → Enable slow query logging to find N+1 problems

### See Also

- Section 10: Layout Builder Restrictions (limiting blocks, not security)
- Section 16: Best Practices (governance and caching)
- Reference: `/core/modules/layout_builder/src/InlineBlockUsage.php` (orphan tracking)
- Reference: [Delete Orphaned Non Reusable Blocks](https://www.drupal.org/project/delete_orphaned_non_reusable_blocks)
- Reference: [OWASP guidelines](https://owasp.org/)
