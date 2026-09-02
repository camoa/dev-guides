---
description: Config import specifies config to copy from extensions, strict mode controls validation of existing config
tldr: "Use `config.import` to specify config files to copy from extensions. Use `config.strict` to control validation of existing config."
drupal_version: "11.x"
---

# Config Import & Strict Mode

## When to Use

> Use `config.import` to specify config files to copy from extensions. Use `config.strict` to control validation of existing config.

The `config.import` section specifies config to copy from extensions. The `config.strict` setting controls validation of existing config.

## Steps: Import Config and Choose a Strict Mode

1. **Import all extension config** — Use wildcard to import everything
   ```yaml
   config:
     import:
       node: '*'
   ```

2. **Import specific config** — List config names explicitly
   ```yaml
   config:
     import:
       node:
         - views.view.content
         - core.entity_view_mode.node.teaser
       image:
         - image.style.medium
   ```

3. **Strict mode - boolean** — Validate all recipe config matches active
   ```yaml
   config:
     strict: true  # All config must match exactly
     strict: false # Only import config that doesn't exist
   ```

4. **Strict mode - array** — Validate only listed config
   ```yaml
   config:
     strict:
       - field.storage.node.field_image  # Database schema must match
       - node.type.article
   ```

## Decision Points: Choosing Strict Mode

| At this step... | If... | Then... |
|---|---|---|
| Config may already exist | Recipe adds to existing site | Use `strict: false` to skip existing config |
| Config must be exact | Recipe enforces schema (fields) | Use `strict: true` or list critical config in array |
| Import conflicts with actions | Action modifies imported config | Actions run after import; last action wins |

## Common Mistakes

- Using `strict: true` on sites with existing config → Recipe fails if any config doesn't match exactly; use array or false
- Forgetting strict mode defaults to true → Implicit `strict: true` causes failures on existing sites
- Importing config then modifying via actions without strict awareness → Strict validates imported config, not action results
- Listing config that doesn't exist in extension → Runtime error; validate extension provides config being imported
- Not understanding UUID/dependencies are stripped in comparison → UUIDs and empty dependencies ignored; only real differences trigger strict failures

## See Also

- Previous: ← [Extension Installation](extension-installation.md)
- Next: [Config Actions - Universal](config-actions-universal.md) →
- Reference: `core/lib/Drupal/Core/Recipe/ConfigConfigurator.php`
