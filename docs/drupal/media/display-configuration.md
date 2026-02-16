---
description: Customizing how media source fields are displayed in views and edited in forms when media type is created.
---

# Display Configuration

### When to Use

Customizing how media source fields are displayed in views and edited in forms when media type is created.

### Decision

| Customization | Method | Use Case |
|---------------|--------|----------|
| Custom formatter for source field | Override `prepareViewDisplay()` | Instagram embed, YouTube player |
| Custom widget for source field | Override `prepareFormDisplay()` | URL input with preview, autocomplete |
| Hide source field in display | Set component to hidden in prepareViewDisplay() | Source field not user-facing |
| Add help text to widget | Configure widget description | Guide editors on URL format |

### Pattern

Configuring custom formatter and widget (10 lines):
```php
public function prepareViewDisplay(MediaTypeInterface $type, EntityViewDisplayInterface $display): void {
  $display->setComponent($this->getSourceFieldDefinition($type)->getName(), [
    'type' => 'custom_media_formatter',
    'label' => 'visually_hidden',
    'settings' => ['width' => 640, 'height' => 480],
    'weight' => 1,
  ]);
}

public function prepareFormDisplay(MediaTypeInterface $type, EntityFormDisplayInterface $display): void {
  $source_field = $this->getSourceFieldDefinition($type)->getName();
  $display->setComponent($source_field, [
    'type' => 'string_textfield',
    'weight' => $display->getHighestWeight() + 1,
    'settings' => ['placeholder' => 'https://example.com/item/123'],
  ]);
}
```

### Common Mistakes

- Hardcoding field name → Breaks when source field name changes
- Not calling `getSourceFieldDefinition()` → Wrong field configured
- Forgetting to set weight → Display order unpredictable
- Using non-existent formatter → White screen, plugin not found error
- Not considering Media Library → Custom widgets may break inline entity forms

**WHY:**
- **Field name flexibility**: Source field name is configurable; hardcoding assumes default name, breaks custom configurations
- **Weight matters**: Display components stack by weight; missing weight causes fields to appear in wrong order
- **Plugin existence**: Referenced formatters/widgets must exist; non-existent plugins cause fatal errors
- **Media Library compatibility**: Media Library uses inline entity forms with specific requirements; custom widgets may break selection UI

### See Also

- Previous: [Validation Constraints](index.md)
- Next: [Security Best Practices](index.md)
- Reference: core/modules/media/src/MediaSourceInterface.php (line 146-179)