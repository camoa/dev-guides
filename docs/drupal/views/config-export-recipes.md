---
description: When managing views as exportable configuration, deploying via config sync, or packaging in recipes.
drupal_version: "11.x"
---

## 17. Views Config Export & Recipes

### When to Use
When managing views as exportable configuration, deploying via config sync, or packaging in recipes.

### Workflow: Exporting Views to Config

#### Step 1: Create/Modify View in UI
Build view in Views UI (`/admin/structure/views`).

#### Step 2: Export Single View
```bash
drush config:export --destination=/tmp/config views.view.my_view
```

Exports to `/tmp/config/views.view.my_view.yml`.

Or export all config:
```bash
drush config:export
```

Exports all config to `config/sync/` directory.

#### Step 3: Commit to Version Control
```bash
git add config/sync/views.view.my_view.yml
git commit -m "Add custom articles listing view"
```

#### Step 4: Import on Other Environments
```bash
drush config:import
```

Imports all config from `config/sync/`.

Reference: [Drupal Configuration API](https://www.drupal.org/docs/drupal-apis/configuration-api/configuration-schemametadata)

### Recipe Pattern: Packaging Views

#### Recipe Structure
```
my_recipe/
  recipe.yml
  config/
    views.view.my_view.yml
```

#### recipe.yml
```yaml
name: 'Article Listing Recipe'
description: 'Adds article listing views'
type: 'Content'
config:
  import:
    views:
      - views.view.articles_listing
      - views.view.articles_block
```

#### Conditional Config (Optional vs Required)
Views in `/config/install/` → **Required** (installed with module)
Views in `/config/optional/` → **Installed only if dependencies exist**

Example: View with taxonomy dependency
```
my_module/
  config/
    optional/
      views.view.tagged_content.yml  # Only installs if taxonomy module enabled
```

Reference: `core/modules/node/config/optional/views.view.content.yml` (core example)

### Pattern: View Dependencies
```yaml
dependencies:
  module:
    - node
    - user
    - taxonomy
```

When exporting, Views automatically calculates dependencies based on:
- Base table module
- Field modules
- Plugin provider modules
- Relationship entity types

Reference: `core/modules/views/src/Entity/View.php` lines 271-287

### Config Actions in Recipes (Drupal 11+)

#### Create View from Scratch
```yaml
config:
  actions:
    views.view.my_view:
      createIfNotExists:
        langcode: en
        status: true
        id: my_view
        label: 'My Custom View'
        module: views
        base_table: node_field_data
        display:
          default:
            # ... full config
```

#### Modify Existing View
```yaml
config:
  actions:
    views.view.content:
      ensure:
        display.page_1.display_options.pager.options.items_per_page: 25
```

### Common Mistakes
- Exporting view without dependencies → Import fails on other environment; always check `dependencies` key
- Hardcoding UUIDs in view config → UUIDs differ across environments; Views config doesn't include UUIDs by design
- Putting views in `/config/install/` with optional dependencies → Install fails if dependency missing; use `/config/optional/`
- Not testing config import on clean site → View relies on manual DB state; always test on fresh install
- Editing exported YAML and breaking schema → Validate against schema or import will fail silently

### See Also
- Section 2: View Config Schema — understanding YAML structure
- Reference: [Defining Configuration in Drupal](https://www.drupal.org/docs/develop/creating-modules/defining-and-using-your-own-configuration-in-drupal)
