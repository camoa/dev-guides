---
description: "Text column types in Custom Field 5.0.2 -- string, string_long, email, telephone, uri, color -- with schema, length limits, and gotchas."
tldr: "Six text column types (string, string_long, email, telephone, uri, color) cover short strings through long text; use string_long past 255 characters and the link type instead of uri when a title or attributes are needed."
drupal_version: "11.x"
---

# Column Types: Text Fields

## When to Use

Storing text data in custom field columns -- names, labels, descriptions, emails, phone numbers, URLs, colors.

## string

Short text up to 255 characters (VARCHAR column).

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| length | integer | 255 | Max 255; locked after data exists |

**Schema:** `VARCHAR(length) NOT NULL DEFAULT ''`

```yaml
columns:
  first_name:
    name: first_name
    type: string
    length: 50
  last_name:
    name: last_name
    type: string
    length: 50
```

**Gotchas:** Length cannot exceed 255. For longer text, use string_long. Default value is empty string, not NULL.

## string_long

Long text (TEXT column) for descriptions, notes, multi-line content.

**Schema:** `TEXT NOT NULL`

```yaml
columns:
  description:
    name: description
    type: string_long
```

**Gotchas:** Cannot be used in database indexes. Not suitable for sorting/filtering in Views without performance impact.

## email

Email address with validation (VARCHAR 254).

**Schema:** `VARCHAR(254) NOT NULL DEFAULT ''`

```yaml
columns:
  contact_email:
    name: contact_email
    type: email
```

**Gotchas:** Max length 254 per RFC 5321. Validation on input, not storage -- invalid data can be imported programmatically.

## telephone

Phone number (VARCHAR, configurable length).

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| length | integer | 256 | Max 256 |

**Schema:** `VARCHAR(length) NOT NULL DEFAULT ''`

```yaml
columns:
  phone:
    name: phone
    type: telephone
    length: 20
```

**Gotchas:** No built-in format validation -- stores as-is. Use widget validation for formatting.

## uri

URI/URL field (VARCHAR 2048).

**Schema:** `VARCHAR(2048) NOT NULL DEFAULT ''`

```yaml
columns:
  website:
    name: website
    type: uri
```

**Gotchas:** Stores URI only. Use LinkWidget for full link functionality with title and attributes.

## color

Hex color value (VARCHAR 7) -- stores `#RRGGBB` format.

**Schema:** `VARCHAR(7) NOT NULL DEFAULT ''`

```yaml
columns:
  brand_color:
    name: brand_color
    type: color
```

**Gotchas:** Automatically converts to uppercase hex with # prefix. Input without # gets # prepended. Invalid colors stored as NULL.

## Common Mistakes

- **Using string for long text** -- Use string_long for content exceeding 255 characters
- **Setting telephone length too short** -- International phone numbers with extensions can exceed 20 characters
- **Using uri instead of link** -- uri stores URL only; link type includes title and options for attributes
- **Not validating email/phone format** -- Storage types don't enforce format; validation happens at widget level

## See Also

- [Column Types: Numeric Fields](column-types-numeric.md)
- Reference: `/modules/contrib/custom_field/src/Plugin/CustomField/FieldType/`
