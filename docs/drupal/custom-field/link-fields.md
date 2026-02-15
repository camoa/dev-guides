---
description: Link sub-fields with URL, title, attributes, Linkit integration, and security considerations for target_blank links.
---

# Link Sub-Fields

## When to Use

You need full link functionality (URL + title + attributes) within a custom field column.

## Pattern

**Link column configuration**:

```yaml
columns:
  external_link:
    name: external_link
    type: link
```

**Widget configuration**:

```php
$settings['field_settings']['external_link'] = [
  'widget' => 'link',
  'widget_settings' => [
    'placeholder_url' => 'https://example.com',
    'placeholder_title' => 'Link title',
  ],
  // Link field settings
  'link_type' => LinkItemInterface::LINK_GENERIC, // or LINK_INTERNAL, LINK_EXTERNAL
  'title' => DRUPAL_OPTIONAL, // or DRUPAL_REQUIRED, DRUPAL_DISABLED
];
```

**Accessing in code**:

```php
$uri = $node->field_custom->external_link; // URI string
$title = $node->field_custom->{'external_link__title'};
$options = $node->field_custom->{'external_link__options'}; // Serialized array

// Render as link
$url = Url::fromUri($uri, $options);
$link = Link::fromTextAndUrl($title ?: $uri, $url)->toRenderable();
```

**Link options array**:

```php
[
  'attributes' => [
    'target' => '_blank',
    'rel' => 'noopener noreferrer',
    'class' => ['external-link'],
  ],
]
```

## Decision

| If you need... | Use... | Why |
|---|---|---|
| Internal and external links with attributes | link type + LinkWidget | Full link functionality, attribute support |
| External URLs only (no title/attributes) | uri type + UrlWidget | Simpler, just URL validation |
| URLs with Linkit entity browser | link type + custom_field_linkit sub-module | Linkit autocomplete for internal links |

## Common Mistakes

- **Not validating link types** -- Configure link_type to restrict internal/external; validation enforces
- **Forgetting to sanitize title** -- Link title is user input; sanitize before rendering
- **Not setting rel=noopener for target=_blank** -- Security vulnerability; always set noopener noreferrer for external links
- **Using uri type when attributes needed** -- uri stores URL only; link type required for target, class, rel

## See Also

- Reference: `/modules/contrib/custom_field/src/Plugin/CustomField/FieldWidget/LinkWidget.php`
- Sub-module: custom_field_linkit
