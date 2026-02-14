---
description: When you need JSON, XML, or other serialized output for APIs, AJAX endpoints, or headless/decoupled applications.
drupal_version: "11.x"
---

## 6. REST Export Display

### When to Use
When you need JSON, XML, or other serialized output for APIs, AJAX endpoints, or headless/decoupled applications.

### Steps
1. **Add REST export display** to view
2. **Configure path** for API endpoint
3. **Set authentication methods** (optional)
4. **Configure serializer formats** in style plugin settings
5. **Set access control** (API consumers need permission)

### REST Export Options

#### Path & Format Configuration
```yaml
rest_export_1:
  display_plugin: rest_export
  display_options:
    path: api/v1/articles
    auth: ['cookie', 'basic_auth']  # Optional auth providers
```

- **Path**: URL for API endpoint (no wildcard restrictions unlike page displays)
- **Auth**: Array of authentication provider IDs (`cookie`, `basic_auth`, custom)

Reference: `core/modules/rest/src/Plugin/views/display/RestExport.php` lines 255-274

#### Serializer Style Configuration
REST export displays default to `serializer` style plugin:

```yaml
display_options:
  style:
    type: serializer
    options:
      formats:
        json: json
        xml: xml
      uses_fields: false
```

- **formats**: Allowed output formats (json, xml, hal_json, etc.)
- **uses_fields**: If false, uses entity serialization; if true, uses field-based output

#### Route Configuration
REST exports respond only to GET requests with format requirements:

```yaml
# Auto-generated route requirements
_format: 'json|xml'  # Based on formats in style options
_auth: ['cookie', 'basic_auth']  # If auth is configured
```

Reference: RestExport.php lines 343-373

### Pattern
JSON API endpoint with basic auth:

```yaml
rest_export_1:
  id: rest_export_1
  display_title: 'JSON API'
  display_plugin: rest_export
  position: 2
  display_options:
    path: api/content
    auth:
      - basic_auth
    pager:
      type: some
      options:
        items_per_page: 50
        offset: 0
    style:
      type: serializer
      options:
        formats:
          json: json
    row:
      type: data_entity
      options:
        view_mode: default
    access:
      type: perm
      options:
        perm: 'access content'
```

### Common Mistakes
- Not setting authentication but requiring it in access → Falls back to anonymous; access check may fail unexpectedly
- Exposing sensitive data without access control → Always set appropriate permissions; REST exports bypass normal page access
- Using `data_entity` row without understanding view mode → Entity serializes with all accessible fields; control with view mode config
- Forgetting format negotiation → Client must request with `?_format=json` or Accept header; format fallback is first configured format
- Using exposed filters without AJAX → REST exports don't render forms; exposed filters work via query parameters only

### See Also
- Section 14: Access Control — securing API endpoints
- Section 15: Style & Row Plugins — serializer configuration
- Section 31: Security & Performance — REST export security
- Reference: [RestExport display plugin](https://api.drupal.org/api/drupal/core!modules!rest!src!Plugin!views!display!RestExport.php/11.x)
