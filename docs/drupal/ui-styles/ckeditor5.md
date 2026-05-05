---
description: Apply curated inline text styles via CKEditor 5 using UI Styles without exposing freeform class input.
tldr: Enable ui_styles_ckeditor5 and add its toolbar items to a text format's CKEditor 5 toolbar. CKEditor-targeted styles must also be whitelisted in the text format's allowed HTML — otherwise Drupal's filter strips the injected class on render.
drupal_version: "11.x"
---

# Integration: CKEditor 5

## When to Use

> Use this guide when letting authors apply curated text styles inline (highlight, lead paragraph, drop cap) inside CKEditor 5 without exposing the Source button or freeform class input.

## Pattern

Enable `ui_styles_ckeditor5`. In the CKEditor 5 toolbar configuration of a text format (Configuration → Text formats and editors), add the **UI Styles** plugin's toolbar items.

Style definitions used by CKEditor 5 must declare the HTML element they apply to — the CKEditor plugin maps `tag` + class to an inline button. See the module's docs for the CKEditor-specific declaration schema additions.

**Storage**: Applied as an HTML class on the wrapping element directly in the rendered field HTML — no separate config storage.

## Common Mistakes

- **Allowing styles whose CSS classes aren't whitelisted in the text format's allowed HTML** → Drupal's filter strips the class on render. Update the format's allowed HTML to permit the relevant `<tag class="...">` pattern
- **Reusing the same style ID across CKEditor and block-level use** → Works, but the editor UX may surface inappropriate options. Scope CKEditor styles into a separate category

## See Also

- [Style Definition Format](definition-format.md)
- [Integration: Block Layout](block-layout.md)
- Reference: `modules/ui_styles_ckeditor5/` in the UI Styles module
