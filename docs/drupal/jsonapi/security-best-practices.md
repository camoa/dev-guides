---
description: "Essential for all JSON:API deployments, especially production environments and public-facing APIs."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## Security Best Practices

### When to Use

Essential for all JSON:API deployments, especially production environments and public-facing APIs.

### Decision

| Practice | When to Apply | Impact |
|----------|---------------|--------|
| Read-only mode | Public APIs, no write needs | High - prevents all mutations |
| Audit access handlers | Before enabling write ops | High - prevents unauthorized access |
| Disable unused resources | All deployments | Medium - reduces attack surface |
| Use stable contrib modules | All deployments | High - security advisories |
| Secret base path | Additional obscurity layer | Low - security through obscurity |
| Limit mutable bundles | Selective write access | Medium - granular control |

### Items

#### 1. Use Stable Contrib Modules

**Description:** Only use stable modules with security coverage.

**Why:** Security advisories are only issued for stable releases. Alpha/beta/dev modules don't receive security support.

**Implementation:**
```bash
# Check module status
drush pm:list --status=enabled

# Only use stable versions
composer require drupal/jsonapi_extras:^3.0
```

#### 2. Audit Entity & Field Access

**Description:** Review and test access callbacks before enabling write operations.

**Why:** JSON:API respects Drupal access system but doesn't add extra protection. Weak access handlers expose data.

**Implementation:**
```php
// In custom module: implement hook_ENTITY_TYPE_access()
function mymodule_node_access(NodeInterface $node, $op, AccountInterface $account) {
  if ($node->bundle() === 'article' && $op === 'update') {
    // Custom access logic
    return AccessResult::forbiddenIf(!$account->hasPermission('edit articles'));
  }
  return AccessResult::neutral();
}

// Test access thoroughly
// - Anonymous users
// - Authenticated users without permissions
// - Edge cases (own content vs others)
```

#### 3. Expose Only What You Use

**Description:** Disable entity types and bundles not needed via API.

**Why:** Reduces attack surface and prevents accidental data exposure.

**Implementation via JSON:API Extras:**
```yaml
# config/install/jsonapi_extras.jsonapi_resource_config.taxonomy_term--tags.yml
id: taxonomy_term--tags
disabled: true
```

**Implementation via code:**
```php
/**
 * Implements hook_jsonapi_entity_filter_access().
 */
function mymodule_jsonapi_entity_filter_access(EntityTypeInterface $entity_type, AccountInterface $account) {
  // Disable all taxonomy terms from JSON:API
  if ($entity_type->id() === 'taxonomy_term') {
    return AccessResult::forbidden('Taxonomy not exposed via API');
  }
  return AccessResult::neutral();
}
```

#### 4. Read-Only Mode

**Description:** Disable write operations (POST, PATCH, DELETE) globally.

**Why:** Mitigates write-related vulnerabilities. Default since Drupal 9.

**Implementation:**
- Visit `/admin/config/services/jsonapi`
- Uncheck "Accept all JSON:API create, read, update, and delete operations"
- Save configuration

**Verify:**
```bash
# Should return 405 Method Not Allowed
curl -X POST https://example.com/jsonapi/node/article
```

#### 5. Secret Base Path

**Description:** Change `/jsonapi` to obscure path.

**Why:** Prevents automated scanners from discovering API. Defense in depth, not primary security.

**Implementation:**
```yaml
# config/default/services.yml
parameters:
  jsonapi.base_path: /hidden/b69dhj027ooae/jsonapi
```

**Result:**
```
Before: /jsonapi/node/article
After:  /hidden/b69dhj027ooae/jsonapi/node/article
```

**Gotcha:** Security through obscurity. Combine with proper authentication and access control.

#### 6. Limit Mutable Bundles

**Description:** Allow POST/PATCH only for specific bundles.

**Why:** Granular control over which content types are writable via API.

**Implementation:**
```php
// mymodule/src/Routing/JsonapiLimitingRouteSubscriber.php
namespace Drupal\mymodule\Routing;

use Drupal\Core\Routing\RouteSubscriberBase;
use Symfony\Component\Routing\RouteCollection;

class JsonapiLimitingRouteSubscriber extends RouteSubscriberBase {
  protected function alterRoutes(RouteCollection $collection) {
    $mutable_types = [
      'node--article' => TRUE,
      'custom_entity--custom_entity' => TRUE,
    ];

    foreach ($collection as $name => $route) {
      $defaults = $route->getDefaults();
      if (!empty($defaults['_is_jsonapi']) && !empty($defaults['resource_type'])) {
        $methods = $route->getMethods();
        $resource_type = $defaults['resource_type'];

        // Remove DELETE everywhere
        if (in_array('DELETE', $methods)) {
          $collection->remove($name);
        }
        // Remove POST/PATCH for non-whitelisted types
        elseif (empty($mutable_types[$resource_type])) {
          if (in_array('POST', $methods) || in_array('PATCH', $methods)) {
            $collection->remove($name);
          }
        }
      }
    }
  }
}
```

**Register service:**
```yaml
# mymodule.services.yml
services:
  mymodule.route_subscriber:
    class: Drupal\mymodule\Routing\JsonapiLimitingRouteSubscriber
    tags:
      - { name: event_subscriber }
```

### Common Mistakes

**Relying solely on obscurity:** Secret base path alone is insufficient. WHY: Once discovered, no protection exists. Always implement proper authentication and access control.

**Not testing anonymous access:** Assuming authentication is required without testing. WHY: Some endpoints might be accidentally public. Test thoroughly as anonymous user.

**Exposing internal fields:** Fields like `field_internal_notes` or `field_admin_comments` in API. WHY: Field-level access control might not be implemented. Use JSON:API Extras to disable sensitive fields.

**Granting broad permissions:** "Restful POST" permission without entity-specific limits. WHY: User can create/modify entities they shouldn't. Grant granular permissions per bundle.

**Not using HTTPS in production:** Transmitting authentication credentials over HTTP. WHY: Credentials are interceptable. Always use HTTPS (enforce with redirect).

**Ignoring rate limiting:** Allowing unlimited API requests. WHY: DoS vulnerability and resource exhaustion. Implement rate limiting via contrib module or reverse proxy.

### See Also
- [Authentication Patterns](authentication-patterns.md)
- [JSON:API Extras Customization](jsonapi-extras-customization.md)
- [Code Reference Map](code-reference-map.md)
- Drupal security best practices: https://www.drupal.org/docs/security-in-drupal
