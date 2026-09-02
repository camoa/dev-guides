---
description: Every recipe requires a recipe.yml file defining metadata, dependencies, extensions, configuration, inputs, and content
tldr: "Every recipe requires a `recipe.yml` file defining metadata, dependencies, extensions, configuration, inputs, and content."
drupal_version: "11.x"
---

# Recipe YAML Schema

## When to Use

> Every recipe requires a `recipe.yml` file defining metadata, dependencies, extensions, configuration, inputs, and content.

## Items: recipe.yml Keys

### name

**Type:** `string` (required)
**Description:** Human-readable recipe name
**Validation:** Cannot span multiple lines or contain control characters
**Usage Example:**
```yaml
name: 'Standard'
```

### description

**Type:** `string` (optional)
**Description:** Short description of the recipe
**Validation:** Cannot contain control characters except tabs, newlines, carriage returns
**Usage Example:**
```yaml
description: 'Provides a standard site with commonly used features pre-configured.'
```

### type

**Type:** `string` (optional)
**Description:** Recipe category for organizational purposes
**Validation:** Cannot span multiple lines or contain control characters
**Usage Example:**
```yaml
type: 'Site'
```

### recipes

**Type:** `array` (optional)
**Description:** List of recipe machine names to apply before this recipe
**Validation:** Each recipe must exist and cannot depend on itself
**Usage Example:**
```yaml
recipes:
  - basic_block_type
  - article_content_type
```
**Gotchas:** Dependencies are applied recursively; circular dependencies are prevented by validation

### install

**Type:** `array` (optional)
**Description:** List of module/theme machine names to install
**Validation:** Each extension must be available (discovered by extension discovery)
**Usage Example:**
```yaml
install:
  - image
  - node
  - path
```
**Gotchas:** Themes install after modules; already-installed extensions are skipped

### config

**Type:** `associative_array` (optional)
**Description:** Configuration to import and config actions to apply
**Sub-keys:** `import`, `strict`, `actions`
**Usage Example:**
```yaml
config:
  strict: true
  import:
    node:
      - views.view.content
  actions:
    user.role.authenticated:
      grantPermission: 'access content'
```
**Gotchas:** Import happens before actions; strict mode validates config before application

### input

**Type:** `associative_array` (optional)
**Description:** Defines user-provided values for the recipe
**Keys:** Input name → input definition
**Usage Example:**
```yaml
input:
  site_name:
    description: 'The name of the site'
    data_type: string
    default:
      source: config
      config: [system.site, name]
```
**Gotchas:** Only primitive data types supported; inputs replaced in config actions using `${input_name}` syntax

### content

**Type:** `array` (optional, reserved for future use)
**Description:** Reserved for default content configuration
**Usage Example:**
```yaml
content: []
```
**Gotchas:** Currently handled by `content/` directory; this key is validated but not actively used

### extra

**Type:** `associative_array` (optional)
**Description:** Extension-specific data keyed by extension name
**Validation:** Keys must be valid extension names
**Usage Example:**
```yaml
extra:
  my_module:
    custom_setting: value
```
**Gotchas:** Only the specified extension can access its extra data via `Recipe::getExtra()`

## Common Mistakes

- Omitting `name` → Required field, validation fails without it
- Using relative paths in recipes list → Recipe names are machine names, not paths
- Listing themes before modules in install → Themes depend on modules; runner handles order automatically but explicit theme-before-module breaks
- Misspelling config action keys → Actions silently fail if plugin ID doesn't exist
- Forgetting to install extensions that provide config being imported → Validation catches this for config actions, not always for imports

## See Also

- Previous: ← [Recipe System Overview](recipe-system-overview.md)
- Next: [Creating Your First Recipe](creating-first-recipe.md) →
- Reference: `core/lib/Drupal/Core/Recipe/Recipe.php` (parse method, validation constraints)
