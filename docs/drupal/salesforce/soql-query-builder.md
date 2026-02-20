---
description: SOQL query builder — SelectQuery properties, conditions, operators, pagination, raw SOQL with SelectQueryRaw
drupal_version: "11.x"
---

# SOQL Query Builder

## When to Use

> Use `SelectQuery` for programmatic SOQL queries with conditions. Use `SelectQueryRaw` for complex queries with subqueries or syntax not supported by the builder.

## Decision

| Approach | Use When |
|---|---|
| `SelectQuery` builder | Standard field/condition queries, simpler logic |
| `SelectQueryRaw` | Subqueries, complex SOQL not expressible via builder |
| `$client->queryAll()` | Include archived/deleted records in results |
| `$client->queryMore()` | Paginate through large result sets |

**Operators supported:** `=`, `!=`, `<`, `>`, `LIKE`, `IN`, `NOT IN`

## Pattern

```php
// Builder pattern
$query = new \Drupal\salesforce\SelectQuery('Contact');
$query->fields = ['Id', 'Name', 'Email', 'Account.Name'];
$query->addCondition('Status__c', 'Active');
$query->addCondition('Country__c', ['US', 'CA'], 'IN'); // Array → IN clause
$query->addCondition('Email', '%@example.com', 'LIKE');
$query->order = ['LastModifiedDate' => 'DESC'];
$query->limit = 100;
$query->offset = 0;
$query->conjunction = 'AND'; // or 'OR'
$results = $client->query($query);

// Raw SOQL (subqueries, complex syntax)
$query = new \Drupal\salesforce\SelectQueryRaw(
  "SELECT Id, Name, (SELECT Id FROM Contacts) FROM Account WHERE Type = 'Customer'"
);

// Pagination
$results = $client->query($query);
while (!$results->done()) {
  foreach ($results->records() as $sobject) {
    $name = $sobject->field('Name');
  }
  $results = $client->queryMore($results);
}
```

## Common Mistakes

- **Wrong**: Not checking `$results->done()` before calling `queryMore()` — calling it when done throws an exception → **Right**: Always check `done()` before paginating
- **Wrong**: Using `SELECT *` in SOQL — not supported in Salesforce → **Right**: Always specify explicit field lists in `$query->fields`

## See Also

- [REST Client API](rest-client-api.md)
- [Pull Synchronization](pull-synchronization.md)
- Reference: `/web/modules/contrib/salesforce/src/SelectQuery.php`
- Reference: `/web/modules/contrib/salesforce/src/SelectQueryRaw.php`
- Reference: `/web/modules/contrib/salesforce/src/SelectQueryResult.php`
- Salesforce SOQL docs: https://developer.salesforce.com/docs/atlas.en-us.soql_sosl.meta/soql_sosl/
