---
description: ConfigFormBase — admin settings forms with automatic config sync
drupal_version: "11.x"
---

# Pattern: Configuration Form (ConfigFormBase)

### When to Use

**Appropriate Use Cases:**
- Admin settings forms
- System configuration pages
- Module settings (admin/config paths)
- Site-wide preferences

**When NOT to Use:**
- Non-configuration data storage → Use FormBase + custom storage
- Entity configuration → Use EntityForm
- Temporary workflow data → Use FormBase with FormState

### Implementation Pattern

**Core Example:**
- File: `/web/core/lib/Drupal/Core/Form/ConfigFormBase.php`
- Pattern: Automatic config sync via #config_target (Drupal 10.2+)
- Study: Lines 106-120 (ConfigTarget), 203-262 (typed validation)

**Contrib Example:**
- File: `/modules/contrib/ai_provider_anthropic/src/Form/AnthropicConfigForm.php`
- Pattern: Config constants, `getEditableConfigNames()`, manual save
- Shows: Traditional pattern (pre-#config_target)

**Required Configuration Files:**
1. `config/install/mymodule.settings.yml` - Default values
2. `config/schema/mymodule.schema.yml` - Typed data definition

### Modern Pattern: #config_target (Drupal 10.2+)

**Declarative Config Binding:**
```
'#config_target' property maps form elements to config properties
Automatic sync: config → form and form → config
Typed validation runs automatically from schema
```

**Benefits:**
- Less code (no manual get/set in submit)
- Automatic validation from schema constraints
- Works outside forms (recipes, programmatic config)

**Reference:**
- Documentation: [#config_target in ConfigFormBase](https://www.drupal.org/node/3373502)
- Core issue: [#3382510](https://www.drupal.org/project/drupal/issues/3382510)
- Tutorial: [QED42: Exploring #config_target](https://www.qed42.com/insights/exploring-the-new-config-target-option-in-drupal-10)

### Traditional Pattern (Pre-10.2)

**Manual Config Management:**
```
buildForm(): $config->get('setting')
submitForm(): $config->set('setting', $value)->save()
```

**Example:** AnthropicConfigForm lines 78-134

### Key Decisions

| Pattern | When to Use | Complexity |
|---------|-------------|------------|
| #config_target | Simple config mapping | Low |
| #config_target + ConfigTarget | Need transformations | Medium |
| Manual get/set | Complex logic, conditional saving | High |

**Override Detection:**
```
ConfigFormBase automatically shows override warnings
Respects config overrides (settings.php)
Use hasOverrides() to check programmatically
```

**Common Mistakes:**
- Forgetting `getEditableConfigNames()` implementation
  - **WHY BAD:** Config override detection breaks, can't determine which configs form modifies, permission system can't enforce restrictions
- Not creating schema file (validation won't work)
  - **WHY BAD:** #config_target validation fails, typed data constraints not enforced, no type checking, config import doesn't validate
- Using ConfigFormBase for non-config storage
  - **WHY BAD:** Expects config schema, requires getEditableConfigNames(), config override system confused, unnecessary complexity
- Hardcoding config names instead of constants
  - **WHY BAD:** Refactoring breaks all references, typos cause silent failures, IDE can't refactor, no autocomplete

**See Also:**
- Configuration API Guide
- Typed Data Guide (for schema constraints)
- Config Translation Guide
