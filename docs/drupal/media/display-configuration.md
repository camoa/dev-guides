---
description: Configuring custom formatters and widgets for media source fields
drupal_version: "11.x"
---

# Display Configuration

## When to Use

> Use display configuration when customizing how media source fields are displayed in views and edited in forms when media type is created.

## Decision

| Customization | Method | Use Case |
|---------------|--------|----------|
| Custom formatter for source field | Override `prepareViewDisplay()` | Instagram embed, YouTube player |
| Custom widget for source field | Override `prepareFormDisplay()` | URL input with preview, autocomplete |
| Hide source field in display | Set component to hidden in prepareViewDisplay() | Source field not user-facing |
| Add help text to widget | Configure widget description | Guide editors on URL format |

## Pattern

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

## Common Mistakes

- **Wrong**: Hardcoding field name → **Right**: Use `getSourceFieldDefinition()->getName()`
- **Wrong**: Not calling `getSourceFieldDefinition()` → **Right**: Get field name dynamically
- **Wrong**: Forgetting to set weight → **Right**: Set weight for predictable ordering
- **Wrong**: Using non-existent formatter → **Right**: Verify formatter plugin exists
- **Wrong**: Not considering Media Library → **Right**: Test widgets in inline entity forms

## See Also

- Previous: [Validation Constraints](validation-constraints.md)
- Next: [Security Best Practices](security-best-practices.md)
- Reference: core/modules/media/src/MediaSourceInterface.php (line 146-179)
