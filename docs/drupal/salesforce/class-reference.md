---
description: "Salesforce class reference — RestClient methods, SFID, SObject, SelectQueryResult, PushParams, MappingConstants, SOAP client"
tldr: "Use this reference when implementing custom code that interacts with the Salesforce module's PHP classes directly. All paths are relative to `/web/modules/contrib/salesforce/`."
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
| `SelectQueryRaw` | `src/SelectQueryRaw.php` | Execute raw SOQL (vs. builder pattern) |
| `SelectQueryResult` | `src/SelectQueryResult.php` | Query results with pagination |
| `RestException` | `src/Rest/RestException.php` | Wrap API errors with response body |
| `RestResponse` | `src/Rest/RestResponse.php` | JSON-decoded API response |
| `SalesforceIdentity` | `src/Rest/SalesforceIdentity.php` | Identity info returned after authentication |
| `PushParams` | `modules/salesforce_mapping/src/PushParams.php` | Push operation parameters wrapper |
| `MappedObjectStorage` | `modules/salesforce_mapping/src/MappedObjectStorage.php` | Custom storage for MappedObject |
| `MappingConstants` | `modules/salesforce_mapping/src/MappingConstants.php` | Sync trigger and direction constants |
| `SalesforceAuthConfig` | `src/Entity/SalesforceAuthConfig.php` | Auth provider config entity |
| `SalesforceAuthTokenStorage` | `src/Storage/SalesforceAuthTokenStorage.php` | OAuth token and identity storage |
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

## Additional RestClient Methods

Beyond the commonly used methods documented above, RestClient provides:

**External ID Operations:**
- `objectReadbyExternalId($name, $field, $value)` - Read object by external ID field

**Time-Based Queries:**
- `getDeleted($type, $startDate, $endDate)` - Get records deleted in timeframe
- `getUpdated($name, $start, $end)` - Get records updated in timeframe

**Query Pagination:**
- `queryAll($query)` - Query including deleted/archived records
- `queryMore($results)` - Fetch next page of query results

**API Resources:**
- `listResources()` - List available REST API resources
- `getVersions($reset)` - List available API versions

**HTTP Client Configuration:**
- `setHttpClientOptions($options)` - Set Guzzle HTTP client options
- `setHttpClientOption($name, $value)` - Set single HTTP option
- `getHttpClientOptions()` - Get current HTTP options
- `getHttpClientOption($name)` - Get single HTTP option

**Reference:** `/web/modules/contrib/salesforce/src/Rest/RestClientInterface.php`

## Additional Classes Reference

### SalesforceAuthConfig Entity

Config entity for storing auth provider configurations.

**Location:** `/web/modules/contrib/salesforce/src/Entity/SalesforceAuthConfig.php`

**Key Methods:**
- `getPlugin()` - Get the auth provider plugin instance
- `getCredentials()` - Get credentials from the provider
- `getPluginsAsOptions()` - Get available plugins for forms

### SalesforceAuthTokenStorage

Service for storing OAuth tokens and identity in Drupal state.

**Location:** `/web/modules/contrib/salesforce/src/Storage/SalesforceAuthTokenStorage.php`
**Service ID:** `salesforce.auth_token_storage`

**Key Methods:**
- `storeAccessToken($service, $token)` - Store OAuth token
- `retrieveAccessToken($service)` - Retrieve stored token
- `hasAccessToken($service)` - Check if token exists
- `clearToken($service)` - Remove stored token
- `storeIdentity($service, $identity)` - Store user identity
- `retrieveIdentity($service)` - Retrieve user identity

### RestException

Exception class for Salesforce API errors. Wraps HTTP response for debugging.

**Location:** `/web/modules/contrib/salesforce/src/Rest/RestException.php`

**Key Methods:**
- `getResponse()` - Get the HTTP response object
- `getResponseBody()` - Get raw response body for error details

**Usage:**
```php
try {
  $result = $client->objectCreate('Contact', $params);
} catch (\Drupal\salesforce\Rest\RestException $e) {
  $body = $e->getResponseBody();  // Contains Salesforce error details
  \Drupal::logger('mymodule')->error('SF Error: @body', ['@body' => $body]);
}
```

### RestResponse

Wrapper for Salesforce API responses with JSON decoding.

**Location:** `/web/modules/contrib/salesforce/src/Rest/RestResponse.php`

**Key Properties:**
- `$data` - JSON-decoded response body

**Subclasses:**
- `RestResponseDescribe` - Object describe results (`/web/modules/contrib/salesforce/src/Rest/RestResponseDescribe.php`)
- `RestResponseResources` - Available resources list (`/web/modules/contrib/salesforce/src/Rest/RestResponseResources.php`)

### SalesforceIdentity

Wrapper for Salesforce user identity information returned after authentication.

**Location:** `/web/modules/contrib/salesforce/src/Rest/SalesforceIdentity.php`

**Key Methods:**
- `getUrl($api_type, $api_version)` - Get API endpoint URLs from identity

### SelectQueryRaw

Class for executing raw SOQL queries (vs. builder pattern).

**Location:** `/web/modules/contrib/salesforce/src/SelectQueryRaw.php`

**Usage:**
```php
$query = new SelectQueryRaw("SELECT Id, Name FROM Contact WHERE Email != ''");
$results = $client->query($query);
```

### SelectQueryResult

Wrapper for SOQL query results with pagination support.

**Location:** `/web/modules/contrib/salesforce/src/SelectQueryResult.php`

**Key Methods:**
- `records()` - Get array of SObject records
- `size()` - Total number of records matching query
- `done()` - TRUE if no more results, FALSE if pagination needed
- `nextRecordsUrl()` - URL for next page of results

**Usage:**
```php
$results = $client->query($query);
foreach ($results->records() as $sobject) {
  $name = $sobject->field('Name');
}
if (!$results->done()) {
  $moreResults = $client->queryMore($results);
}
```

### SFID

Value object for Salesforce record IDs (handles 15 and 18 character formats).

**Location:** `/web/modules/contrib/salesforce/src/SFID.php`

**Key Methods:**
- `is15()` - Check if 15-character format
- `is18()` - Check if 18-character format (case-insensitive)
- `__toString()` - Get string representation

**Usage:**
```php
$sfid = new \Drupal\salesforce\SFID('003000000000001AAA');
$prefix = substr((string) $sfid, 0, 3);  // Object type prefix
```

### SObject

Wrapper for Salesforce object records returned from API.

**Location:** `/web/modules/contrib/salesforce/src/SObject.php`

**Key Methods:**
- `id()` - Get record SFID
- `type()` - Get object type name
- `field($name)` - Get field value by name
- `fields()` - Get all fields as associative array

**Usage:**
```php
$contact = $client->objectRead('Contact', $sfid);
$email = $contact->field('Email');
$type = $contact->type();  // 'Contact'
$allFields = $contact->fields();
```

### PushParams

Wrapper for push operation parameters.

**Location:** `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/PushParams.php`

**Key Methods:**
- `getParams()` - Get all push parameters
- `getParam($key)` - Get specific parameter
- `setParam($key, $value)` - Set parameter (use in PUSH_PARAMS event)
- `unsetParam($key)` - Remove parameter
- `getMapping()` - Get the mapping entity
- `getDrupalEntity()` - Get the Drupal entity being pushed

### MappedObjectStorage

Custom storage handler for MappedObject entities.

**Location:** `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/MappedObjectStorage.php`

**Key Methods:**
- `loadByDrupal($entity_type_id, $entity_id)` - Load by Drupal entity info
- `loadByEntity($entity)` - Load by Drupal entity object
- `loadByEntityAndMapping($entity, $mapping)` - Load single by entity and mapping
- `loadBySfid($sfid)` - Load by Salesforce ID
- `loadBySfidAndMapping($sfid, $mapping)` - Load single by SFID and mapping
- `setForcePull($mapping)` - Mark all mapped objects for force pull

### MappingConstants

Constants for mapping configuration values.

**Location:** `/web/modules/contrib/salesforce/modules/salesforce_mapping/src/MappingConstants.php`

**Sync Trigger Constants:**
- `SALESFORCE_MAPPING_SYNC_DRUPAL_CREATE` = 'push_create'
- `SALESFORCE_MAPPING_SYNC_DRUPAL_UPDATE` = 'push_update'
- `SALESFORCE_MAPPING_SYNC_DRUPAL_DELETE` = 'push_delete'
- `SALESFORCE_MAPPING_SYNC_SF_CREATE` = 'pull_create'
- `SALESFORCE_MAPPING_SYNC_SF_UPDATE` = 'pull_update'
- `SALESFORCE_MAPPING_SYNC_SF_DELETE` = 'pull_delete'

**Direction Constants:**
- `SALESFORCE_MAPPING_DIRECTION_DRUPAL_SF` = 'drupal_sf'
- `SALESFORCE_MAPPING_DIRECTION_SF_DRUPAL` = 'sf_drupal'
- `SALESFORCE_MAPPING_DIRECTION_SYNC` = 'sync'

**Other Constants:**
- `SALESFORCE_MAPPING_ARRAY_DELIMITER` = ';' (multipicklist delimiter)
- `SALESFORCE_MAPPING_NAME_LENGTH` = 128
- `SALESFORCE_MAPPING_STATUS_SUCCESS` = 1
- `SALESFORCE_MAPPING_STATUS_ERROR` = 0

## SOAP Module Details

### SoapClient

Wrapper around the Salesforce Partner SOAP API.

**Location:** `/web/modules/contrib/salesforce/modules/salesforce_soap/src/Soap/SoapClient.php`
**Service ID:** `salesforce_soap.client`

**Extends:** `SforcePartnerClient` (from developerforce/force.com-toolkit-for-php)

**Key Methods:**
- `connect()` - Establish SOAP connection using REST auth tokens
- `isConnected()` - Check connection status
- `trySoap($function, $params, $refresh)` - Execute SOAP call with auto-retry

**Use Cases:**
- Metadata API operations not available in REST
- Bulk API operations
- Legacy integrations requiring SOAP

**Decision Point:** Prefer REST API for all standard operations. Use SOAP only when specific functionality is unavailable via REST.

## Common Mistakes

- **Wrong**: Comparing SFID strings directly with `==` — 15 and 18 char versions of the same record won't match → **Right**: Use the `SFID` value object and compare via `(string) $sfid` after normalization to 18 chars
- **Wrong**: Accessing `$results->records()` after `done()` returns true on the last page — the result is empty not null → **Right**: Always check `done()` before calling `queryMore()`

## See Also

- [REST Client API](rest-client-api.md)
- [SOQL Query Builder](soql-query-builder.md)
- [Mapped Objects API](mapped-objects-api.md)
- [Event System](event-system.md)
- Reference: `src/Rest/RestClientInterface.php`
