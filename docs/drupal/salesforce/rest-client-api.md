---
description: Salesforce REST client programmatic API — objectCreate, objectUpdate, objectUpsert, query, direct API calls, binary fetch
drupal_version: "11.x"
---

# REST Client API

## When to Use

> Use `salesforce.client` (`RestClient`) when you need programmatic, non-mapping-driven access to Salesforce objects — direct CRUD, raw SOQL queries, custom Apex REST calls, or fetching binary attachments.

## Decision

| Operation | Method | Notes |
|---|---|---|
| Query records | `$client->query($query)` | Pass `SelectQuery` or `SelectQueryRaw` |
| Create record | `$client->objectCreate($type, $fields)` | Returns SFID |
| Update record | `$client->objectUpdate($type, $sfid, $fields)` | No return value |
| Upsert record | `$client->objectUpsert($type, $extIdField, $value, $fields)` | Returns SFID |
| Read record | `$client->objectRead($type, $sfid)` | Returns `SObject` |
| Delete record | `$client->objectDelete($type, $sfid)` | No return value |
| Describe object | `$client->objectDescribe($type)` | Returns field metadata |
| Custom endpoint | `$client->apiCall($path, $params, $method)` | Relative or absolute path |
| Fetch binary | `$client->httpRequestRaw($url)` | Raw file content |

## Pattern

```php
$client = \Drupal::service('salesforce.client');

// Query
$query = new \Drupal\salesforce\SelectQuery('Contact');
$query->fields = ['Id', 'FirstName', 'LastName', 'Email'];
$query->addCondition('Email', "''", '!=');
$results = $client->query($query);

// Create
$sfid = $client->objectCreate('Contact', [
  'FirstName' => 'John',
  'Email' => 'john@example.com',
]);

// Upsert with external ID
$sfid = $client->objectUpsert('Contact', 'External_Id__c', $extId, [
  'FirstName' => 'Jane',
]);

// Apex REST endpoint
$response = $client->apiCall('/services/apexrest/MyEndpoint', [
  'recordId' => '003000000000001AAA',
], 'POST');

// Check initialization before use
if (!$client->isInit()) {
  throw new \Exception('Salesforce client not authorized');
}
```

## Common Mistakes

- **Wrong**: Calling client methods without checking `$client->isInit()` in custom code → **Right**: Check initialization or catch `\Drupal\salesforce\Rest\RestException` and inspect `$e->getResponseBody()`
- **Wrong**: Using `apiCall()` with a relative path for Apex REST → **Right**: Apex REST requires an absolute path starting with `/services/apexrest/`

## See Also

- [SOQL Query Builder](soql-query-builder.md)
- [Mapped Objects API](mapped-objects-api.md)
- [Class Reference](class-reference.md)
- Reference: `/web/modules/contrib/salesforce/src/Rest/RestClientInterface.php`
- Reference: `/web/modules/contrib/salesforce/src/Rest/RestClient.php`
