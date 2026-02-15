---
description: Working with datetime, daterange, time, time_range, and duration sub-fields including widget selection and timezone handling.
---

# Date/Time Sub-Fields

## When to Use

Working with date, time, date range, time range, or duration columns in custom fields.

## Pattern

**Datetime column**:

```yaml
columns:
  event_date:
    name: event_date
    type: datetime
    datetime_type: datetime  # or 'date' for date-only
```

**Daterange column**:

```yaml
columns:
  event_period:
    name: event_period
    type: daterange
    datetime_type: datetime  # or 'date' or 'allday'
```

**Accessing in code**:

```php
// Datetime
$datetime_value = $node->field_custom->event_date; // ISO 8601 string
$timezone = $node->field_custom->{'event_date__timezone'};
$date_obj = new DrupalDateTime($datetime_value, $timezone);

// Daterange
$start = $node->field_custom->event_period; // Start date
$end = $node->field_custom->{'event_period__end'}; // End date
$timezone = $node->field_custom->{'event_period__timezone'};
$duration_seconds = $node->field_custom->{'event_period__duration'};

// Time
$time_seconds = $node->field_custom->opening_time; // 0-86400
$hours = floor($time_seconds / 3600);
$minutes = floor(($time_seconds % 3600) / 60);
```

## Decision

| Widget | When to Use | Notes |
|---|---|---|
| DateTimeDefaultWidget | Standard date/time picker | HTML5 inputs, best browser support |
| DateTimeDatelistWidget | Dropdowns for date parts | Accessible, no JS dependency |
| DateTimeLocalWidget | HTML5 datetime-local input | Simple, but limited browser support |
| DateRangeDefaultWidget | Start/end date picker | For daterange type |
| TimeWidget | Time-of-day picker | For time type (0-86400 seconds) |
| TimeRangeWidget | Start/end time | For time_range type |
| DurationWidget | Duration with granularity | Years/months/days/hours/minutes selector |

## Common Mistakes

- **Mixing date types and widgets** -- datetime_type=date requires date-only widget; datetime requires datetime widget
- **Not handling timezones** -- Datetime and daterange store timezone in extended property; don't assume UTC
- **Using time for timestamps** -- time is time-of-day only (0-86400); use datetime for full timestamps
- **Forgetting duration auto-calculation** -- daterange and time_range calculate duration on save; read-only property
- **Cross-midnight time ranges** -- time_range doesn't support end < start (23:00 to 01:00); use two ranges or datetime

## See Also

- Reference: `/modules/contrib/custom_field/src/Plugin/CustomField/FieldWidget/DateTimeDefaultWidget.php`
