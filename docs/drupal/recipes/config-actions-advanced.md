---
description: Complex config action scenarios including wildcards, optional config, chaining, and input substitution
tldr: "Use advanced config action patterns when you need wildcards for bulk operations, optional config handling, chaining multiple actions, or input substitution."
drupal_version: "11.x"
---

# Config Actions - Advanced Patterns

## When to Use

> Use advanced config action patterns when you need wildcards for bulk operations, optional config handling, chaining multiple actions, or input substitution.

Complex config action scenarios: wildcards, optional config, chaining, input substitution.

## Steps: Wildcards, Optional Config, Substitution and Chaining

1. **Wildcards for bulk operations** — Target multiple entities with patterns
   ```yaml
   config:
     actions:
       user.role.*:
         grantPermission: 'access content'
       core.entity_view_display.node.*.default:
         setComponent:
           name: created
           options: { type: timestamp, weight: 10 }
   ```

2. **Optional config actions** — Prefix with `?` to skip if config doesn't exist
   ```yaml
   config:
     actions:
       ?block.block.legacy_block:
         setProperties:
           status: false
   ```

3. **Input substitution** — Use `${input_name}` in config names or values
   ```yaml
   input:
     theme_name:
       data_type: string
       default: { source: value, value: olivero }
   config:
     actions:
       block.block.${theme_name}_search:
         placeBlockInRegion:
           region: header
           theme: ${theme_name}
   ```

4. **Chaining actions** — Multiple actions on same config entity
   ```yaml
   config:
     actions:
       user.role.editor:
         createIfNotExists:
           label: 'Editor'
         grantPermissions:
           - 'access content'
           - 'access toolbar'
         setProperties:
           weight: 5
   ```

5. **Drupal token substitution** — Use Drupal tokens in config values (separate from `${input}` syntax)
   ```yaml
   config:
     actions:
       metatag.metatag_defaults.node:
         simpleConfigUpdate:
           tags.og_title: '[node:title]'
           tags.og_url: '[site:url]/node/[node:nid]'
   ```
   Token syntax `[entity:field]` is processed by Drupal's token system at runtime, not at recipe apply time. Only useful for config values that support tokens (metatag, pathauto, etc.).

6. **Create entities then configure** — Use createIfNotExists before entity-specific actions
   ```yaml
   config:
     actions:
       core.entity_form_display.node.article.default:
         createIfNotExists:
           targetEntityType: node
           bundle: article
           mode: default
         setComponents:
           - name: body
             options: { type: text_textarea_with_summary }
   ```

## Decision Points: Choosing an Advanced Pattern

| At this step... | If... | Then... |
|---|---|---|
| Config may not exist | Action should be optional | Prefix config name with `?` |
| Multiple entities need same action | Entities share config prefix pattern | Use wildcards like `user.role.*` |
| Action values vary by input | Recipe needs environment flexibility | Use `${input_name}` substitution |
| Actions must run in sequence | Later action depends on earlier | YAML order matters; earlier actions run first |

## Common Mistakes

- Using wildcards with optional prefix → `?user.role.*` is invalid; wildcards and optional are mutually exclusive
- Forgetting input values are strings → `${site_name}` is always string; no type coercion for integers/booleans
- Not testing wildcard patterns → Wildcards only match existing config; create first, then wildcard-modify
- Assuming action order doesn't matter → YAML dict order is preserved; actions run in declaration order
- Missing createIfNotExists before entity-specific actions → Entity must exist or be created in same recipe

## See Also

- Previous: ← [Config Actions - Entity-Specific](config-actions-entity-specific.md)
- Next: [Input System - Defining Inputs](input-defining.md) →
- Reference: `core/lib/Drupal/Core/Config/Action/ConfigActionManager.php` (applyAction method)
