---
description: Drupal 11 multilingual changes — content_translation.admin.inc deprecation, compatibility checking, migration paths
---

# Drupal 11 Changes & Deprecations

### When to Use
When upgrading to Drupal 11 or maintaining modules compatible with Drupal 11.x.

### Decision: Migration Path

| Deprecated element | Replacement | Action required |
|---|---|---|
| `content_translation.admin.inc` functions | Functions moved to `content_translation.module` | Update function calls (path changes, signatures same) |
| `t()` global function (still works) | `$this->t()` via StringTranslationTrait | Refactor for best practices (not breaking) |

### Pattern: content_translation.admin.inc Deprecation

**Deprecated in**: Drupal 11.4.0
**Removed in**: Drupal 12.0.0

**Background**:
- `content_translation.admin.inc` contained helper functions for field sync UI
- Functions moved to `content_translation.module`
- File deprecated, will be removed in Drupal 12

**Affected function**:
- `content_translation_field_sync_widget()`

**Migration**:

```php
// OLD (deprecated)
include_once \Drupal::root() . '/core/modules/content_translation/content_translation.admin.inc';
$widget = content_translation_field_sync_widget($field);

// NEW (Drupal 11.4+)
// Function now in content_translation.module (auto-loaded)
$widget = content_translation_field_sync_widget($field);
```

**If you directly included the file**, remove the `include_once`:

```php
// Remove this line
include_once \Drupal::root() . '/core/modules/content_translation/content_translation.admin.inc';

// Function still available
$widget = content_translation_field_sync_widget($field);
```

**Most modules won't be affected** — function auto-loaded from `.module` file.

### Pattern: Best Practices Updates (Non-Breaking)

**t() function** — still works but discouraged in new code:

```php
// OLD (still works, not deprecated)
$message = t('Hello, world!');

// NEW (best practice)
use Drupal\Core\StringTranslation\StringTranslationTrait;

class MyClass {
  use StringTranslationTrait;

  public function myMethod() {
    $message = $this->t('Hello, world!');
  }
}
```

**Reason**: `$this->t()` is testable, mockable, dependency-injectable.

### Pattern: Checking for Drupal 11 Compatibility

**Module compatibility**:

```yaml
# mymodule.info.yml
name: My Module
core_version_requirement: ^10 || ^11
```

**Check for deprecated code**:

```bash
# Use Drupal Check or PHPStan
composer require --dev mglaman/drupal-check
vendor/bin/drupal-check modules/custom/mymodule

# Or PHPStan with Drupal extension
composer require --dev phpstan/phpstan drupal/core-dev
vendor/bin/phpstan analyze modules/custom/mymodule
```

### Known Issues & Changes

**Twig 3.x** (Drupal 11.x uses Twig 3):
- Stricter syntax checking
- Some deprecated Twig 2 patterns removed
- Update custom Twig extensions if any

**Symfony 6.4 / 7.x**:
- Drupal 11 uses newer Symfony components
- Some Symfony APIs changed
- Check custom services using Symfony components

**jQuery updates**:
- Drupal 11 updates jQuery version
- Some jQuery plugins may need updates
- Test custom JavaScript libraries

**No major translation system changes** — core translation architecture stable between Drupal 10 and 11.

### Common Mistakes

- **Not testing after Drupal 11 upgrade** → Even non-deprecated code may behave differently. Test all translation workflows
- **Ignoring deprecation warnings** → Drupal logs deprecation warnings. Monitor logs and fix before Drupal 12
- **Not checking contrib module compatibility** → TMGMT and other translation modules may need updates for Drupal 11
- **Assuming all APIs unchanged** → Some edge case APIs changed. Review change records at https://www.drupal.org/list-changes/drupal

### See Also
- → [Interface Translation](interface-translation.md) — .po file management (unchanged)
- → [Translating Custom Modules](translating-custom-modules.md) — best practices
- Reference: https://www.drupal.org/project/drupal/issues/3560560 (deprecated message fix)
- Reference: https://www.drupal.org/docs/understanding-drupal/how-drupal-11-is-made-and-what-is-included (Drupal 11 overview)
