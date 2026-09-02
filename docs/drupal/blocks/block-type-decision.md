---
description: Decide between block plugin, content block, or inline block for your use case
tldr: "Use block plugins when you need logic, DI, or dynamic content. Use content blocks when editors need to manage content without code changes."
drupal_version: "11.x"
---

# Block Type Decision Matrix

## When to Use

> Before creating any block, decide which approach fits your use case.

## Decision

| If you need... | Use... | Why |
|----------------|--------|-----|
| Business logic, dynamic content, external data | Block Plugin | Programmatic control, dependency injection, no UI overhead |
| Editor-managed content with fields | Content Block | Fieldable entities, revisions, translations, no code changes |
| One-off content specific to a single page/layout | Inline Block (Layout Builder) | No reusability overhead, lives with the layout |
| Entity field displayed as a block | Field Block (Layout Builder) | Native entity display, no duplication |
| Integration with services/APIs | Block Plugin with DI | Full access to Symfony DI container |
| Content that appears on multiple pages | Reusable Content Block | Single source of truth, update once |
| Contextual content that changes per page | Block Plugin with cache contexts | Proper caching variation |
| Form-based interaction | Block Plugin returning form | `formBuilder->getForm()` in `build()` |

**The fundamental question:** Is this **logic** or **content**?
- Logic = Block Plugin (code-driven)
- Content = Content Block (editor-driven)
- One-off content in layout = Inline Block
- Need both = Content Block Type + fields

## Pattern

**Block Plugin example** (logic-driven):
```php
#[Block(id: "current_time", admin_label: new TranslatableMarkup("Current Time"))]
class CurrentTimeBlock extends BlockBase {
  public function build() {
    return [
      '#markup' => date('Y-m-d H:i:s'),
      '#cache' => ['max-age' => 0],
    ];
  }
}
```

**Content Block** (editor-driven): Create via UI at `/admin/structure/block-content/types`, add fields, create instances at `/block/add/{type}`.

**Reference:** `core/modules/system/src/Plugin/Block/SystemBrandingBlock.php` (block plugin), `core/modules/block_content/` (content blocks)

## Common Mistakes

- Using block plugins for static content → Use content blocks; site builders can manage without code changes
- Using content blocks for dynamic logic → Use block plugins; entities add overhead and can't easily inject services
- Creating reusable content blocks when content only appears once → Use inline blocks in Layout Builder
- Hardcoding placement in code → Use config entities for placement flexibility

## See Also

- [Creating Block Plugins](creating-block-plugins.md) (for logic)
- [Custom Block Types](custom-block-types.md) (for content)
- [Layout Builder Integration](layout-builder-blocks.md) (for inline/field blocks)
