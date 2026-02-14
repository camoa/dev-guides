---
description: "Removing entities from Drupal. Requires authentication and delete permissions. Irreversible without backups."
drupal_version: "11.x"
topic: "drupal/jsonapi"
---

## Deleting Resources (DELETE)

### When to Use

Removing entities from Drupal. Requires authentication and delete permissions. Irreversible without backups.

### Pattern

**DELETE request:**
```bash
curl -X DELETE "https://example.com/jsonapi/node/article/{uuid}" \
  -H "Accept: application/vnd.api+json" \
  -H "Authorization: Basic dXNlcjpwYXNz"
```

**Response:**
- Success: `204 No Content` (empty body)
- Errors: `403 Forbidden`, `404 Not Found`

**JavaScript example:**
```javascript
fetch(`/jsonapi/node/article/${uuid}`, {
  method: 'DELETE',
  headers: {
    'Accept': 'application/vnd.api+json',
    'Authorization': 'Basic ' + btoa('user:pass')
  }
})
  .then(response => {
    if (response.status === 204) {
      console.log('Deleted successfully');
    }
  });
```

### Common Mistakes

**Expecting response body:** DELETE returns `204 No Content` with empty body. WHY: Spec says no content on successful delete. Check status code, not body.

**Not handling 404 errors gracefully:** Deleting already-deleted entity returns 404. WHY: Entity no longer exists. Treat 404 as success in idempotent delete operations.

**Deleting without confirmation:** DELETE is permanent (unless content moderation enabled). WHY: No trash/recycle bin by default. Implement client-side confirmation dialogs.

**Assuming cascade deletes work via API:** Deleting parent doesn't auto-delete children. WHY: Entity reference field configuration controls cascade behavior. Check field settings.

### See Also
- [Creating Resources (POST)](creating-resources.md)
- [Updating Resources (PATCH)](updating-resources.md)
- [Security Best Practices](security-best-practices.md)
