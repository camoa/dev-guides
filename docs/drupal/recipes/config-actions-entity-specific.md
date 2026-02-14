---
description: Config actions for specific entity types derived from ActionMethod attributes on entity methods
drupal_version: "11.x"
---

# Config Actions - Entity-Specific

## When to Use

> Use entity-specific config actions when you need to configure roles, text formats, displays, workflows, or other specialized entity types.

## Decision

| Entity Type | Action | Use For |
|-------------|--------|---------|
| user.role.* | grantPermission(s) | Grant single or multiple permissions |
| user.role.* | grantPermissionsForEachNodeType | Grant permissions with %bundle placeholder |
| user.role.* | revokePermission(s) | Revoke single or multiple permissions |
| filter.format.* | setFilterFormat | Configure text format filter plugins |
| editor.editor.* | setEditorImageUpload | Configure image upload settings for WYSIWYG |
| editor.editor.* | addItemToToolbar | Add button to CKEditor 5 toolbar |
| core.entity_form_display.* | setComponent(s) | Configure field widget display |
| core.entity_view_display.* | setComponent(s) | Configure field formatter display |
| core.entity_*_display.* | removeComponent | Hide field from display |
| field.field.* | addToAllBundles | Add field to all bundles of entity type |
| workflows.workflow.* | addNodeTypes | Add content types to workflow |
| workflows.workflow.* | addTaxonomyVocabularies | Add vocabularies to workflow |
| block.block.* | placeBlockInRegion | Place block in theme region |

## Pattern

Grant permissions to role:

```yaml
config:
  actions:
    user.role.authenticated:
      grantPermission: 'access content'
    user.role.editor:
      grantPermissions:
        - 'access content'
        - 'access toolbar'
```

Grant permissions for each node type:

```yaml
config:
  actions:
    user.role.content_editor:
      grantPermissionsForEachNodeType:
        - 'create %bundle content'
        - 'edit own %bundle content'
```

Configure text format:

```yaml
config:
  actions:
    filter.format.basic_html:
      setFilterFormat:
        id: filter_html
        configuration:
          allowed_html: '<p> <a href>'
        weight: -10
```

Configure field display:

```yaml
config:
  actions:
    core.entity_form_display.node.article.default:
      setComponents:
        - name: body
          options:
            type: text_textarea_with_summary
            weight: 2
            region: content
        - name: field_image
          options:
            type: image_image
            weight: 1
```

Add to editorial workflow:

```yaml
config:
  actions:
    workflows.workflow.editorial:
      addNodeTypes:
        - article
        - page
      addTaxonomyVocabularies:
        - tags
```

## Common Mistakes

- **Wrong**: Using grantPermissions with single permission → **Right**: Works but use grantPermission for clarity
- **Wrong**: Forgetting %bundle placeholder in grantPermissionsForEachNodeType → **Right**: Literal `%bundle` string won't match real permissions
- **Wrong**: Setting display components before field exists → **Right**: Create field storage/config first, then display
- **Wrong**: Not understanding setComponents vs removeComponent → **Right**: setComponents adds/updates, removeComponent hides
- **Wrong**: Hardcoding theme-specific actions → **Right**: Use inputs or variables for theme names to make recipes portable

## See Also

- [Config Actions - Universal](config-actions-universal.md)
- [Config Actions - Advanced Patterns](config-actions-advanced.md)
- Reference: `core/modules/user/src/Entity/Role.php` (ActionMethod attributes)
- Reference: https://project.pages.drupalcode.org/distributions_recipes/config_action_list.html
