---
description: "Date/time column types in Custom Field 5.0.2 -- datetime, daterange, time, time_range, duration -- with extended properties and auto-calculated duration."
tldr: "Five date/time column types match the exact sub-type needed (datetime vs date-only vs time-of-day vs range); daterange and time_range auto-calculate duration on save, and time_range has no cross-midnight support."
drupal_version: "11.x"
---

# Column Types: Date/Time Fields

## When to Use

Storing dates, times, date ranges, time ranges, or durations in custom field columns.

## datetime

Date and/or time value.

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| datetime_type | string | datetime | datetime/date |

**Schema:**

- datetime_type=datetime: `VARCHAR(20)` stores ISO 8601 format `YYYY-MM-DDTHH:MM:SS`
- datetime_type=date: `VARCHAR(20)` stores `YYYY-MM-DD`

**Extended properties:** `field__timezone` (if datetime_type=datetime)

```yaml
columns:
  event_date:
    name: event_date
    type: datetime
    datetime_type: datetime
```

**Gotchas:** Timezone stored separately in extended property. Date-only type has no time component -- adding time fails validation.

## daterange

Start and end date/time.

| Setting | Type | Default | Notes |
|---------|------|---------|-------|
| datetime_type | string | datetime | datetime/date/allday |

**Extended properties:**

- `field__end` -- end date/time
- `field__timezone` -- timezone
- `field__duration` -- calculated duration in seconds

```yaml
columns:
  event_period:
    name: event_period
    type: daterange
    datetime_type: datetime
```

**Gotchas:** Duration auto-calculated on save (end_timestamp - start_timestamp). Allday type treats full days with no time component.

## time

Time of day value (seconds since midnight: 0-86400).

**Schema:** `INT NOT NULL DEFAULT 0` (range 0-86400)

```yaml
columns:
  opening_time:
    name: opening_time
    type: time
```

**Gotchas:** Stored as integer seconds since midnight. 86401 treated as NULL/empty. No timezone -- time-of-day only.

## time_range

Start and end time of day.

**Schema:** Start `INT` (0-86400), End `INT` (0-86400)

**Extended properties:**

- `field__end` -- end time
- `field__duration` -- calculated duration in seconds

```yaml
columns:
  business_hours:
    name: business_hours
    type: time_range
```

**Gotchas:** Duration auto-calculated. If end < start, duration is NULL (no cross-midnight support).

## duration

Time span in seconds.

**Schema:** `INT NOT NULL DEFAULT 0`

```yaml
columns:
  processing_time:
    name: processing_time
    type: duration
```

**Gotchas:** Stored as seconds integer. DurationWidget provides granularity selection (years/months/days/hours/minutes). Display formatting via DurationFormatter.

## Common Mistakes

- **Using datetime for time-of-day** -- Use time type for repeated daily schedules; datetime includes full date
- **Forgetting timezone handling** -- datetime and daterange store timezone in extended property; access via `$item->{'field__timezone'}`
- **Expecting cross-midnight time ranges** -- time_range doesn't handle end < start (e.g., 23:00-01:00). Store as two ranges or use datetime
- **Not accounting for duration auto-calculation** -- daterange and time_range calculate duration on save; don't set manually

## See Also

- [Column Types: Numeric Fields](column-types-numeric.md)
- [Column Types: Reference Fields](column-types-reference.md)
- [Date/Time Sub-Fields](datetime-fields.md) -- widget selection and code access patterns
