---
description: Salesforce class reference — RestClient methods, SFID, SObject, SelectQueryResult, PushParams, MappingConstants, SOAP client
drupal_version: "11.x"
---

# Class Reference

## When to Use

> Use this reference when implementing custom code that interacts with the Salesforce module's PHP classes directly. All paths are relative to `/web/modules/contrib/salesforce/`.

## Decision

| Class | Location | Key Purpose |
|---|---|---|
| `SFID` | `src/SFID.php` | Salesforce ID value object (15/18 char) |
| `SObject` | `src/SObject.php` | Wrap a Salesforce record from API |
| `SelectQueryResult` | `src/SelectQueryResult.php` | Query results with pagination |
| `RestException` | `src/Rest/RestException.php` | Wrap API errors with response body |
| `RestResponse` | `src/Rest/RestResponse.php` | JSON-decoded API response |
| `PushParams` | `modules/salesforce_mapping/src/PushParams.php` | Push operation parameters wrapper |
| `MappedObjectStorage` | `modules/salesforce_mapping/src/MappedObjectStorage.php` | Custom storage for MappedObject |
| `MappingConstants` | `modules/salesforce_mapping/src/MappingConstants.php` | Sync trigger and direction constants |
| `SalesforceAuthConfig` | `src/Entity/SalesforceAuthConfig.php` | Auth provider config entity |
| `SoapClient` | `modules/salesforce_soap/src/Soap/SoapClient.php` | SOAP API wrapper (service: `salesforce_soap.client`) |

## Pattern

**SFID — 15 vs 18 character IDs:**
```php
$sfid = new \Drupal\salesforce\SFID('003000000000001AAA');
$sfid->is15();  // false
$sfid->is18();  // true
$prefix = substr((string) $sfid, 0, 3);  // object type prefix
```

**SObject — reading fields:**
```php
$contact = $client->objectRead('Contact', $sfid);
$email = $contact->field('Email');
$type = $contact->type();      // 'Contact'
$allFields = $contact->fields(); // associative array
```

**SelectQueryResult — pagination:**
```php
$results = $client->query($query);
echo $results->size();    // total matching records
foreach ($results->records() as $sobject) { /* ... */ }
if (!$results->done()) {
  $more = $client->queryMore($results);
}
```

**RestException — error details:**
```php
try {
  $client->objectCreate('Contact', $params);
} catch (\Drupal\salesforce\Rest\RestException $e) {
  $body = $e->getResponseBody(); // Salesforce error JSON
}
```

**PushParams — modifying in PUSH_PARAMS event:**
```php
public function pushParamsAlter(SalesforcePushParamsEvent $event): void {
  $params = $event->getParams();
  $params->setParam('Description__c', 'Modified value');
  $params->unsetParam('Internal_Field__c'); // remove field from push
}
```

**MappingConstants:**
```php
// Sync trigger constants
MappingConstants::SALESFORCE_MAPPING_SYNC_DRUPAL_CREATE  // 'push_create'
MappingConstants::SALESFORCE_MAPPING_SYNC_SF_UPDATE      // 'pull_update'

// Direction constants
MappingConstants::SALESFORCE_MAPPING_DIRECTION_DRUPAL_SF // 'drupal_sf'
MappingConstants::SALESFORCE_MAPPING_DIRECTION_SYNC      // 'sync'

// Multipicklist delimiter
MappingConstants::SALESFORCE_MAPPING_ARRAY_DELIMITER     // ';'
```

**Additional RestClient methods:**
- `objectReadbyExternalId($name, $field, $value)` — read by external ID
- `getDeleted($type, $start, $end)` — records deleted in timeframe
- `getUpdated($name, $start, $end)` — records updated in timeframe
- `queryAll($query)` — include deleted/archived records
- `listResources()` — list available REST API resources
- `getVersions($reset)` — list available API versions

## Common Mistakes

- **Wrong**: Comparing SFID strings directly with `==` — 15 and 18 char versions of the same record won't match → **Right**: Use the `SFID` value object and compare via `(string) $sfid` after normalization to 18 chars
- **Wrong**: Accessing `$results->records()` after `done()` returns true on the last page — the result is empty not null → **Right**: Always check `done()` before calling `queryMore()`

## See Also

- [REST Client API](rest-client-api.md)
- [SOQL Query Builder](soql-query-builder.md)
- [Mapped Objects API](mapped-objects-api.md)
- [Event System](event-system.md)
- Reference: `src/Rest/RestClientInterface.php`
