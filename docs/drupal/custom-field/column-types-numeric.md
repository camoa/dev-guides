---
description: "Numeric column types in Custom Field 5.0.2 -- integer, float, decimal, boolean -- with size ranges and precision rules."
tldr: "Four numeric column types cover whole numbers, floats, fixed-precision decimals and booleans; always use decimal (never float) for currency, and set unsigned on counts and IDs."
drupal_version: "11.x"
---

# Column Types: Numeric Fields

## When to Use

Storing numbers -- integers, floats, decimals, booleans in custom field columns.

## integer

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
  temperature:
    name: temperature
    type: integer
    size: small
    unsigned: FALSE
```

**Gotchas:** Size locked after data exists. Unsigned prevents negative values -- good for counts, bad for deltas.

## float

Floating-point number (DOUBLE column).

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| size | string | normal | tiny/small/medium/big/normal |
| unsigned | boolean | FALSE | If TRUE, disallows negative values |

**Schema:** DOUBLE precision floating point

```yaml
columns:
  latitude:
    name: latitude
    type: float
  longitude:
    name: longitude
    type: float
```

**Gotchas:** Subject to floating-point precision errors -- NOT suitable for currency. Use decimal for money.

## decimal

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
  weight_kg:
    name: weight_kg
    type: decimal
    precision: 8
    scale: 3
```

**Gotchas:** Precision must be >= scale. For money, use precision=10, scale=2 (max $99,999,999.99). Values rounded to scale on save.

## boolean

TRUE/FALSE value (TINYINT 1).

**Schema:** `TINYINT(1) NOT NULL DEFAULT 0`

```yaml
columns:
  is_active:
    name: is_active
    type: boolean
```

**Gotchas:** Stored as 0/1 integer. Default is 0 (FALSE). Use CheckboxWidget for input, BooleanFormatter for output.

## Common Mistakes

- **Using float for currency** -- Floating-point errors cause rounding issues. Always use decimal with appropriate precision/scale for money
- **Setting precision too low for decimal** -- Precision 10, scale 2 maxes at $99,999,999.99. For larger values, increase precision
- **Not setting unsigned for counts** -- Quantities, counts, IDs should be unsigned to prevent negative values
- **Forgetting scale rounds on save** -- Decimal with scale=2 rounds 10.999 to 11.00, not truncates

## See Also

- [Column Types: Text Fields](column-types-text.md)
- [Column Types: Date/Time Fields](column-types-datetime.md)
