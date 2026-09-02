---
description: Config actions for specific entity types derived from ActionMethod attributes on entity methods
tldr: "Use entity-specific config actions when you need to configure roles, text formats, displays, workflows, or other specialized entity types."
drupal_version: "11.x"
---

# Config Actions - Entity-Specific

## When to Use

> Use entity-specific config actions when you need to configure roles, text formats, displays, workflows, or other specialized entity types.

Config actions for specific entity types. These actions are derived from ActionMethod attributes on entity methods.

## Items: Entity-Specific Config Actions

### grantPermission / grantPermissions (user.role.*)

**Description:** Grant permission(s) to a role
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| grantPermission | string | Single permission machine name |
| grantPermissions | array | Multiple permission machine names |

**Usage Example:**
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
**Gotchas:** Permissions must exist (provided by installed modules); no validation until runtime

### grantPermissionsForEachNodeType (user.role.*)

**Description:** Grant permissions with bundle placeholder for each node type
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| value | array | Permission templates with `%bundle` placeholder |

**Usage Example:**
```yaml
config:
  actions:
    user.role.content_editor:
      grantPermissionsForEachNodeType:
        - 'create %bundle content'
        - 'edit own %bundle content'
```
**Gotchas:** Only works for node bundles; `%bundle` replaced with node type machine name

### revokePermission / revokePermissions (user.role.*)

**Description:** Revoke permission(s) from a role
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| revokePermission | string | Single permission |
| revokePermissions | array | Multiple permissions |

**Usage Example:**
```yaml
config:
  actions:
    user.role.anonymous:
      revokePermission: 'post comments'
```
**Gotchas:** Safe to revoke non-existent permissions (no-op)

### setFilterFormat (filter.format.*)

**Description:** Configure text format filter plugins
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| id | string | Filter plugin ID |
| configuration | array | Filter plugin config |
| weight | int | Filter order |

**Usage Example:**
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
**Gotchas:** Filter plugins must be provided by installed modules

### setEditorImageUpload (editor.editor.*)

**Description:** Configure image upload settings for WYSIWYG
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| status | bool | Enable/disable uploads |
| scheme | string | public or private |
| directory | string | Upload directory |
| max_size | string | File size limit |

**Usage Example:**
```yaml
config:
  actions:
    editor.editor.basic_html:
      setEditorImageUpload:
        status: true
        scheme: public
        directory: 'inline-images'
```
**Gotchas:** Requires editor module; only works with compatible editors (CKEditor 5)

### setComponent / setComponents (core.entity_form_display.*, core.entity_view_display.*)

**Description:** Configure field widget/formatter display
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| name | string | Field machine name |
| options | array | Widget/formatter settings |

**Usage Example:**
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
**Gotchas:** Field must exist; display creates if missing via createIfNotExists first

### removeComponent (core.entity_form_display.*, core.entity_view_display.*)

**Description:** Hide field from display
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| value | string or array | Field name(s) to remove |

**Usage Example:**
```yaml
config:
  actions:
    core.entity_view_display.node.article.default:
      removeComponent: 'field_internal_notes'
```
**Gotchas:** Removes from `content` section; field remains on entity

### addItemToToolbar (editor.editor.*)

**Description:** Add button to CKEditor 5 toolbar
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| item_name | string | Toolbar item machine name |
| position | int (optional) | Position in toolbar |

**Usage Example:**
```yaml
config:
  actions:
    editor.editor.full_html:
      addItemToToolbar: drupalMedia
```
**Gotchas:** Item must be provided by an installed CKEditor 5 plugin; only works with CKEditor 5 editors

### addToAllBundles (field.field.*)

**Description:** Add field to all bundles of an entity type (pairs with setComponent)
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| field_name | string | Field machine name |

**Usage Example:**
```yaml
config:
  actions:
    field.storage.node.field_tags:
      addToAllBundles: {}
```
**Gotchas:** Field storage must exist; creates field.field.* config for each bundle; pair with setComponent for display

### addNodeTypes / addTaxonomyVocabularies (workflows.workflow.*)

**Description:** Add content types or vocabularies to an editorial workflow
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| value | array | List of bundle machine names |

**Usage Example:**
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
**Gotchas:** Workflow must exist; bundles must exist; requires content_moderation module

### placeBlockInRegion (block.block.*)

**Description:** Place block in theme region
**Parameters:**
| Param | Type | Notes |
|-------|------|-------|
| region | string | Theme region machine name |
| theme | string | Theme machine name |

**Usage Example:**
```yaml
config:
  actions:
    block.block.olivero_search:
      placeBlockInRegion:
        region: header
        theme: olivero
```
**Gotchas:** Region must exist in theme; theme must be installed

## Common Mistakes

- Using grantPermissions with single permission → Works but use grantPermission for clarity
- Forgetting %bundle placeholder in grantPermissionsForEachNodeType → Literal `%bundle` string won't match real permissions
- Setting display components before field exists → Create field storage/config first, then display
- Not understanding setComponents vs removeComponent → setComponents adds/updates, removeComponent hides
- Hardcoding theme-specific actions → Use inputs or variables for theme names to make recipes portable

## See Also

- Previous: ← [Config Actions - Universal](config-actions-universal.md)
- Next: [Config Actions - Advanced Patterns](config-actions-advanced.md) →
- Reference: `core/modules/user/src/Entity/Role.php` (ActionMethod attributes)
- Reference: https://project.pages.drupalcode.org/distributions_recipes/config_action_list.html
