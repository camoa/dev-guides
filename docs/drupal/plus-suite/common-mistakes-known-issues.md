---
description: Plus Suite common mistakes, known issues, debugging tips, and performance considerations as of April 2026
tldr: "Read this before starting any Plus Suite implementation and when troubleshooting problems."
drupal_version: "11.x"
---

# Common Mistakes & Known Issues

## When to Use

> When troubleshooting Plus Suite problems or before starting implementation.

## Known Issues (as of April 2026)

**Recipe on Existing Sites (Critical)**

- Issue: [#3517909](https://www.drupal.org/project/plus_suite/issues/3517909)
- Problem: Recipe fails when `field.storage.node.layout_builder__layout` already exists.
- Status: Needs work. Works on fresh installs and Drupal CMS, but existing sites with Layout Builder will fail.
- Workaround: Install modules manually, create config by hand.

**DropzoneJS Repository**

- Issue: [#3535241](https://www.drupal.org/project/plus_suite/issues/3535241)
- Problem: DropzoneJS JS library must be added as a composer repository manually.
- Workaround: Add the repository to composer.json before requiring plus_suite.

**Navigation+ on Existing Sites**

- Issue: [#3518649](https://www.drupal.org/project/plus_suite/issues/3518649)
- Problem: Navigation+ may have incompatibilities on existing sites.

## Common Mistakes: Quick Reference

| Mistake | Consequence | Fix |
|---|---|---|
| Not enabling Navigation module | Edit Mode button doesn't appear | Enable core `navigation` module |
| Skipping Edit Mode config per bundle | Content type can't enter Edit Mode | Structure → Content Types → Edit → Navigation+ |
| No promoted blocks configured | Empty "Promoted" tab in PlaceBlock | Configure promoted blocks on Manage Display |
| Missing field sample value config | Empty blocks on placement | Configure generators per field |
| Wrong Edit+ handle type | Inline editing targets wrong element | Set handle to `wrapper` for multi-value fields |
| Nesting too deep | Performance issues, confusing UX | Limit to 2-3 levels |
| Not clearing cache after config changes | Stale tool/mode behavior | `drush cr` after config changes |
| Forgetting `access inline editing` permission | Users can enter Edit Mode but can't change content | Grant permission to editor role |
| No default layout on Layout Block type | "Undefined array key 'layout_plugin'" error | Configure a default One Column layout on the block type's Manage Display |
| Field templates missing wrapper attributes | Edit+ inline editing silently fails | Field templates MUST include `<div{{ attributes }}>` and `<div{{ item.attributes }}>` wrappers |
| Missing `data-drupal-messages-fallback` div | Edit+ AJAX messages don't display | Page template must contain `<div data-drupal-messages-fallback></div>` |
| Not enabling "Allow each content item..." | Only default layout available, no per-node customization | Check BOTH "Use Layout builder" AND "Allow each content item to have its layout customized" |
| Layout Block type still has body field | Body field takes up space inside nested layout | Remove the body field from the Layout Block block type |
| Z-index conflicts with Edit+ sidebar | Sidebar appears behind other page elements | Override sidebar z-index using CSS custom properties |
| CKEditor floating panel misaligned | Editor toolbar overlaps fixed header | Use `hook_page_attachments()` to set CKEditor viewport offset for fixed headers |

## Edit+ Field Template Requirement

**Critical**: For Edit+ inline editing to work, field templates MUST include wrapper and item attributes. Direct field output in custom templates (like `{{ content.field_name }}` rendered without attributes) will break inline editing:

```twig
{# Correct — attributes are passed through #}
<div{{ attributes }}>
  {% for item in items %}
    <div{{ item.attributes }}>{{ item.content }}</div>
  {% endfor %}
</div>

{# Wrong — no attributes, Edit+ cannot correlate form items #}
<div class="my-wrapper">
  {{ items[0].content }}
</div>
```

## Performance Considerations

| Concern | Mitigation |
|---|---|
| TwigRenderTemplateEvent on every render | Only active in Edit Mode |
| TreeIndex for nested layouts | O(1) lookups, built once per request |
| Multiple AJAX calls during editing | Each tool has optimized JS libraries |
| Tempstore reads on page load | Param converter only checks when edit mode active |

## Upgrade Considerations

- Plus Suite is in active development with frequent releases (14 in ~13 months)
- Pin to specific versions in composer.json rather than using dev branches in production
- Test upgrades in staging before applying to production
- The recipe is version-locked to compatible module versions

## Debugging Tips

| Issue | Debug Approach |
|---|---|
| Edit Mode not activating | Check `navigationMode` cookie value in browser dev tools |
| Tool not appearing | Check `applies()` method, verify Layout Builder enabled |
| Inline editing not working | Verify `access inline editing` permission, check field third-party settings |
| Blocks not getting sample content | Check field_sample_value config on each field |
| Nested layout changes not saving | Ensure `bubbleChangesToRoot()` is called |
| AJAX errors | Check browser console for JS errors, verify routes exist |

## Common Mistakes

- **Do not use Plus Suite on Drupal < 11.3** — it requires the Navigation module which is only in 11.3+.
- **Do not apply the recipe without reading the issue queue first** — the recipe status changes frequently.
- **Do not skip the install.sh script for evaluation** — it handles all the complex setup automatically.

## See Also

- [Installation & Setup](installation-setup.md)
- [Recipe Structure](recipe-structure.md)
- [Permissions & Access](permissions-access.md)
- Reference: [Plus Suite issue queue](https://www.drupal.org/project/issues/plus_suite)
