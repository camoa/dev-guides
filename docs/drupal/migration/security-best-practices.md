---
description: Security controls for SQL injection, XSS, and access bypass in migrations
drupal_version: "11.x"
---

# Security Best Practices

## When to Use

Migration introduces security risks: SQL injection in custom sources, XSS in migrated content, access bypass during imports. Apply security controls at source, process, and destination layers.

## Decision

| Security concern | Mitigation | Implementation |
|---|---|---|
| SQL injection in custom sources | Prepared statements, never string concat | Use database API properly |
| XSS in migrated HTML | Sanitize during process | Use filter_default_format, validate HTML |
| Access bypass during migration | Check permissions | Validate user can create content |
| Credential exposure | Environment variables | Never hardcode DB passwords |
| Insecure file uploads | Validate file types, limit extensions | Configure file field validators |

## Pattern

**Secure custom source plugin:**

```php
// WRONG - SQL injection vulnerability
$query = "SELECT * FROM {node} WHERE title = '" . $user_input . "'";

// CORRECT - Prepared statement
$query = $this->select('node', 'n')
  ->fields('n')
  ->condition('title', $user_input, '=');
```

**Sanitize HTML content:**

```yaml
process:
  body/value:
    -
      plugin: callback
      callable: strip_tags
      source: body
    -
      plugin: callback
      callable: trim
  body/format:
    plugin: default_value
    default_value: basic_html  # Use restrictive format
```

**Secure file migration:**

```yaml
process:
  field_document:
    -
      plugin: migration_lookup
      migration: d7_file
      source: field_document
    -
      plugin: file_validate_extensions
      extensions: 'pdf doc docx'  # Whitelist only
```

**Reference**: `/core/lib/Drupal/Core/Database/Connection.php` for secure database queries

## Common Mistakes

- **Wrong**: Migrating D7 PHP filter content → **Right**: Huge security risk, rewrite as plugins/templates
- **Wrong**: Not validating file extensions → **Right**: Executable uploads possible
- **Wrong**: Using Full HTML format for migrated content → **Right**: XSS risk, use filtered formats
- **Wrong**: Storing database credentials in migration YAML → **Right**: Use settings.php, environment variables
- **Wrong**: Not escaping user-generated content → **Right**: Always assume D7 content may be malicious

## See Also

- Reference: [Drupal security best practices 2025](https://wishdesk.com/blog/drupal-security-best-practices-in-2025)
- Reference: [OWASP Top 10](https://owasp.org/www-project-top-ten/)
