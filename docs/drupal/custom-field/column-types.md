---
description: All 27 custom field column types organized by category -- text, numeric, date/time, reference, file, and data fields with schema details and gotchas.
---

# Column Types

## Text Fields

### string

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
```

**Gotchas:** Length cannot exceed 255. For longer text, use string_long. Default value is empty string, not NULL.

### string_long

Long text (TEXT column) for descriptions, notes, multi-line content.

**Schema:** `TEXT NOT NULL`

```yaml
columns:
  description:
    name: description
    type: string_long
```

**Gotchas:** Cannot be used in database indexes. Not suitable for sorting/filtering in Views without performance impact.

### email

Email address with validation (VARCHAR 254).

**Schema:** `VARCHAR(254) NOT NULL DEFAULT ''`

**Gotchas:** Max length 254 per RFC 5321. Validation on input, not storage -- invalid data can be imported programmatically.

### telephone

Phone number (VARCHAR, configurable length).

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| length | integer | 256 | Max 256 |

**Schema:** `VARCHAR(length) NOT NULL DEFAULT ''`

**Gotchas:** No built-in format validation -- stores as-is. Use widget validation for formatting.

### uri

URI/URL field (VARCHAR 2048).

**Schema:** `VARCHAR(2048) NOT NULL DEFAULT ''`

**Gotchas:** Stores URI only. Use LinkWidget for full link functionality with title and attributes.

### color

Hex color value (VARCHAR 7) -- stores `#RRGGBB` format.

**Schema:** `VARCHAR(7) NOT NULL DEFAULT ''`

**Gotchas:** Automatically converts to uppercase hex with # prefix. Input without # gets # prepended. Invalid colors stored as NULL.

### Text field mistakes

- **Using string for long text** -- Use string_long for content exceeding 255 characters
- **Setting telephone length too short** -- International phone numbers with extensions can exceed 20 characters
- **Using uri instead of link** -- uri stores URL only; link type includes title and options for attributes
- **Not validating email/phone format** -- Storage types don't enforce format; validation happens at widget level

---

## Numeric Fields

### integer

Whole number (INT column).

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| size | string | normal | tiny/small/medium/big/normal |
| unsigned | boolean | FALSE | If TRUE, disallows negative values |

**Size ranges** (unsigned in parentheses):

- tiny: -128 to 127 (0 to 255)
- small: -32768 to 32767 (0 to 65535)
- medium: -8388608 to 8388607 (0 to 16777215)
- normal: -2147483648 to 2147483647 (0 to 4294967295)
- big: -9223372036854775808 to 9223372036854775807 (0 to 18446744073709551615)

```yaml
columns:
  quantity:
    name: quantity
    type: integer
    size: normal
    unsigned: TRUE
```

**Gotchas:** Size locked after data exists. Unsigned prevents negative values -- good for counts, bad for deltas.

### float

Floating-point number (DOUBLE column).

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| size | string | normal | tiny/small/medium/big/normal |
| unsigned | boolean | FALSE | If TRUE, disallows negative values |

**Gotchas:** Subject to floating-point precision errors -- NOT suitable for currency. Use decimal for money.

### decimal

Fixed-precision decimal (DECIMAL column) for currency and exact values.

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| precision | integer | 10 | Total digits (including scale) |
| scale | integer | 2 | Digits after decimal point |
| unsigned | boolean | FALSE | If TRUE, disallows negative values |

**Schema:** `DECIMAL(precision, scale)` -- precision max 32, scale max 10

```yaml
columns:
  price:
    name: price
    type: decimal
    precision: 10
    scale: 2
    unsigned: TRUE
```

**Gotchas:** Precision must be >= scale. For money, use precision=10, scale=2 (max $99,999,999.99). Values rounded to scale on save.

### boolean

TRUE/FALSE value (TINYINT 1).

**Schema:** `TINYINT(1) NOT NULL DEFAULT 0`

**Gotchas:** Stored as 0/1 integer. Default is 0 (FALSE). Use CheckboxWidget for input, BooleanFormatter for output.

### Numeric field mistakes

- **Using float for currency** -- Floating-point errors cause rounding issues. Always use decimal for money
- **Setting precision too low for decimal** -- Precision 10, scale 2 maxes at $99,999,999.99. For larger values, increase precision
- **Not setting unsigned for counts** -- Quantities, counts, IDs should be unsigned to prevent negative values
- **Forgetting scale rounds on save** -- Decimal with scale=2 rounds 10.999 to 11.00, not truncates

---

## Date/Time Fields

### datetime

Date and/or time value.

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| datetime_type | string | datetime | datetime/date |

**Schema:**

- datetime_type=datetime: `VARCHAR(20)` stores ISO 8601 format `YYYY-MM-DDTHH:MM:SS`
- datetime_type=date: `VARCHAR(20)` stores `YYYY-MM-DD`

**Extended properties:** `field__timezone` (if datetime_type=datetime)

**Gotchas:** Timezone stored separately in extended property. Date-only type has no time component -- adding time fails validation.

### daterange

Start and end date/time.

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| datetime_type | string | datetime | datetime/date/allday |

**Extended properties:**

- `field__end` -- end date/time
- `field__timezone` -- timezone
- `field__duration` -- calculated duration in seconds

**Gotchas:** Duration auto-calculated on save (end_timestamp - start_timestamp). Allday type treats full days with no time component.

### time

Time of day value (seconds since midnight: 0-86400).

**Schema:** `INT NOT NULL DEFAULT 0` (range 0-86400)

**Gotchas:** Stored as integer seconds since midnight. 86401 treated as NULL/empty. No timezone -- time-of-day only.

### time_range

Start and end time of day.

**Extended properties:**

- `field__end` -- end time
- `field__duration` -- calculated duration in seconds

**Gotchas:** Duration auto-calculated. If end < start, duration is NULL (no cross-midnight support).

### duration

Time span in seconds.

**Schema:** `INT NOT NULL DEFAULT 0`

**Gotchas:** Stored as seconds integer. DurationWidget provides granularity selection (years/months/days/hours/minutes). Display formatting via DurationFormatter.

### Date/time field mistakes

- **Using datetime for time-of-day** -- Use time type for repeated daily schedules; datetime includes full date
- **Forgetting timezone handling** -- datetime and daterange store timezone in extended property; access via `$item->{'field__timezone'}`
- **Expecting cross-midnight time ranges** -- time_range doesn't handle end < start (e.g., 23:00-01:00). Store as two ranges or use datetime
- **Not accounting for duration auto-calculation** -- daterange and time_range calculate duration on save; don't set manually

---

## Reference Fields

### entity_reference

Reference to any entity type.

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| target_type | string | NULL | Entity type ID (node, taxonomy_term, user, media, etc.) |

**Schema:** `INT UNSIGNED NOT NULL DEFAULT 0` (stores target entity ID)

```yaml
columns:
  category:
    name: category
    type: entity_reference
    target_type: taxonomy_term
  author:
    name: author
    type: entity_reference
    target_type: user
```

**Gotchas:** target_type required and locked after data exists. Only entity types with ID key allowed. No bundle filtering at storage level -- use widget settings for that.

### Reference field mistakes

- **Not setting target_type** -- Required field; entity_reference won't save without it
- **Trying to change target_type after data** -- Locked once data exists; requires field recreation
- **Forgetting access checks** -- Entity references don't auto-check access; validate in widget and check in formatter
- **Not configuring widget handler settings** -- Use EntityReferenceAutocompleteWidget or EntityReferenceSelectWidget settings to filter by bundle, sort, etc.

---

## File Fields

### file

File upload reference (stores file entity ID).

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| target_type | string | file | Always 'file' (auto-set) |
| uri_scheme | string | public | public/private |

**Schema:** `INT UNSIGNED NOT NULL DEFAULT 0` (file entity ID)

**Gotchas:** File entity ID stored, not file path. Use FileWidget with upload_location, max_filesize, file_extensions settings.

### image

Image file with extended properties (alt, title, width, height).

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| target_type | string | file | Always 'file' (auto-set) |
| uri_scheme | string | public | public/private |

**Extended properties:**

- `field__alt` -- VARCHAR(512) alt text
- `field__title` -- VARCHAR(1024) title text
- `field__width` -- INT image width in pixels
- `field__height` -- INT image height in pixels

**Gotchas:** Width/height auto-populated from image dimensions on save. Alt text separate from file entity. Access via `$item->{'thumbnail__alt'}`.

### File field mistakes

- **Not configuring file extensions** -- Widget settings control allowed extensions; storage doesn't validate
- **Using public for sensitive files** -- Set uri_scheme=private for files requiring access control
- **Forgetting alt text for accessibility** -- image type stores alt in extended property; required for accessibility
- **Not setting upload location** -- Configure via widget settings: `upload_location` like `field/[entity_type]/[field_name]`

---

## Data Fields

### link

Full link with URI, title, and options (target, class, etc.).

**Extended properties:**

- `field__title` -- VARCHAR(255) link title
- `field__options` -- BLOB serialized link options array

**Gotchas:** Options array stores attributes like `target`, `class`, `rel`. Access via `$item->{'link__options'}`. Validation constraints: LinkAccessConstraint, LinkExternalProtocolsConstraint, LinkNotExistingInternalConstraint, LinkTypeConstraint.

### map

Key-value pairs (associative array).

**Schema:** `BLOB` (serialized array)

**Gotchas:** Stored as serialized PHP array -- not queryable in database. Use map_string for simple key-value text, map for mixed types.

### map_string

Key-value pairs (string values only).

**Schema:** `BLOB` (serialized array)

**Gotchas:** Similar to map but enforces string values. Widget provides key-value input interface.

### uuid

Universally unique identifier.

**Schema:** `VARCHAR(128)`

**Gotchas:** Auto-generated on creation. No configuration UI. Has `never_check_empty` flag -- doesn't affect field empty state.

### Data field mistakes

- **Using map for queryable data** -- BLOB columns can't be queried efficiently; use discrete columns for searchable/filterable data
- **Not sanitizing link options** -- Link options array can contain XSS vectors; sanitize in formatter
- **Expecting map to be JSON** -- Stored as PHP serialized array, not JSON; use JSON:API normalizer for API exposure
- **Manually setting UUID** -- UUID auto-generated; setting manually can cause collisions

## See Also

- Reference: `/modules/contrib/custom_field/src/Plugin/CustomField/FieldType/`
