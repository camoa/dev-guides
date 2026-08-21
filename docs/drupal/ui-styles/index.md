---
description: UI Styles module — curated CSS class options for site builders in Drupal's block, Layout Builder, Views, CKEditor, and page/region UIs.
tracks:
  - project: ui_styles
    channel: stable
    declared: "8.x-1.21"
    verified: 2026-08-20
guide-meta:
  concepts:
    - UI Styles
    - ui_styles
    - ui_styles.yml
    - curated CSS classes
    - style plugins
    - source plugins
    - Checkbox widget
    - Toolbar widget
    - Select widget
    - stylesheet generation
    - ui_styles_block
    - ui_styles_layout_builder
    - ui_styles_ckeditor5
    - ui_styles_views
    - ui_styles_page
    - ui_styles_ui_patterns
    - hook_ui_styles_styles_alter
    - StylesheetGenerator
  not:
    - UI Skins (CSS variable theming — separate module)
    - Layout Builder Styles (legacy lb_styles module)
    - UI Patterns component structure (see drupal/ui-patterns)
    - freeform extra CSS classes
  requires:
    - drupal/layout-builder
  complements:
    - drupal/ui-patterns
    - drupal/sdc
    - drupal/layout-builder
    - drupal/views
  specializes: ""
  category: drupal
---

# UI Styles

**Philosophy**: Centralize curated CSS class options in YAML so site builders can apply design-system utilities through Drupal's UI without typing class names. Definitions live alongside themes/modules; UI Styles handles discovery, form rendering, and class injection at render time.

## I Need To...

| I need to... | Guide | Summary |
|-------------|-------|---------|
| Understand what UI Styles does and when to use it vs alternatives | [Overview](overview.md) | Use UI Styles when site builders need curated, named CSS class options in block/LB/Views UIs without freeform input. It injects classes at render time from YAML-defined plugins; it is not a CSS generator and does not replace UI Skins or UI Patterns. |
| Install UI Styles and enable the right submodules | [Installation](installation.md) | Require drupal/ui_styles via Composer, then enable only the integration submodules you need (block, layout_builder, ckeditor5, views, page, ui_patterns). The base module is the engine — enabling it alone adds no editor UI. |
| Declare a style in YAML with options, icons, and categories | [Style Definition Format](definition-format.md) | Place {name}.ui_styles.yml at the theme/module root; prefix plugin IDs with the theme/module name to avoid collisions. Each style declares options as class => label (short) or class => {label, icon, description} (long). Use category to group related styles. |
| Choose or control the form widget (checkbox / toolbar / select) | [Source Plugins](source-plugins.md) | UI Styles picks the widget automatically — 1 option becomes a Checkbox, all options with icons become a Toolbar, everything else falls back to a Select dropdown. To force Toolbar, every option must have an icon field; to force Checkbox, declare exactly one option. |
| Apply styles to blocks in Block layout | [Block Layout Integration](block-layout.md) | Enable ui_styles_block; each block's configuration form gains a UI Styles fieldset. Selections persist in block config entity third-party settings under ui_styles_block.selected and are injected into #attributes['class'] at render time. |
| Apply styles to blocks and sections in Layout Builder | [Layout Builder Integration](layout-builder.md) | Enable ui_styles_layout_builder; block placement forms and section configuration forms both gain UI Styles fieldsets. Apply background/rhythm/width classes at the section level, component-specific classes at the block level. |
| Add inline text styles via CKEditor 5 | [CKEditor 5 Integration](ckeditor5.md) | Enable ui_styles_ckeditor5 and add its toolbar items to a text format's CKEditor 5 toolbar. CKEditor-targeted styles must also be whitelisted in the text format's allowed HTML — otherwise Drupal's filter strips the injected class on render. |
| Style Views displays, pagers, and exposed filters | [Views Integration](views.md) | Enable ui_styles_views; each Views display configuration gains UI Styles fieldsets for the display wrapper, pager, and exposed form. Display-level styles target the outer View wrapper — per-row styling still requires template overrides or field formatters. |
| Apply styles to regions and pages | [Pages & Regions Integration](page-region.md) | Enable ui_styles_page; the theme settings page gains a section to apply styles to the page wrapper and each region. Selections store in theme settings YAML and apply via hook_preprocess_region/page. These are theme-level (all pages) — don't duplicate with LB section styles. |
| Style UI Patterns / SDC components | [UI Patterns & SDC Integration](ui-patterns-sdc.md) | Enable ui_styles_ui_patterns; pattern instances in Layout Builder gain UI Styles form fieldsets per exposed prop slot. Styles merge into the rendered Twig template's attributes. Component-internal markup not exposed as a slot cannot be targeted — modify the Twig template instead. |
| Ship a theme with its own UI Styles definitions | [Theme Authoring](theme-authoring.md) | Place {theme}.ui_styles.yml at the theme root (not a subdirectory); clear cache after creation. Prefix plugin IDs with the theme name. Subthemes inherit parent UI Styles and add to them; suppress parent styles with enabled: false on the same plugin ID. |
| Understand the optimized stylesheet generation | [Stylesheet Generation](stylesheet-generation.md) | The ui_styles.stylesheet_generator service parses all theme/module CSS, filters it to only rules matching declared style option classes, and serves the result as ui_styles/generated_styles on every page. Output is cached; clear cache after editing CSS or style definitions. |
| Override or disable an existing style | [Overriding & Disabling](overriding.md) | Disable an upstream style by re-declaring its plugin ID with enabled: false in your theme's YAML. Add options by re-declaring with only the new options (arrays merge). For conditional/runtime overrides, implement hook_ui_styles_styles_alter(). Never edit upstream YAML directly. |
| Hook into the render pipeline programmatically | [Programmatic Use](programmatic.md) | Use plugin.manager.ui_styles to read definitions, the ui_styles_styles form element type in custom forms, and Drupal\ui_styles\Render\Element::addClasses() to inject classes into render arrays. Store both the selected array and extra string — not just the class string. |
| Avoid common mistakes | [Anti-Patterns](anti-patterns.md) | The most common mistakes are relying on the extra freeform field instead of curated options, using generic plugin IDs that collide, defining mega-styles with too many options, and deleting style definitions without auditing existing config references. |
| Find key classes and services | [Code Reference](code-reference.md) | Core services are plugin.manager.ui_styles (style definitions) and ui_styles.stylesheet_generator (optimized CSS). The ui_styles_styles form element type accepts selected+extra default_value. Use hook_ui_styles_styles_alter() to modify definitions programmatically. |
