---
description: "Performance and security best practices for Custom Field -- single-table advantage, entity load patterns, XSS prevention, and access checks."
tldr: "Custom Field's single-table storage avoids Paragraphs' N+1 query problem; always check entity access before rendering references, sanitize formatter output with render arrays instead of raw concatenation, and use private:// for sensitive files."
drupal_version: "11.x"
---

# Best Practices: Performance & Security

## When to Use

You want to optimize custom field performance and ensure secure data handling.

## Performance

**Single-table advantage**:

- Custom Field stores all sub-fields in one table row -- single query to load all data
- Paragraphs creates N entities -- N+1 query problem (1 parent + N children)
- For 10 sub-fields: Custom Field = 1 JOIN, Paragraphs = 10+ JOINs

**Optimization patterns**:

```php
// GOOD: Load entity once, access multiple sub-fields
$node = \Drupal::entityTypeManager()->getStorage('node')->load($nid);
$street = $node->field_address->street;
$city = $node->field_address->city;
$state = $node->field_address->state;

// BAD: Loading entity repeatedly
$street = Node::load($nid)->field_address->street;
$city = Node::load($nid)->field_address->city; // Redundant load
```

**Views performance**:

- All columns in same table -- no relationship needed
- Filter/sort on custom field columns = single table query
- vs Paragraphs: require relationships, multiple JOIN tables

**Field count limits**:

- MySQL row size limit: ~8KB per row
- Practical limit: ~50-100 sub-fields depending on types
- For 100+ fields: consider custom field type plugin instead

**Caching**:

- Field values cached with entity
- No special caching needed
- Clear entity cache when updating programmatically

## Security

**Input validation**:

- Widget validation runs automatically
- For custom widgets, implement validation in widget plugin
- Don't trust programmatic imports -- validate types

**XSS prevention**:

```php
// GOOD: Use render arrays with automatic escaping
return [
  '#markup' => $this->t('Value: @value', ['@value' => $value]),
];

// BAD: Raw concatenation
return '<div>' . $value . '</div>'; // XSS vulnerability
```

**Entity reference access checks**:

```php
// GOOD: Check access before rendering
$entity = $storage->load($entity_id);
if ($entity && $entity->access('view')) {
  return $entity->toLink()->toRenderable();
}

// BAD: Assume access
return $storage->load($entity_id)->toLink(); // May expose restricted content
```

**File upload security**:

- Always validate file extensions in widget settings
- Use private:// scheme for sensitive files
- Configure upload_location to segregate files
- Set max_filesize to prevent DoS

**Link security**:

- Use noopener noreferrer for target="_blank"
- Validate external URLs with allowed protocols
- Built-in constraints: LinkExternalProtocolsConstraint, LinkAccessConstraint

**SQL injection prevention**:

- Custom Field uses Entity API -- parameterized queries automatic
- For custom queries, use query builders with placeholders
- Never concatenate user input into SQL

## Common Mistakes

- **Loading entities in loops** -- Load once, access multiple times; or use loadMultiple()
- **Not sanitizing output in custom formatters** -- Use render arrays with #markup and placeholders, not raw concatenation
- **Exposing entity references without access checks** -- Always check $entity->access('view')
- **Public files for private data** -- Use private:// scheme and configure file access controls
- **Complex joins in Views** -- Custom Field columns in same table; avoid relationship if possible

## See Also

- OWASP: https://owasp.org/www-project-top-ten/
- Drupal security: https://www.drupal.org/security/secure-coding-practices
- [Development Standards](development-standards.md)
